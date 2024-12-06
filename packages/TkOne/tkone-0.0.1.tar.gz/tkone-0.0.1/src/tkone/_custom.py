from typing import List, Union, Literal, Callable, overload, Dict, Any
from tkinter import ttk, Tk
from tkinter import *
from pathlib import Path

import customtkinter

def global_color_theme(theme: Union[Path, Literal["blue", "green", "dark-blue"]] = "green"):
    if isinstance(theme, Path):
        customtkinter.set_default_color_theme(theme.__str__())
    else:
        customtkinter.set_default_color_theme(theme)

def global_appearance_mode(mode: Literal["light", "dark", "system"] = "system"):
    customtkinter.set_appearance_mode(mode)

class Scroller:
    @overload
    def __init__(
        self,
        master: Union[customtkinter.CTkFrame, Frame, ttk.Frame, Tk, customtkinter.CTk, Toplevel, Misc],
        *,
        parent_callbacks: Union[Dict[str, Union[Callable, None]], None] = None,
        orientation: Literal['horizontal', 'vertical'] = 'vertical',
        pack_options: Dict[str, Any] = {'fill': BOTH, 'expand': True},
        **kwargs
    ) -> None: ...

    @overload
    def __init__(
        self,
        master: Union[customtkinter.CTkFrame, Frame, ttk.Frame, Tk, customtkinter.CTk, Toplevel, Misc],
        *,
        parent_callbacks: Union[Dict[str, Union[Callable, None]], None] = None,
        orientation: Literal['horizontal', 'vertical'] = 'vertical',
        place_options: Dict[str, Any] = {'relx': 0, 'rely': 0, 'relwidth': 1, 'relheight': 1},
        **kwargs
    ) -> None: ...

    @overload
    def __init__(
        self,
        master: Union[customtkinter.CTkFrame, Frame, ttk.Frame, Tk, customtkinter.CTk, Toplevel, Misc],
        *,
        parent_callbacks: Union[Dict[str, Union[Callable, None]], None] = None,
        orientation: Literal['horizontal', 'vertical'] = 'vertical',
        grid_options: Dict[str, Any] = {'sticky': NSEW},
        **kwargs
    ) -> None: ...

    def __init__(
        self,
        master: Union[customtkinter.CTkFrame, Frame, ttk.Frame, Tk, customtkinter.CTk, Toplevel, Misc],
        *,
        parent_callbacks: Union[Dict[str, Union[Callable, None]], None] = None,
        orientation: Literal['horizontal', 'vertical'] = 'vertical',
        **kwargs
    ) -> None:
        # Define parent and parent callbacks
        self.parent = master
        self.parent_callbacks = parent_callbacks

        # Define packing placeholders
        self.pack_options = None
        self.place_options = None
        self.grid_options = None

        # retrieve options from kwargs
        if 'pack_options' in kwargs:
            self.pack_options = kwargs.pop('pack_options')
        elif 'place_options' in kwargs:
            self.place_options = kwargs.pop('place_options')
        elif 'grid_options' in kwargs:
            self.grid_options = kwargs.pop('grid_options')

        # Define the scrollable frame with kwargs.
        self.scrollable = customtkinter.CTkScrollableFrame(master, orientation=orientation, **kwargs)

        # Pack the scrollable frame with the appropriate options
        if self.pack_options is not None:
            self.scrollable.pack(**self.pack_options)
        elif self.place_options is not None:
            self.scrollable.place(**self.place_options)
        elif self.grid_options is not None:
            self.scrollable.grid(**self.grid_options)
        
        # Bind events to the scrollable frame
        self.scrollable.bind_all('<Enter>', self._on_entry)
        self.scrollable.bind_all('<Leave>', self._on_leave)
    
    def _on_entry(self, event: Event) -> None:
        if self.parent_callbacks is not None:
            for binding in self.parent_callbacks.keys():
                if binding in ['<MouseWheel>', '<Button-4>', '<Button-5>']:
                    self.parent.unbind_all(binding)
            
        self.scrollable.bind_all('<MouseWheel>', self._on_mousewheel)
        self.scrollable.bind_all('<Button-4>', self._on_mousewheel)
        self.scrollable.bind_all('<Button-5>', self._on_mousewheel)

    def _on_leave(self, event: Event) -> None:
        self.scrollable.unbind_all('<MouseWheel>')
        self.scrollable.unbind_all('<Button-4>')
        self.scrollable.unbind_all('<Button-5>')
        if self.parent_callbacks is not None:
            for binding, callback in self.parent_callbacks.items():
                if binding in ['<MouseWheel>', '<Button-4>', '<Button-5>']:
                    if callback is not None:
                        self.parent.bind_all(sequence=binding, func=callback)

    def _on_mousewheel(self, event):
        # Get current scroll position
        current_pos = self.scrollable._parent_canvas.yview()
        
        # Handle different event types (Windows vs Linux)
        if event.num == 5 or event.delta < 0:
            move = 3  # Scroll down
        else:
            move = -3  # Scroll up
            
        # Only scroll if we're not at the boundaries
        if (move > 0 and current_pos[1] < 1) or (move < 0 and current_pos[0] > 0):
            self.scrollable._parent_canvas.yview_scroll(move, "units")
    
    @property
    def actual(self) -> customtkinter.CTkScrollableFrame:
        return self.scrollable

class Toolbar:
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
        if isinstance(master, Scroller):
            self.parent = master.actual
        else:
            self.parent = master
        
        self.orientation = orientation
        self.toolchain = customtkinter.CTkScrollableFrame(self.parent, orientation=orientation, height=height, **kwargs)
        self.tools: Dict[str, customtkinter.CTkButton] = {}
    
    @overload
    def register_tool(self, text: str, width: int = 140, height: int = 28, *, command: Callable) -> None: ...

    @overload
    def register_tool(self, text: str, width: int = 140, height: int = 28) -> Callable: ...

    def register_tool(self, text: str, width: int = 140, height: int = 28, *, command: Union[Callable, None] = None) -> Union[None, Callable]:
        if command is None and (self.register_tool.__defaults__ is None or len(self.register_tool.__defaults__) == 2):  # Called as decorator
            # Decorator usage
            def decorator(func: Callable) -> Callable:
                self.tools[text] = customtkinter.CTkButton(self.toolchain, text=text, hover_color='red', command=func, width=width, height=height)
                return func
            return decorator
        elif command is None:
            # explicit None
            raise ValueError('command cannot be None')
        else:
            # Direct registration
            self.tools[text] = customtkinter.CTkButton(self.toolchain, text=text, hover_color='white', command=command, width=width, height=height)
            return None
    
    def pack(
        self,
        expand: bool = True,
        fill: Literal['both', 'x', 'y', 'none'] = 'x',
        anchor: Literal['n', 'e', 's', 'w', 'ne', 'nw', 'se', 'sw', 'center'] = 'n',
        menu_side: Literal['top', 'bottom', 'left', 'right'] = 'left',
        menu_padx: int = 1,
        menu_pady: int = 3
    ) -> None:
        self.toolchain.pack(expand=expand, fill=fill, anchor=anchor)
        for tool in self.tools.values():
            tool.pack(side=menu_side, padx=menu_padx, pady=menu_pady)
    
    def bind_mousewheel(self, parent_callbacks: Union[Dict[str, Callable], None] = None) -> None:
        self.given_callbacks = parent_callbacks

        self.toolchain.bind('<Enter>', self.on_entry)
        self.toolchain.bind('<Leave>', self.on_leave)

        for child in self.toolchain.winfo_children():
            child.bind('<Enter>', self.on_entry)
            child.bind('<Leave>', self.on_leave)
    
    def on_entry(self, event: Event) -> None:
        if self.given_callbacks is not None:
            for binding, callback in self.given_callbacks.items():
                if binding in ['<MouseWheel>', '<Button-4>', '<Button-5>']:
                    self.parent.unbind_all(binding)
    
        self.toolchain.bind('<MouseWheel>', self.on_mousewheel)
        self.toolchain.bind('<Button-4>', self.on_mousewheel)
        self.toolchain.bind('<Button-5>', self.on_mousewheel)

        for child in self.toolchain.winfo_children():
            child.bind('<MouseWheel>', self.on_mousewheel)
            child.bind('<Button-4>', self.on_mousewheel)
            child.bind('<Button-5>', self.on_mousewheel)
    
    def on_leave(self, event: Event) -> None:
        self.toolchain.unbind('<MouseWheel>')
        self.toolchain.unbind('<Button-4>')
        self.toolchain.unbind('<Button-5>')

        for child in self.toolchain.winfo_children():
            child.unbind('<MouseWheel>')
            child.unbind('<Button-4>')
            child.unbind('<Button-5>')

        if self.given_callbacks is not None:
            for binding, callback in self.given_callbacks.items():
                if binding in ['<MouseWheel>', '<Button-4>', '<Button-5>']:
                    if callback is not None:
                        self.parent.bind_all(binding, callback)
    
    def on_mousewheel(self, event: Event) -> None:
        if self.orientation == 'vertical':
            current_pos = self.toolchain._parent_canvas.yview()
        else:
            current_pos = self.toolchain._parent_canvas.xview()

        if event.num == 5 or event.delta < 0:
            move = 3
        else:
            move = -3
        
        if (move > 0 and current_pos[1] < 1) or (move < 0 and current_pos[0] > 0):
            if self.orientation == 'vertical':
                self.toolchain._parent_canvas.yview_scroll(move, "units")
            else:
                self.toolchain._parent_canvas.xview_scroll(move, "units")
    
    @property
    def actual(self) -> customtkinter.CTkScrollableFrame:
        return self.toolchain

    def change_order(self, new_order: List[str]) -> None:
        for name in new_order:
            if name not in self.tools:
                raise ValueError(f"Tool '{name}' not found")
        
        for tool in self.tools.values():
            tool.pack_forget()
        
        self.tools = {name: self.tools[name] for name in new_order}
    
    @overload
    def replace_tool(self, old_name: str) -> Callable: ...
    @overload
    def replace_tool(self, old_name: str, new_tool: Callable) -> None: ...

    def replace_tool(self, old_name: str, new_tool: Union[Callable, None] = None) -> Union[None, Callable]:
        if old_name not in self.tools:
            raise ValueError(f"Tool '{old_name}' not found")
        
        if new_tool is None:  # Decorator usage
            def decorator(func: Callable) -> Callable:
                tool = self.tools.pop(old_name)
                tool.destroy()
                self.tools[old_name] = customtkinter.CTkButton(
                    self.toolchain, 
                    text=old_name, 
                    hover_color='red', 
                    command=func,
                    width=tool.cget('width'),
                    height=tool.cget('height')
                )
                return func
            return decorator
        else:  # Direct method call
            tool = self.tools.pop(old_name)
            tool.destroy()
            self.tools[old_name] = customtkinter.CTkButton(
                self.toolchain, 
                text=old_name, 
                hover_color='red', 
                command=new_tool,
                width=tool.cget('width'),
                height=tool.cget('height')
            )
            return None

class Page:
    _pages = {}  # Stores page class definitions
    _instances = {}  # Will store instantiated pages
    _current = None
    _container = None
    _footer = None
    _footer_height: int = 24

    def __init__(self, name: str):
        self.name = name

    def __call__(self, page_class: Callable) -> Callable:
        Page._pages[self.name] = page_class
        return page_class

    @classmethod
    def set_container(cls, container: Any) -> None:
        """Set the container where pages will be packed"""
        cls._container = container

    @staticmethod
    def footer(footer_class: Callable = None) -> Callable:
        """Decorator to set a footer that will be shown on all pages"""
        Page._footer = footer_class        
        return footer_class

    @classmethod
    def pack(cls, name: str) -> None:
        if name not in cls._pages:
            raise ValueError(f"Page '{name}' not found")
        
        if cls._container is None:
            raise RuntimeError("Container not set. Call Page.set_container() first")

        # Hide current page if exists
        if cls._current is not None:
            cls._current.pack_forget()

        # Create or retrieve page instance
        if name not in cls._instances:
            # First time creation
            frame = customtkinter.CTkFrame(cls._container)
            content_frame = customtkinter.CTkFrame(frame)
            page_instance = cls._pages[name](content_frame)
            content_frame.pack(fill=BOTH, expand=True)
            
            # Add footer if exists
            if cls._footer is not None:
                footer_frame = customtkinter.CTkFrame(frame, height=cls._footer_height)
                footer_instance = cls._footer(footer_frame)
                footer_frame.pack(fill=X)
            
            cls._instances[name] = frame
        
        # Show the page
        cls._instances[name].pack(fill=BOTH, expand=True)
        cls._current = cls._instances[name]

    @classmethod
    def forget(cls) -> None:
        """
        Remove the current page from view
        """
        if cls._current is not None:
            cls._current.pack_forget()
            cls._current = None

    @classmethod
    def update_footer(cls) -> None:
        """
        Recreate the footer on all existing page instances
        """
        if cls._footer is None:
            return

        for frame in cls._instances.values():
            # Remove existing footer (last child)
            children = frame.winfo_children()
            if len(children) > 1:  # Has footer
                children[-1].destroy()
            
            # Create new footer
            footer_frame = customtkinter.CTkFrame(frame, height=cls._footer_height)
            footer_instance = cls._footer(footer_frame)
            footer_frame.pack(fill=X)