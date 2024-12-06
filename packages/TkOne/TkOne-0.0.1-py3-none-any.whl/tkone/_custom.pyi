"""(Tkinter - CustomTkinter) derivatives

This module contains custom classes that extend,
improve and improvises the default behaviours of
the Tkinter and CustomTkinter classes.

Following is the list of classes that are
derived from the Tkinter and CustomTkinter classes:

- Scroller
- Toolbar
- Page
"""

from typing import List, Union, Literal, Callable, overload, Dict, Any
from tkinter import ttk, Tk
from tkinter import *
from pathlib import Path

import customtkinter

def global_color_theme(theme: Union[Path, Literal["blue", "green", "dark-blue"]] = "green"):
    """Set the global color theme for widgets."""
    ...
def global_appearance_mode(mode: Literal["light", "dark", "system"] = "system"):
    """Set the global appearance mode for widgets."""
    ...

class Scroller:
    """Create a Scrollable Feed with mouse wheel support."""

    @overload
    def __init__(
        self,
        master: Union[

            # Base
            Misc,
            Widget,

            # tkinter Base
            Tk,
            Toplevel,
            Frame,
            Canvas,

            # tkinter.ttk
            ttk.Notebook,
            ttk.Frame,

            # customtkinter classes
            customtkinter.CTkFrame,
            customtkinter.CTk,
            customtkinter.CTkCanvas,
            customtkinter.CTkScrollableFrame,
            customtkinter.CTkTabview,
            customtkinter.CTkToplevel,

            # Any
            Any
        ] = Tk(),
        *,
        parent_callbacks: Union[Dict[str, Union[Callable, None]], None] = None,
        orientation: Literal['horizontal', 'vertical'] = 'vertical',
        pack_options: Union[Dict[str, Any], None] = None,
        **kwargs
    ) -> None:
        """Create a Scroller object and pack it using the `pack` geometry manager.
        
        #### parameter description

        ------------------------------------------------------------------------------------------------

        `master` can be any Tk or Toplevel widget. Apart from that, it can be any tkinter.Frame or ttk.Frame.
        It also supports `customtkinter` widgets. It can be `customtkinter.CTk` or `customtkinter.CTkFrame`.
        Other than that it can be any other widget (Note: This can be problematic in most cases but provided
        for further customisation if applicable).

        ------------------------------------------------------------------------------------------------

        `parent_callbacks` is a dictionary containing the bindings for the parent widget(if any).
        This is mainly for `<MouseWheel>`, `<Button-4>`, `<Button-5>` bindings. In case the parent is 
        bound to these events, it will hinder the scrolling of the `Scroller` object. Therefore, set the
        `parent_callbacks` dictionary properly.

        Demo `parent_callbacks` dictionary:
        ```python
        parent_callbacks = {
            "<MouseWheel>": <function>,
            "<Button-4>": None,
            "<Button-5>": <function>,
        }
        ```

        Here, `<function>` is the function that will be called when the event occurs.
        If the event is not bound, set it to `None` or do not add the entry to the dictionary.

        ------------------------------------------------------------------------------------------------

        `orientation` can be either `horizontal` or `vertical`.

        ------------------------------------------------------------------------------------------------

        `pack_options` is a dictionary containing the options to be passed to the `pack` method. The default
        values are `{'fill': BOTH, 'expand': True}` and these values are mandatory. Keep the default values and
        add any additional options if needed. Or experiment as you wish.

        ### You need to explicitly set this parameter since this is an overloaded method.

        ------------------------------------------------------------------------------------------------

        Apart from the above parameters, pass any valid keyword parameters for the `Scrollable Frame`.
        
        Valid Keyword Parameters for `Scrollable Frame` and their default values:

        - `width`: int = 100
        - `height`: int = 100
        - `corner_radius`: int | str | None = None
        - `border_width`: int | str | None = None
        - `bg_color`: str | Tuple[str, str] = "transparent"
        - `fg_color`: str | Tuple[str, str] | None = None
        - `border_color`: str | Tuple[str, str] | None = None
        - `scrollbar_fg_color`: str | Tuple[str, str] | None = None
        - `scrollbar_button_color`: str | Tuple[str, str] | None = None
        - `scrollbar_button_hover_color`: str | Tuple[str, str] | None = None
        - `label_text`: str = ""
        - `label_text_color`: str | Tuple[str, str] | None = None
        - `label_fg_color`: str | Tuple[str, str] | None = None
        - `label_font`: tuple | customtkinter.CTkFont | None = None
        - `label_anchor`: str = "center"

        ------------------------------------------------------------------------------------------------

        #### Ideal Usage

        The ideal usage of `Scroller` is when used with `tk.Tk()` or `customtkinter.CTk()`. However,
        it can be used with any frame. (`tkinter.Frame`, `ttk.Frame`, `customtkinter.CTkFrame`).

        ```python
        >>> from tkinter import Tk
        >>> some_app = Tk()
        >>> scroller = Scroller(some_app)
        >>> some_app.mainloop()
        ```

        ------------------------------------------------------------------------------------------------

        #### Detailed Usage Implementation

        ```python
        from tkinter import Tk
        from tkone import Scroller
        from typing import Union

        class App:
            def __init__(self, master: Union[Tk, Toplevel] = Tk()):
                # set master
                self.master = master

                # suppose we want to bind the `<MouseWheel>`
                # event to the root. for some reason.
                # I am showing this just to make you understand
                # the `parent_callbacks` parameter. It may not
                # be Tk() directly and could be Canvas or other
                # widgets or as simple as a Frame.
                self.master.bind("<MouseWheel>", self.on_mousewheel)

                # create scroller inside the root.
                self.scroller = Scroller(
                    self.master,
                    parent_callbacks={"<MouseWheel>": self.on_mousewheel},
                    pack_options={"fill": BOTH, "expand": True, "padx": 10, "pady": 10}
                )
                # Note that pack_options key:value
                # pair -> {"fill": BOTH, "expand": True}
                # is mandatory and we can only add more
                # key:value pairs to it. such as
                # padx, pady, sticky, etc.

                # Now we can use the scroller object to pack
                # our widgets. Remember Scroller is just a class
                # and to pack widgets we need to use the
                # `Scroller.actual` attribute.

                # let us create a label and a button and pack
                # them inside the scroller.
                self.label = Label(self.scroller.actual, text="Hello, World!")
                self.button = Button(self.scroller.actual, text="Click Me")

                self.label.pack()
                self.button.pack()

                # NOTE: If you are using the `tkone.Builder`
                # class, you can easily manage the above
                # operations in one line.

                # let us create some more widgets and pack
                # them inside the scroller.
                
                self.entry = Builder.add_ttk_entry(
                    master=self.scroller.actual,
                    *args,
                    **kwargs
                )
                # see the Builder class for more information
                # on the parameters.
            
            def on_mousewheel(self, event: Event):
                \"""Handle the `<MouseWheel>` event.\"""
                ...
            
            @property
            def mainloop(self):
                self.master.mainloop()

            # Other Methods go here...
        
        if __name__ == "__main__":
            app = App()
            app.mainloop
        ```
        """
        ...
    
    @overload
    def __init__(
        self,
        master: Union[

            # Base
            Misc,
            Widget,

            # tkinter Base
            Tk,
            Toplevel,
            Frame,
            Canvas,

            # tkinter.ttk
            ttk.Notebook,
            ttk.Frame,

            # customtkinter classes
            customtkinter.CTkFrame,
            customtkinter.CTk,
            customtkinter.CTkCanvas,
            customtkinter.CTkScrollableFrame,
            customtkinter.CTkTabview,
            customtkinter.CTkToplevel,

            # Any
            Any
        ] = Tk(),
        *,
        parent_callbacks: Union[Dict[str, Union[Callable, None]], None] = None,
        orientation: Literal['horizontal', 'vertical'] = 'vertical',
        place_options: Union[Dict[str, Any], None] = None,
        **kwargs
    ) -> None:
        """Create a Scroller object and place it using the `place` geometry manager.
        
        #### parameter description

        ------------------------------------------------------------------------------------------------

        `master` can be any Tk or Toplevel widget. Apart from that, it can be any tkinter.Frame or ttk.Frame.
        It also supports `customtkinter` widgets. It can be `customtkinter.CTk` or `customtkinter.CTkFrame`.
        Other than that it can be any other widget (Note: This can be problematic in most cases but provided
        for further customisation if applicable).

        ------------------------------------------------------------------------------------------------

        `parent_callbacks` is a dictionary containing the bindings for the parent widget(if any).
        This is mainly for `<MouseWheel>`, `<Button-4>`, `<Button-5>` bindings. In case the parent is 
        bound to these events, it will hinder the scrolling of the `Scroller` object. Therefore, set the
        `parent_callbacks` dictionary properly.

        Demo `parent_callbacks` dictionary:
        ```python
        parent_callbacks = {
            "<MouseWheel>": <function>,
            "<Button-4>": None,
            "<Button-5>": <function>,
        }
        ```

        Here, `<function>` is the function that will be called when the event occurs.
        If the event is not bound, set it to `None` or do not add the entry to the dictionary.

        ------------------------------------------------------------------------------------------------

        `orientation` can be either `horizontal` or `vertical`.

        ------------------------------------------------------------------------------------------------

        `place_options` is a dictionary containing the options to be passed to the `place` method. The default
        values are `{'relx': 0, 'rely': 0, 'relwidth': 1, 'relheight': 1}` and these values are mandatory. Keep the
        default values and add any additional options if needed. Or experiment as you wish.

        ### You need to explicitly set this parameter since this is an overloaded method.

        ------------------------------------------------------------------------------------------------

        Apart from the above parameters, pass any valid keyword parameters for the `Scrollable Frame`.
        
        Valid Keyword Parameters for `Scrollable Frame` and their default values:

        - `width`: int = 100
        - `height`: int = 100
        - `corner_radius`: int | str | None = None
        - `border_width`: int | str | None = None
        - `bg_color`: str | Tuple[str, str] = "transparent"
        - `fg_color`: str | Tuple[str, str] | None = None
        - `border_color`: str | Tuple[str, str] | None = None
        - `scrollbar_fg_color`: str | Tuple[str, str] | None = None
        - `scrollbar_button_color`: str | Tuple[str, str] | None = None
        - `scrollbar_button_hover_color`: str | Tuple[str, str] | None = None
        - `label_text`: str = ""
        - `label_text_color`: str | Tuple[str, str] | None = None
        - `label_fg_color`: str | Tuple[str, str] | None = None
        - `label_font`: tuple | customtkinter.CTkFont | None = None
        - `label_anchor`: str = "center"

        ------------------------------------------------------------------------------------------------

        #### Ideal Usage

        The ideal usage of `Scroller` is when used with `tk.Tk()` or `customtkinter.CTk()`. However,
        it can be used with any frame. (`tkinter.Frame`, `ttk.Frame`, `customtkinter.CTkFrame`).

        ```python
        >>> from tkinter import Tk
        >>> some_app = Tk()
        >>> scroller = Scroller(some_app)
        >>> some_app.mainloop()
        ```

        ------------------------------------------------------------------------------------------------

        #### Detailed Usage Implementation

        ```python
        from tkinter import Tk
        from tkone import Scroller
        from typing import Union

        class App:
            def __init__(self, master: Union[Tk, Toplevel] = Tk()):
                # set master
                self.master = master

                # suppose we want to bind the `<MouseWheel>`
                # event to the root. for some reason.
                # I am showing this just to make you understand
                # the `parent_callbacks` parameter. It may not
                # be Tk() directly and could be Canvas or other
                # widgets or as simple as a Frame.
                self.master.bind("<MouseWheel>", self.on_mousewheel)

                # create scroller inside the root.
                self.scroller = Scroller(
                    self.master,
                    parent_callbacks={"<MouseWheel>": self.on_mousewheel},
                    place_options={"relx": 0, "rely": 0, "relwidth": 1, "relheight": 1, "padx": 10, "pady": 10}
                )
                # Note that place_options key:value
                # pair -> {"relx": 0, "rely": 0, "relwidth": 1, "relheight": 1}
                # is mandatory and we can only add more
                # key:value pairs to it. such as
                # padx, pady, sticky, etc.

                # Now we can use the scroller object to place
                # our widgets. Remember Scroller is just a class
                # and to place widgets we need to use the
                # `Scroller.actual` attribute.

                # let us create a label and a button and pack
                # them inside the scroller.
                self.label = Label(self.scroller.actual, text="Hello, World!")
                self.button = Button(self.scroller.actual, text="Click Me")

                self.label.pack()
                self.button.pack()

                # NOTE: If you are using the `tkone.Builder`
                # class, you can easily manage the above
                # operations in one line.

                # let us create some more widgets and pack
                # them inside the scroller.
                
                self.entry = Builder.add_ttk_entry(
                    master=self.scroller.actual,
                    *args,
                    **kwargs
                )
                # see the Builder class for more information
                # on the parameters.
            
            def on_mousewheel(self, event: Event):
                \"""Handle the `<MouseWheel>` event.\"""
                ...
            
            @property
            def mainloop(self):
                self.master.mainloop()

            # Other Methods go here...
        
        if __name__ == "__main__":
            app = App()
            app.mainloop
        ```
        """
        ...
    
    @overload
    def __init__(
        self,
        master: Union[

            # Base
            Misc,
            Widget,

            # tkinter Base
            Tk,
            Toplevel,
            Frame,
            Canvas,

            # tkinter.ttk
            ttk.Notebook,
            ttk.Frame,

            # customtkinter classes
            customtkinter.CTkFrame,
            customtkinter.CTk,
            customtkinter.CTkCanvas,
            customtkinter.CTkScrollableFrame,
            customtkinter.CTkTabview,
            customtkinter.CTkToplevel,

            # Any
            Any
        ] = Tk(),
        *,
        parent_callbacks: Union[Dict[str, Union[Callable, None]], None] = None,
        orientation: Literal['horizontal', 'vertical'] = 'vertical',
        grid_options: Union[Dict[str, Any], None] = None,
        **kwargs
    ) -> None:
        """Create a Scroller object and grid it using the `grid` geometry manager.
        
        #### parameter description

        ------------------------------------------------------------------------------------------------

        `master` can be any Tk or Toplevel widget. Apart from that, it can be any tkinter.Frame or ttk.Frame.
        It also supports `customtkinter` widgets. It can be `customtkinter.CTk` or `customtkinter.CTkFrame`.
        Other than that it can be any other widget (Note: This can be problematic in most cases but provided
        for further customisation if applicable).

        ------------------------------------------------------------------------------------------------

        `parent_callbacks` is a dictionary containing the bindings for the parent widget(if any).
        This is mainly for `<MouseWheel>`, `<Button-4>`, `<Button-5>` bindings. In case the parent is 
        bound to these events, it will hinder the scrolling of the `Scroller` object. Therefore, set the
        `parent_callbacks` dictionary properly.

        Demo `parent_callbacks` dictionary:
        ```python
        parent_callbacks = {
            "<MouseWheel>": <function>,
            "<Button-4>": None,
            "<Button-5>": <function>,
        }
        ```

        Here, `<function>` is the function that will be called when the event occurs.
        If the event is not bound, set it to `None` or do not add the entry to the dictionary.

        ------------------------------------------------------------------------------------------------

        `orientation` can be either `horizontal` or `vertical`.

        ------------------------------------------------------------------------------------------------

        `grid_options` is a dictionary containing the options to be passed to the `grid` method. The default
        values are `{'sticky': NSEW}` and these values are mandatory. Keep the default values and add any
        additional options if needed. Or experiment as you wish.

        ### You need to explicitly set this parameter since this is an overloaded method.

        ------------------------------------------------------------------------------------------------

        Apart from the above parameters, pass any valid keyword parameters for the `Scrollable Frame`.
        
        Valid Keyword Parameters for `Scrollable Frame` and their default values:

        - `width`: int = 100
        - `height`: int = 100
        - `corner_radius`: int | str | None = None
        - `border_width`: int | str | None = None
        - `bg_color`: str | Tuple[str, str] = "transparent"
        - `fg_color`: str | Tuple[str, str] | None = None
        - `border_color`: str | Tuple[str, str] | None = None
        - `scrollbar_fg_color`: str | Tuple[str, str] | None = None
        - `scrollbar_button_color`: str | Tuple[str, str] | None = None
        - `scrollbar_button_hover_color`: str | Tuple[str, str] | None = None
        - `label_text`: str = ""
        - `label_text_color`: str | Tuple[str, str] | None = None
        - `label_fg_color`: str | Tuple[str, str] | None = None
        - `label_font`: tuple | customtkinter.CTkFont | None = None
        - `label_anchor`: str = "center"

        ------------------------------------------------------------------------------------------------

        #### Ideal Usage

        The ideal usage of `Scroller` is when used with `tk.Tk()` or `customtkinter.CTk()`. However,
        it can be used with any frame. (`tkinter.Frame`, `ttk.Frame`, `customtkinter.CTkFrame`).

        ```python
        >>> from tkinter import Tk
        >>> some_app = Tk()
        >>> scroller = Scroller(some_app)
        >>> some_app.mainloop()
        ```

        ------------------------------------------------------------------------------------------------

        #### Detailed Usage Implementation

        ```python
        from tkinter import Tk
        from tkone import Scroller
        from typing import Union

        class App:
            def __init__(self, master: Union[Tk, Toplevel] = Tk()):
                # set master
                self.master = master

                # suppose we want to bind the `<MouseWheel>`
                # event to the root. for some reason.
                # I am showing this just to make you understand
                # the `parent_callbacks` parameter. It may not
                # be Tk() directly and could be Canvas or other
                # widgets or as simple as a Frame.
                self.master.bind("<MouseWheel>", self.on_mousewheel)

                # create scroller inside the root.
                self.scroller = Scroller(
                    self.master,
                    parent_callbacks={"<MouseWheel>": self.on_mousewheel},
                    grid_options={"sticky": NSEW, "padx": 10, "pady": 10}
                )
                # Note that grid_options key:value
                # pair -> {"sticky": NSEW}
                # is mandatory and we can only add more
                # key:value pairs to it. such as
                # padx, pady, sticky, etc.

                # Now we can use the scroller object to grid
                # our widgets. Remember Scroller is just a class
                # and to grid widgets we need to use the
                # `Scroller.actual` attribute.

                # let us create a label and a button and pack
                # them inside the scroller.
                self.label = Label(self.scroller.actual, text="Hello, World!")
                self.button = Button(self.scroller.actual, text="Click Me")

                self.label.pack()
                self.button.pack()

                # NOTE: If you are using the `tkone.Builder`
                # class, you can easily manage the above
                # operations in one line.

                # let us create some more widgets and pack
                # them inside the scroller.
                
                self.entry = Builder.add_ttk_entry(
                    master=self.scroller.actual,
                    *args,
                    **kwargs
                )
                # see the Builder class for more information
                # on the parameters.
            
            def on_mousewheel(self, event: Event):
                \"""Handle the `<MouseWheel>` event.\"""
                ...
            
            @property
            def mainloop(self):
                self.master.mainloop()

            # Other Methods go here...
        
        if __name__ == "__main__":
            app = App()
            app.mainloop
        ```
        """
        ...
    
    def _on_entry(self, event: Event) -> None:
        """<Enter> event handler."""
        ...
    
    def _on_leave(self, event: Event) -> None:
        """<Leave> event handler."""
        ...
    
    def _on_mousewheel(self, event: Event) -> None:
        """Mouse Wheel event handler."""
        ...

    @property
    def actual(self) -> customtkinter.CTkScrollableFrame:
        """Scroller inner object.
        
        An object to use as a parent to create widgets inside the `Scroller`.
        """
        ...

class Toolbar:
    """Create a Toolbar with mouse wheel support and customizable buttons."""

    def __init__(
        self,
        master: Union[
            # Base
            Misc,
            Widget,

            # tkinter Base
            Tk,
            Toplevel,
            Frame,
            Canvas,

            # tkinter.ttk
            ttk.Frame,
            ttk.Notebook,


            # customtkinter classes
            customtkinter.CTkFrame,
            customtkinter.CTk,
            customtkinter.CTkCanvas,
            customtkinter.CTkScrollableFrame,
            customtkinter.CTkTabview,
            customtkinter.CTkToplevel,

            # Derived
            Scroller,
        ],
        orientation: Literal['horizontal', 'vertical'] = 'horizontal',
        *,
        height: int = 30,
        **kwargs
    ) -> None:
        """Create a Toolbar with buttons in it for navigation.
        (with mouse wheel support and parent event collision handling)
        
        #### parameter description

        ------------------------------------------------------------------------------------------------

        `master` can be any Tk or Toplevel widget. Apart from that, it can be any tkinter.Frame or ttk.Frame.
        It also supports `customtkinter` widgets. It can be `customtkinter.CTk` or `customtkinter.CTkFrame`.
        Other than that it can be any other widget (Note: This can be problematic in most cases but provided
        for further customisation if applicable).

        ------------------------------------------------------------------------------------------------

        `orientation` can be either `horizontal` or `vertical`. Default is `horizontal`.

        ------------------------------------------------------------------------------------------------

        `height` is the height of the `Toolbar`. Default is `30`.

        ------------------------------------------------------------------------------------------------

        Apart from the above parameters, pass any valid keyword parameters for the `Scrollable Frame`.

        Valid Keyword Parameters for `Scrollable Frame` and their default values:

        - `width`: int = 100
        - `height`: int = 100
        - `corner_radius`: int | str | None = None
        - `border_width`: int | str | None = None
        - `bg_color`: str | Tuple[str, str] = "transparent"
        - `fg_color`: str | Tuple[str, str] | None = None
        - `border_color`: str | Tuple[str, str] | None = None
        - `scrollbar_fg_color`: str | Tuple[str, str] | None = None
        - `scrollbar_button_color`: str | Tuple[str, str] | None = None
        - `scrollbar_button_hover_color`: str | Tuple[str, str] | None = None
        - `label_text`: str = ""
        - `label_text_color`: str | Tuple[str, str] | None = None
        - `label_fg_color`: str | Tuple[str, str] | None = None
        - `label_font`: tuple | customtkinter.CTkFont | None = None
        - `label_anchor`: str = "center"

        ------------------------------------------------------------------------------------------------
        """
        ...
    
    @overload
    def register_tool(
        self,
        text: str,
        width: int = 140,
        height: int = 28,
        *,
        command: Callable
    ) -> None:
        """Register a tool with a command. This is a method and needs to be called as a method.
        Check before using, as there is a decorator counterpart.

        #### parameter description

        ------------------------------------------------------------------------------------------------

        `text`: str = The text to be displayed on the tool (button).

        ------------------------------------------------------------------------------------------------

        `width`: int = The width of the tool (button). Default is `140`.

        ------------------------------------------------------------------------------------------------

        `height`: int = The height of the tool (button). Default is `28`.

        ------------------------------------------------------------------------------------------------

        `command`: Callable = The command to be executed when the tool (button) is clicked.

        """
        ...
    
    @overload
    def register_tool(
        self,
        text: str,
        width: int = 140,
        height: int = 28,
    ) -> Callable:
        """Register a tool with a command. This is a decorator and needs to be used as a decorator.
        Check before using, as there is a method counterpart.

        #### parameter description

        ------------------------------------------------------------------------------------------------

        `text`: str = The text to be displayed on the tool (button).

        ------------------------------------------------------------------------------------------------

        `width`: int = The width of the tool (button). Default is `140`.

        ------------------------------------------------------------------------------------------------

        `height`: int = The height of the tool (button). Default is `28`.

        ------------------------------------------------------------------------------------------------

        #### Usage

        ```python
        from tkone import Toolbar
        from tkinter import Tk

        app = Tk()
        toolbar = Toolbar(app)
        toolbar.register_tool(text="Button 1")
        app.mainloop()
        ```

        -------------------------------------------OR-----------------------------------------------------

        ```python
        from tkone import Toolbar
        from tkinter import Tk

        app = Tk()
        toolbar = Toolbar(app)

        @toolbar.register_tool(text="Button 1")
        def on_button_1_click():
            print("Button 1 clicked")
        
        app.mainloop()
        ```
        """
        ...
    
    def bind_mousewheel(
        self,
        parent_callbacks: Union[Dict[str, Callable], None] = None
    ) -> None:
        """Bind the mouse wheel to the Toolbar.
        
        #### parameter description

        ------------------------------------------------------------------------------------------------

        `parent_callbacks`: Union[Dict[str, Callable], None] = A dictionary containing the bindings for the parent widget(if any).
        This is mainly for `<MouseWheel>`, `<Button-4>`, `<Button-5>` bindings. In case the parent is
        bound to these events, it will hinder the scrolling of the `Toolbar` object. Therefore, set the
        `parent_callbacks` dictionary properly.
        """
        ...
    
    def on_entry(self, event: Event) -> None:
        """<Enter> event handler."""
        ...
    
    def on_leave(self, event: Event) -> None:
        """<Leave> event handler."""
        ...
    
    def on_mousewheel(self, event: Event) -> None:
        """Mouse Wheel event handler."""
        ...

    @property
    def actual(self) -> customtkinter.CTkFrame:
        """Toolbar inner object.
        
        An object to use as a parent to create widgets inside the `Toolbar`.

        NOT RECOMMENDED TO USE.
        """
        ...

    def pack(
        self,
        expand: bool = True,
        fill: Literal['both', 'x', 'y', 'none'] = 'x',
        anchor: Literal['n', 'e', 's', 'w', 'ne', 'nw', 'se', 'sw', 'center'] = 'n',
        menu_side: Literal['top', 'bottom', 'left', 'right'] = 'left',
        menu_padx: int = 1,
        menu_pady: int = 3
    ) -> None:
        """Pack the Toolbar. With Default values, gets packed at the top."""
        ...

    def change_order(self, new_order: List[str]) -> None:
        """Change the order of the tools in the Toolbar.
        
        You will have to call `pack()` again after changing the order.
        """
        ...
    
    @overload
    def replace_tool(self, old_name: str) -> Callable:
        """Replace old function with a new function
        
        Use this as a decorator over a function.
        """
        ...

    @overload
    def replace_tool(self, old_name: str, new_tool: Callable) -> None:
        """Replace old function with a new function
        
        Use this as a forced method call.
        """
        ...

class Page:
    """`Pages for your gui application.`

    ------------------------------------------------------------------------------------------------
    
    #### Intermediate Usage Example

    This is just an example, you do not need to use `Toolbar` to use `Page`.
    Just call the `Page.pack()` method with the page name to make the
    mentioned page visible or current.

    ```python
    from tkone import Page
    from tkone import Toolbar
    from tkinter import Tk

    # create the Pages
    @Page("Home")
    class Home:
        def __init__(self, master: Any):
            ...
    
    @Page("Page 2")
    class Page2:
        def __init__(self, master: Any):
            ...

    # the main application class
    class App:
        def __init__(self, master: Tk = Tk()):
            
            # set the master
            self.master = master

            # create a toolbar at the top with buttons for navigation
            self.toolbar = Toolbar(self.master)

            # set page container
            Page.set_container(self.master)

            # create page handlers for the toolbar buttons
            @self.toolbar.register_tool(text="Home")
            def on_home_click():
                Page.pack("Home")
            
            @self.toolbar.register_tool(text="Page 2")
            def on_page_2_click():
                Page.pack("Page 2")
            
            # pack the toolbar
            self.toolbar.pack()
        
    # run the application
    if __name__ == "__main__":
        app = App()
        app.master.mainloop()
    ```
    """

    _pages: Dict[str, Callable] = {}
    _current: Union[Any, None] = None
    _container: Union[customtkinter.CTkFrame, None] = None
    _footer: Union[customtkinter.CTkFrame, None] = None
    _footer_height: int = 24

    def __init__(self, name: str) -> None:
        """
        #### Intermediate Usage Example

        This is just an example, you do not need to use `Toolbar` to use `Page`.
        Just call the `Page.pack()` method with the page name to make the
        mentioned page visible or current.

        ```python
        from tkone import Page
        from tkone import Toolbar
        from tkinter import Tk

        # create the Pages
        @Page("Home")
        class Home:
            def __init__(self, master: Any):
                ...
        
        @Page("Page 2")
        class Page2:
            def __init__(self, master: Any):
                ...

        # the main application class
        class App:
            def __init__(self, master: Tk = Tk()):
                
                # set the master
                self.master = master

                # create a toolbar at the top with buttons for navigation
                self.toolbar = Toolbar(self.master)

                # set page container
                Page.set_container(self.master)

                # create page handlers for the toolbar buttons
                @self.toolbar.register_tool(text="Home")
                def on_home_click():
                    Page.pack("Home")
                
                @self.toolbar.register_tool(text="Page 2")
                def on_page_2_click():
                    Page.pack("Page 2")
                
                # pack the toolbar
                self.toolbar.pack()
        
        # run the application
        if __name__ == "__main__":
            app = App()
            app.master.mainloop()
        ```
        """
        ...

    def __call__(self, page_class: Callable) -> Callable:
        """
        #### Intermediate Usage Example

        This is just an example, you do not need to use `Toolbar` to use `Page`.
        Just call the `Page.pack()` method with the page name to make the
        mentioned page visible or current.

        ```python
        from tkone import Page
        from tkone import Toolbar
        from tkinter import Tk

        # create the Pages
        @Page("Home")
        class Home:
            def __init__(self, master: Any):
                ...
        
        @Page("Page 2")
        class Page2:
            def __init__(self, master: Any):
                ...

        # the main application class
        class App:
            def __init__(self, master: Tk = Tk()):
                
                # set the master
                self.master = master

                # create a toolbar at the top with buttons for navigation
                self.toolbar = Toolbar(self.master)

                # set page container
                Page.set_container(self.master)

                # create page handlers for the toolbar buttons
                @self.toolbar.register_tool(text="Home")
                def on_home_click():
                    Page.pack("Home")
                
                @self.toolbar.register_tool(text="Page 2")
                def on_page_2_click():
                    Page.pack("Page 2")
                
                # pack the toolbar
                self.toolbar.pack()
        
        # run the application
        if __name__ == "__main__":
            app = App()
            app.master.mainloop()
        ```
        """
        ...

    @classmethod
    def set_container(cls, container: Union[Misc, Widget, Any]) -> None:
        """Set the container where pages will be packed.
        
        Basically the root or the parent widget.
        """
        ...
    
    @classmethod
    def footer(cls, footer_class: Callable = None) -> Callable:
        """Decorator to set a footer that will be shown on all pages"""
        ...
    
    @classmethod
    def pack(cls, name: str) -> None:
        """Pack the page with the given name and set it as the current page."""
        ...
    
    @classmethod
    def forget(cls) -> None:
        """Forget the current page."""
        ...

    @classmethod
    def update_footer(cls) -> None:
        """Update the footer on all existing page instances."""
        ...
