'''
Asynchronous data loader
========================

This is the Asynchronous Loader. You can use it to load an image
and use it, even if data are not yet available. You must specify a default
loading image for using a such loader::

    from kivy import *
    image = Loader.image('mysprite.png')

You can also load image from url::

    image = Loader.image('http://mysite.com/test.png')

If you want to change the default loading image, you can do::

    Loader.loading_image = Image('another_loading.png')

Tweaking the asynchronous loader
--------------------------------

.. versionadded:: 1.5.2

You can now tweak the loader to have a better user experience or more
performance, depending of the images you're gonna to load. Take a look at the
parameters:

    - :data:`Loader.num_workers` - define the number of threads to start for
      loading images
    - :data:`Loader.max_upload_per_frame` - define the maximum image uploads in
      GPU to do per frames.

'''

__all__ = ('Loader', 'LoaderBase', 'ProxyImage')

from kivy import kivy_data_dir
from kivy.logger import Logger
from kivy.clock import Clock
from kivy.cache import Cache
from kivy.core.image import ImageLoader, Image

from collections import deque
from time import sleep
from os.path import join
from os import write, close, unlink, environ

# Register a cache for loader
Cache.register('kivy.loader', limit=500, timeout=60)


class ProxyImage(Image):
    '''Image returned by the Loader.image() function.

    :Properties:
        `loaded`: bool, default to False
            It can be True if the image is already cached

    :Events:
        `on_load`
            Fired when the image is loaded and changed
    '''

    def __init__(self, arg, **kwargs):
        kwargs.setdefault('loaded', False)
        super(ProxyImage, self).__init__(arg, **kwargs)
        self.loaded = kwargs.get('loaded')
        self.register_event_type('on_load')

    def on_load(self):
        pass


class LoaderBase(object):
    '''Common base for Loader and specific implementation.
    By default, Loader will be the best available loader implementation.

    The _update() function is called every 1 / 25.s or each frame if we have
    less than 25 FPS.
    '''

    def __init__(self):

        self._loading_image = None
        self._error_image = None
        self._num_workers = 2
        self._max_upload_per_frame = 2

        self._q_load = deque()
        self._q_done = deque()
        self._client = []
        self._running = False
        self._start_wanted = False
        self._trigger_update = Clock.create_trigger(self._update)

    def __del__(self):
        try:
            Clock.unschedule(self._update)
        except Exception:
            pass

    def _set_num_workers(self, num):
        if num < 2:
            raise Exception('Must have at least 2 workers')
        self._num_workers = num
    def _get_num_workers(self):
        return self._num_workers

    num_workers = property(_get_num_workers, _set_num_workers)
    '''Number of workers to use while loading. (used only if the loader
    implementation support it.). This setting impact the loader only at the
    beginning. Once the loader is started, the setting has no impact::

        from kivy.loader import Loader
        Loader.num_workers = 4

    The default value is 2 for giving a smooth user experience. You could
    increase the number of workers, then all the images will be loaded faster,
    but the user will not been able to use the application while loading.
    Prior to 1.5.2, the default number was 20, and loading many full-hd images
    was blocking completly the application.

    .. versionadded:: 1.5.2
    '''

    def _set_max_upload_per_frame(self, num):
        if num is not None and num < 1:
            raise Exception('Must have at least 1 image processing per image')
        self._max_upload_per_frame = num
    def _get_max_upload_per_frame(self):
        return self._max_upload_per_frame

    max_upload_per_frame = property(_get_max_upload_per_frame,
            _set_max_upload_per_frame)
    '''Number of image to upload per frame. By default, we'll upload only 2
    images in the GPU per frame. If you are uploading many tiny images, you can
    easily increase this parameter to 10, or more.
    If you are loading multiples Full-HD images, the upload time can be
    consequent, and can stuck the application during the upload. If you want a
    smooth experience, let the default.

    As matter of fact, a Full-HD RGB image will take ~6MB in memory, so it will
    take times. If you have activated mipmap=True too, then the GPU must
    calculate the mipmap of this big images too, in real time. Then it can be
    smart to reduce the :data:`max_upload_per_frame` to 1 or 2. If you get ride
    of that (or reduce it a lot), take a look at the DDS format.

    .. versionadded:: 1.5.2
    '''

    @property
    def loading_image(self):
        '''Image used for loading (readonly)'''
        if not self._loading_image:
            loading_png_fn = join(kivy_data_dir, 'images', 'image-loading.gif')
            self._loading_image = ImageLoader.load(filename=loading_png_fn)
        return self._loading_image

    @property
    def error_image(self):
        '''Image used for error (readonly)'''
        if not self._error_image:
            error_png_fn = join(
                'atlas://data/images/defaulttheme/image-missing')
            self._error_image = ImageLoader.load(filename=error_png_fn)
        return self._error_image

    def start(self):
        '''Start the loader thread/process'''
        self._running = True

    def run(self, *largs):
        '''Main loop for the loader.'''
        pass

    def stop(self):
        '''Stop the loader thread/process'''
        self._running = False

    def _load(self, kwargs):
        '''(internal) Loading function, called by the thread.
        Will call _load_local() if the file is local,
        or _load_urllib() if the file is on Internet'''

        # FIXME, make it configurable?
        while len(self._q_done) > self.max_upload_per_frame * 2:
            sleep(0.1)

        filename = kwargs['filename']
        load_callback = kwargs['load_callback']
        post_callback = kwargs['post_callback']
        try:
            proto = filename.split(':', 1)[0]
        except:
            #if blank filename then return
            return
        if load_callback is not None:
            data = load_callback(filename)
        elif proto in ('http', 'https', 'ftp', 'smb'):
            data = self._load_urllib(filename, kwargs['kwargs'])
        else:
            data = self._load_local(filename, kwargs['kwargs'])

        if post_callback:
            data = post_callback(data)

        self._q_done.append((filename, data))
        self._trigger_update()

    def _load_local(self, filename, kwargs):
        '''(internal) Loading a local file'''
        # With recent changes to CoreImage, we must keep data otherwise,
        # we might be unable to recreate the texture afterwise.
        return ImageLoader.load(filename, keep_data=True, **kwargs)

    def _load_urllib(self, filename, kwargs):
        '''(internal) Loading a network file. First download it, save it to a
        temporary file, and pass it to _load_local()'''
        import urllib2
        proto = filename.split(':', 1)[0]
        if proto == 'smb':
            try:
                # note: it's important to load SMBHandler every time
                # otherwise the data is occasionaly not loaded
                from smb.SMBHandler import SMBHandler
            except ImportError:
                Logger.warning(
                    'Loader: can not load PySMB: make sure it is installed')
                return
        import tempfile
        data = fd = _out_osfd = None
        try:
            _out_filename = ''
            suffix = '.%s' % (filename.split('.')[-1])
            _out_osfd, _out_filename = tempfile.mkstemp(
                    prefix='kivyloader', suffix=suffix)

            if proto == 'smb':
                # read from samba shares
                fd = urllib2.build_opener(SMBHandler).open(filename)
            else:
                # read from internet
                fd = urllib2.urlopen(filename)
            idata = fd.read()
            fd.close()
            fd = None

            # write to local filename
            write(_out_osfd, idata)
            close(_out_osfd)
            _out_osfd = None

            # load data
            data = self._load_local(_out_filename, kwargs)
        except Exception:
            Logger.exception('Failed to load image <%s>' % filename)
            # close file when remote file not found or download error
            close(_out_osfd)
            return self.error_image
        finally:
            if fd:
                fd.close()
            if _out_osfd:
                close(_out_osfd)
            if _out_filename != '':
                unlink(_out_filename)

        return data

    def _update(self, *largs):
        '''(internal) Check if a data is loaded, and pass to the client'''
        # want to start it ?
        if self._start_wanted:
            if not self._running:
                self.start()
            self._start_wanted = False

        for x in xrange(self.max_upload_per_frame):
            try:
                filename, data = self._q_done.pop()
            except IndexError:
                return

            # create the image
            image = data  # ProxyImage(data)
            if not image.nocache:
                Cache.append('kivy.loader', filename, image)

            # update client
            for c_filename, client in self._client[:]:
                if filename != c_filename:
                    continue
                # got one client to update
                client.image = image
                client.loaded = True
                client.dispatch('on_load')
                self._client.remove((c_filename, client))

        self._trigger_update()

    def image(self, filename, load_callback=None, post_callback=None, **kwargs):
        '''Load a image using loader. A Proxy image is returned with a loading
        image.

      ::
            img = Loader.image(filename)
            # img will be a ProxyImage.
            # You'll use it the same as an Image class.
            # Later, when the image is really loaded,
            # the loader will change the img.image property
            # to the new loaded image

        '''
        data = Cache.get('kivy.loader', filename)
        if data not in (None, False):
            # found image, if data is not here, need to reload.
            return ProxyImage(data,
                    loading_image=self.loading_image,
                    loaded=True, **kwargs)

        client = ProxyImage(self.loading_image,
                    loading_image=self.loading_image, **kwargs)
        self._client.append((filename, client))

        if data is None:
            # if data is None, this is really the first time
            self._q_load.appendleft({
                'filename': filename,
                'load_callback': load_callback,
                'post_callback': post_callback,
                'kwargs': kwargs})
            if not kwargs.get('nocache', False):
                Cache.append('kivy.loader', filename, False)
            self._start_wanted = True
            self._trigger_update()
        else:
            # already queued for loading
            pass

        return client

#
# Loader implementation
#

if 'KIVY_DOC' in environ:

    Loader = None

else:

    #
    # Try to use pygame as our first choice for loader
    #

    try:
        import pygame

        class LoaderPygame(LoaderBase):

            def __init__(self):
                super(LoaderPygame, self).__init__()
                self.worker = None

            def start(self):
                super(LoaderPygame, self).start()
                self.worker = pygame.threads.WorkerQueue()
                self.worker.do(self.run)

            def stop(self):
                super(LoaderPygame, self).stop()
                self.worker.stop()

            def run(self, *largs):
                while self._running:
                    try:
                        parameters = self._q_load.pop()
                    except:
                        sleep(0.1)
                        continue
                    self.worker.do(self._load, parameters)

        Loader = LoaderPygame()
        Logger.info('Loader: using <pygame> as thread loader')

    except:

        #
        # Default to the clock loader
        #
        class LoaderClock(LoaderBase):
            '''Loader implementation using a simple Clock()'''

            def start(self):
                super(LoaderClock, self).start()
                Clock.schedule_interval(self.run, 0)

            def stop(self):
                super(LoaderClock, self).stop()
                Clock.unschedule(self.run)

            def run(self, *largs):
                while self._running:
                    try:
                        parameters = self._q_load.pop()
                    except IndexError:
                        return
                self._load(parameters)

        Loader = LoaderClock()
        Logger.info('Loader: using <clock> as thread loader')

