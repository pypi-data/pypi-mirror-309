"""
The base classes.
"""

__all__ = ["WrapperRenderCanvas", "BaseRenderCanvas", "BaseLoop", "BaseTimer"]

import importlib

from ._events import EventEmitter, EventType  # noqa: F401
from ._loop import Scheduler, BaseLoop, BaseTimer
from ._coreutils import log_exception


# Notes on naming and prefixes:
#
# Since BaseRenderCanvas can be used as a mixin with classes in a GUI framework,
# we must avoid using generic names to avoid name clashes.
#
# * `.public_method`: Public API: usually at least two words, (except the close() method)
# * `._private_method`: Private methods for scheduler and subclasses.
# * `.__private_attr`: Private to exactly this class.
# * `._rc_method`: Methods that the subclass must implement.


class BaseRenderCanvas:
    """The base canvas class.

    Each backends provides its own canvas subclass by implementing a predefined
    set of private methods.

    This base class defines a uniform canvas API so render systems can use code
    that is portable accross multiple GUI libraries and canvas targets. The
    scheduling mechanics are generic, even though they run on different backend
    event systems.

    Arguments:
        size (tuple): the logical size (width, height) of the canvas.
        title (str): The title of the canvas. Can use '$backend' to show the RenderCanvas class name,
            and '$fps' to show the fps.
        update_mode (EventType): The mode for scheduling draws and events. Default 'ondemand'.
        min_fps (float): A minimal frames-per-second to use when the ``update_mode`` is 'ondemand'.
            The default is 1: even without draws requested, it still draws every second.
        max_fps (float): A maximal frames-per-second to use when the ``update_mode`` is 'ondemand'
            or 'continuous'. The default is 30, which is usually enough.
        vsync (bool): Whether to sync the draw with the monitor update. Helps
            against screen tearing, but can reduce fps. Default True.
        present_method (str | None): Override the method to present the rendered result.
            Can be set to e.g. 'screen' or 'bitmap'. Default None (auto-select).

    """

    def __init__(
        self,
        *args,
        size=(640, 480),
        title="$backend",
        update_mode="ondemand",
        min_fps=1.0,
        max_fps=30.0,
        vsync=True,
        present_method=None,
        **kwargs,
    ):
        # Initialize superclass. Note that super() can be e.g. a QWidget, RemoteFrameBuffer, or object.
        super().__init__(*args, **kwargs)

        # If this is a wrapper, no need to initialize furher
        if isinstance(self, WrapperRenderCanvas):
            return

        # The vsync is not-so-elegantly strored on the canvas, and picked up by wgou's canvas contex.
        self._vsync = bool(vsync)

        # Variables and flags used internally
        self.__is_drawing = False
        self.__title_info = {
            "raw": "",
            "fps": "?",
            "backend": self.__class__.__name__,
        }

        # Events and scheduler
        self._events = EventEmitter()
        self.__scheduler = None
        loop = self._rc_get_loop()
        if loop is not None:
            self.__scheduler = Scheduler(
                self,
                self._events,
                self._rc_get_loop(),
                min_fps=min_fps,
                max_fps=max_fps,
                mode=update_mode,
            )

        # We cannot initialize the size and title now, because the subclass may not have done
        # the initialization to support this. So we require the subclass to call _final_canvas_init.
        self.__kwargs_for_later = dict(size=size, title=title)

    def _final_canvas_init(self):
        """Must be called by the subclasses at the end of their ``__init__``.

        This sets the canvas size and title, which must happen *after* the widget itself
        is initialized. Doing this automatically can be done with a metaclass, but let's keep it simple.
        """
        # Pop kwargs
        try:
            kwargs = self.__kwargs_for_later
        except AttributeError:
            return
        else:
            del self.__kwargs_for_later
        # Apply
        if not isinstance(self, WrapperRenderCanvas):
            self.set_logical_size(*kwargs["size"])
            self.set_title(kwargs["title"])

    def __del__(self):
        # On delete, we call the custom close method.
        try:
            self.close()
        except Exception:
            pass
        # Since this is sometimes used in a multiple inheritance, the
        # superclass may (or may not) have a __del__ method.
        try:
            super().__del__()
        except Exception:
            pass

    # %% Implement WgpuCanvasInterface

    _canvas_context = None  # set in get_context()

    def get_physical_size(self):
        """Get the physical size of the canvas in integer pixels."""
        return self._rc_get_physical_size()

    def get_context(self, context_type):
        """Get a context object that can be used to render to this canvas.

        The context takes care of presenting the rendered result to the canvas.
        Different types of contexts are available:

        * "wgpu": get a ``WgpuCanvasContext`` provided by the ``wgpu`` library.
        * "bitmap": get a ``BitmapRenderingContext`` provided by the ``rendercanvas`` library.
        * "another.module": other libraries may provide contexts too. We've only listed the ones we know of.
        * "your.module:ContextClass": Explicit name.

        Later calls to this method, with the same context_type argument, will return
        the same context instance as was returned the first time the method was
        invoked. It is not possible to get a different context object once the first
        one has been created.
        """

        # Note that this method is analog to HtmlCanvas.getContext(), except
        # the context_type is different, since contexts are provided by other projects.

        if not isinstance(context_type, str):
            raise TypeError("context_type must be str.")

        # Resolve the context type name
        known_types = {
            "wgpu": "wgpu",
            "bitmap": "rendercanvas.utils.bitmaprenderingcontext",
        }
        resolved_context_type = known_types.get(context_type, context_type)

        # Is the context already set?
        if self._canvas_context is not None:
            if resolved_context_type == self._canvas_context._context_type:
                return self._canvas_context
            else:
                raise RuntimeError(
                    f"Cannot get context for '{context_type}': a context of type '{self._canvas_context._context_type}' is already set."
                )

        # Load module
        module_name, _, class_name = resolved_context_type.partition(":")
        try:
            module = importlib.import_module(module_name)
        except ImportError as err:
            raise ValueError(
                f"Cannot get context for '{context_type}': {err}. Known valid values are {set(known_types)}"
            ) from None

        # Obtain factory to produce context
        factory_name = class_name or "rendercanvas_context_hook"
        try:
            factory_func = getattr(module, factory_name)
        except AttributeError:
            raise ValueError(
                f"Cannot get context for '{context_type}': could not find `{factory_name}` in '{module.__name__}'"
            ) from None

        # Create the context
        context = factory_func(self, self._rc_get_present_methods())

        # Quick checks to make sure the context has the correct API
        if not (hasattr(context, "canvas") and context.canvas is self):
            raise RuntimeError(
                "The context does not have a canvas attribute that refers to this canvas."
            )
        if not (hasattr(context, "present") and callable(context.present)):
            raise RuntimeError("The context does not have a present method.")

        # Done
        self._canvas_context = context
        self._canvas_context._context_type = resolved_context_type
        return self._canvas_context

    # %% Events

    def add_event_handler(self, *args, **kwargs):
        return self._events.add_handler(*args, **kwargs)

    def remove_event_handler(self, *args, **kwargs):
        return self._events.remove_handler(*args, **kwargs)

    def submit_event(self, event):
        # Not strictly necessary for normal use-cases, but this allows
        # the ._event to be an implementation detail to subclasses, and it
        # allows users to e.g. emulate events in tests.
        return self._events.submit(event)

    add_event_handler.__doc__ = EventEmitter.add_handler.__doc__
    remove_event_handler.__doc__ = EventEmitter.remove_handler.__doc__
    submit_event.__doc__ = EventEmitter.submit.__doc__

    # %% Scheduling and drawing

    def _process_events(self):
        """Process events and animations.

        Called from the scheduler.
        Subclasses *may* call this if the time between ``_rc_request_draw`` and the actual draw is relatively long.
        """

        # We don't want this to be called too often, because we want the
        # accumulative events to accumulate. Once per draw, and at max_fps
        # when there are no draws (in ondemand and manual mode).

        # Get events from the GUI into our event mechanism.
        loop = self._rc_get_loop()
        if loop:
            loop._rc_gui_poll()

        # Flush our events, so downstream code can update stuff.
        # Maybe that downstream code request a new draw.
        self._events.flush()

        # TODO: implement later (this is a start but is not tested)
        # Schedule animation events until the lag is gone
        # step = self._animation_step
        # self._animation_time = self._animation_time or time.perf_counter()  # start now
        # animation_iters = 0
        # while self._animation_time > time.perf_counter() - step:
        #     self._animation_time += step
        #     self._events.submit({"event_type": "animate", "step": step, "catch_up": 0})
        #     # Do the animations. This costs time.
        #     self._events.flush()
        #     # Abort when we cannot keep up
        #     # todo: test this
        #     animation_iters += 1
        #     if animation_iters > 20:
        #         n = (time.perf_counter() - self._animation_time) // step
        #         self._animation_time += step * n
        #         self._events.submit(
        #             {"event_type": "animate", "step": step * n, "catch_up": n}
        #         )

    def _draw_frame(self):
        """The method to call to draw a frame.

        Cen be overriden by subclassing, or by passing a callable to request_draw().
        """
        pass

    def request_draw(self, draw_function=None):
        """Schedule a new draw event.

        This function does not perform a draw directly, but schedules a draw at
        a suitable moment in time. At that time the draw function is called, and
        the resulting rendered image is presented to screen.

        Only affects drawing with schedule-mode 'ondemand'.

        Arguments:
            draw_function (callable or None): The function to set as the new draw
                function. If not given or None, the last set draw function is used.

        """
        if draw_function is not None:
            self._draw_frame = draw_function
        if self.__scheduler is not None:
            self.__scheduler.request_draw()

        # -> Note that the draw func is likely to hold a ref to the canvas. By
        #   storing it here, the gc can detect this case, and its fine. However,
        #   this fails if we'd store _draw_frame on the scheduler!

    def force_draw(self):
        """Perform a draw right now.

        In most cases you want to use ``request_draw()``. If you find yourself using
        this, consider using a timer. Nevertheless, sometimes you just want to force
        a draw right now.
        """
        if self.__is_drawing:
            raise RuntimeError("Cannot force a draw while drawing.")
        self._rc_force_draw()

    def _draw_frame_and_present(self):
        """Draw the frame and present the result.

        Errors are logged to the "rendercanvas" logger. Should be called by the
        subclass at its draw event.
        """

        # Re-entrent drawing is problematic. Let's actively prevent it.
        if self.__is_drawing:
            return
        self.__is_drawing = True

        try:
            # This method is called from the GUI layer. It can be called from a
            # "draw event" that we requested, or as part of a forced draw.

            # Cannot draw to a closed canvas.
            if self._rc_is_closed():
                return

            # Process special events
            # Note that we must not process normal events here, since these can do stuff
            # with the canvas (resize/close/etc) and most GUI systems don't like that.
            self._events.emit({"event_type": "before_draw"})

            # Notify the scheduler
            if self.__scheduler is not None:
                fps = self.__scheduler.on_draw()

                # Maybe update title
                if fps is not None:
                    self.__title_info["fps"] = f"{fps:0.1f}"
                    if "$fps" in self.__title_info["raw"]:
                        self.set_title(self.__title_info["raw"])

            # Perform the user-defined drawing code. When this errors,
            # we should report the error and then continue, otherwise we crash.
            with log_exception("Draw error"):
                self._draw_frame()
            with log_exception("Present error"):
                # Note: we use canvas._canvas_context, so that if the draw_frame is a stub we also dont trigger creating a context.
                # Note: if vsync is used, this call may wait a little (happens down at the level of the driver or OS)
                context = self._canvas_context
                if context:
                    result = context.present()
                    method = result.pop("method")
                    if method in ("skip", "screen"):
                        pass  # nothing we need to do
                    elif method == "fail":
                        raise RuntimeError(method.get("message", "") or "present error")
                    else:
                        # Pass the result to the literal present method
                        func = getattr(self, f"_rc_present_{method}")
                        func(**result)

        finally:
            self.__is_drawing = False

    # %% Primary canvas management methods

    def get_logical_size(self):
        """Get the logical size (width, height) in float pixels."""
        return self._rc_get_logical_size()

    def get_pixel_ratio(self):
        """Get the float ratio between logical and physical pixels."""
        return self._rc_get_pixel_ratio()

    def close(self):
        """Close the canvas."""
        self._rc_close()

    def is_closed(self):
        """Get whether the window is closed."""
        return self._rc_is_closed()

    # %% Secondary canvas management methods

    # These methods provide extra control over the canvas. Subclasses should
    # implement the methods they can, but these features are likely not critical.

    def set_logical_size(self, width, height):
        """Set the window size (in logical pixels)."""
        width, height = float(width), float(height)
        if width < 0 or height < 0:
            raise ValueError("Canvas width and height must not be negative")
        self._rc_set_logical_size(width, height)

    def set_title(self, title):
        """Set the window title."""
        self.__title_info["raw"] = title
        for k, v in self.__title_info.items():
            title = title.replace("$" + k, v)
        self._rc_set_title(title)

    # %% Methods for the subclass to implement

    def _rc_get_loop(self):
        """Get the loop instance for this backend.

        Must return the global loop instance (a BaseLoop subclass) for the canvas subclass,
        or None for a canvas without scheduled draws.
        """
        return None

    def _rc_get_present_methods(self):
        """Get info on the present methods supported by this canvas.

        Must return a small dict, used by the canvas-context to determine
        how the rendered result will be presented to the canvas.
        This method is only called once, when the context is created.

        Each supported method is represented by a field in the dict. The value
        is another dict with information specific to that present method.
        A canvas backend must implement at least either "screen" or "bitmap".

        With method "screen", the context will render directly to a surface
        representing the region on the screen. The sub-dict should have a ``window``
        field containing the window id. On Linux there should also be ``platform``
        field to distinguish between "wayland" and "x11", and a ``display`` field
        for the display id. This information is used by wgpu to obtain the required
        surface id.

        With method "bitmap", the context will present the result as an image
        bitmap. On GPU-based contexts, the result will first be rendered to an
        offscreen texture, and then downloaded to RAM. The sub-dict must have a
        field 'formats': a list of supported image formats. Examples are "rgba-u8"
        and "i-u8". A canvas must support at least "rgba-u8". Note that srgb mapping
        is assumed to be handled by the canvas.
        """
        raise NotImplementedError()

    def _rc_request_draw(self):
        """Request the GUI layer to perform a draw.

        Like requestAnimationFrame in JS. The draw must be performed
        by calling ``_draw_frame_and_present()``. It's the responsibility
        for the canvas subclass to make sure that a draw is made as
        soon as possible.

        Canvases that have a limit on how fast they can 'consume' frames, like
        remote frame buffers, do good to call self._process_events() when the
        draw had to wait a little. That way the user interaction will lag as
        little as possible.

        The default implementation does nothing, which is equivalent to waiting
        for a forced draw or a draw invoked by the GUI system.
        """
        pass

    def _rc_force_draw(self):
        """Perform a synchronous draw.

        When it returns, the draw must have been done.
        The default implementation just calls ``_draw_frame_and_present()``.
        """
        self._draw_frame_and_present()

    def _rc_present_bitmap(self, *, data, format, **kwargs):
        """Present the given image bitmap. Only used with present_method 'bitmap'.

        If a canvas supports special present methods, it will need to implement corresponding ``_rc_present_xx()`` methods.
        """
        raise NotImplementedError()

    def _rc_get_physical_size(self):
        """Get the physical size (with, height) in integer pixels."""
        raise NotImplementedError()

    def _rc_get_logical_size(self):
        """Get the logical size (with, height) in float pixels."""
        raise NotImplementedError()

    def _rc_get_pixel_ratio(self):
        """Get ratio between physical and logical size."""
        raise NotImplementedError()

    def _rc_set_logical_size(self, width, height):
        """Set the logical size. May be ignired when it makes no sense.

        The default implementation does nothing.
        """
        pass

    def _rc_close(self):
        """Close the canvas.

        For widgets that are wrapped by a ``WrapperRenderCanvas``, this should probably
        close the wrapper instead.

        Note that ``BaseRenderCanvas`` implements the ``close()`` method, which
        is a rather common name; it may be necessary to re-implement that too.
        """
        pass

    def _rc_is_closed(self):
        """Get whether the canvas is closed."""
        return False

    def _rc_set_title(self, title):
        """Set the canvas title. May be ignored when it makes no sense.

        For widgets that are wrapped by a ``WrapperRenderCanvas``, this should probably
        set the title of the wrapper instead.

        The default implementation does nothing.
        """
        pass


class WrapperRenderCanvas(BaseRenderCanvas):
    """A base render canvas for top-level windows that wrap a widget, as used in e.g. Qt and wx.

    This base class implements all the re-direction logic, so that the subclass does not have to.
    Subclasses should not implement any of the ``_rc_`` methods. Subclasses must instantiate the
    wrapped canvas and set it as ``_subwidget``.
    """

    def add_event_handler(self, *args, **kwargs):
        return self._subwidget._events.add_handler(*args, **kwargs)

    def remove_event_handler(self, *args, **kwargs):
        return self._subwidget._events.remove_handler(*args, **kwargs)

    def submit_event(self, event):
        return self._subwidget._events.submit(event)

    def get_context(self, *args, **kwargs):
        return self._subwidget.get_context(*args, **kwargs)

    def request_draw(self, *args, **kwargs):
        return self._subwidget.request_draw(*args, **kwargs)

    def force_draw(self):
        self._subwidget.force_draw()

    def get_physical_size(self):
        return self._subwidget.get_physical_size()

    def get_logical_size(self):
        return self._subwidget.get_logical_size()

    def get_pixel_ratio(self):
        return self._subwidget.get_pixel_ratio()

    def set_logical_size(self, width, height):
        self._subwidget.set_logical_size(width, height)

    def set_title(self, *args):
        self._subwidget.set_title(*args)

    def close(self):
        self._subwidget.close()

    def is_closed(self):
        return self._subwidget.is_closed()
