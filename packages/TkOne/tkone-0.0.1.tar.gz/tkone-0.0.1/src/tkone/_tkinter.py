from tkinter import *
from tkinter import ttk
from tkinter import Tk
from tkinter import Misc

from typing import Union, Literal, Any, Tuple, Dict, Mapping

class TkinterBuilder:
    def __init__(self, master: Union[Misc, None] = None) -> None:
        self.master = master

    @staticmethod
    def create_tk_root(
        screenName: Union[str, None] = None,
        baseName: Union[str, None] = None,
        className: str = "Tk",
        useTk: bool = True,
        sync: bool = False,
        use: Union[str, None] = None,
    ) -> Tk:
        return Tk(screenName=screenName, baseName=baseName, className=className, useTk=useTk, sync=sync, use=use)

    def create_ttk_frame_with_master(
        self,
        geometry_manager: Literal["grid", "place", "pack"] = "grid",
        geometry_manager_cnf: Union[Mapping[str, Any], None]  = {},
        geometry_manager_kwargs: Dict[str, Any] = {},
        **kwargs
    ) -> ttk.Frame:
        frame = ttk.Frame(self.master, **kwargs)
        if geometry_manager == "grid":
            frame.grid(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "place":
            frame.place(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "pack":
            frame.pack(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        
        return frame
    
    def create_frame_with_master(
        self,
        cnf: Union[Dict[str, Any], None] = {},
        geometry_manager: Literal["grid", "place", "pack"] = "grid",
        geometry_manager_cnf: Union[Mapping[str, Any], None] = {},
        geometry_manager_kwargs: Dict[str, Any] = {},
        **kwargs
    ) -> Frame:
        frame = Frame(self.master, cnf, **kwargs)
        if geometry_manager == "grid":
            frame.grid(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "place":
            frame.place(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "pack":
            frame.pack(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        return frame

    @staticmethod
    def create_ttk_frame(
        self,
        master: Union[Misc, None] = None,
        geometry_manager: Literal["grid", "place", "pack"] = "grid",
        geometry_manager_cnf: Union[Mapping[str, Any], None] = {},
        geometry_manager_kwargs: Dict[str, Any] = {},
        **kwargs
    ) -> ttk.Frame:
        frame = ttk.Frame(master, **kwargs)
        if geometry_manager == "grid":
            frame.grid(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "place":
            frame.place(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "pack":
            frame.pack(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        return frame

    @staticmethod
    def create_frame(
        master: Union[Misc, None] = None,
        cnf: Union[Dict[str, Any], None] = {},
        geometry_manager: Literal["grid", "place", "pack"] = "grid",
        geometry_manager_cnf: Union[Mapping[str, Any], None] = {},
        geometry_manager_kwargs: Dict[str, Any] = {},
        **kwargs
    ) -> Frame:
        frame = Frame(master, cnf, **kwargs)
        if geometry_manager == "grid":
            frame.grid(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "place":
            frame.place(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "pack":
            frame.pack(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        return frame

    def create_ttk_label_with_master(
        self,
        geometry_manager: Literal["grid", "place", "pack"] = "grid",
        geometry_manager_cnf: Union[Mapping[str, Any], None] = {},
        geometry_manager_kwargs: Dict[str, Any] = {},
        **kwargs
    ) -> ttk.Label:
        label = ttk.Label(self.master, **kwargs)
        if geometry_manager == "grid":
            label.grid(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "place":
            label.place(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "pack":
            label.pack(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        return label
    
    def create_label_with_master(
        self,
        cnf: Union[Dict[str, Any], None] = {},
        geometry_manager: Literal["grid", "place", "pack"] = "grid",
        geometry_manager_cnf: Union[Mapping[str, Any], None] = {},
        geometry_manager_kwargs: Dict[str, Any] = {},
        **kwargs
    ) -> Label:
        label = Label(self.master, cnf, **kwargs)
        if geometry_manager == "grid":
            label.grid(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "place":
            label.place(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "pack":
            label.pack(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        return label
    
    @staticmethod
    def create_ttk_label(
        master: Union[Misc, None] = None,
        geometry_manager: Literal["grid", "place", "pack"] = "grid",
        geometry_manager_cnf: Union[Mapping[str, Any], None] = {},
        geometry_manager_kwargs: Dict[str, Any] = {},
        **kwargs
    ) -> ttk.Label:
        label = ttk.Label(master, **kwargs)
        if geometry_manager == "grid":
            label.grid(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "place":
            label.place(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "pack":
            label.pack(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        return label

    @staticmethod
    def create_label(
        master: Union[Misc, None] = None,
        cnf: Union[Dict[str, Any], None] = {},
        geometry_manager: Literal["grid", "place", "pack"] = "grid",
        geometry_manager_cnf: Union[Mapping[str, Any], None] = {},
        geometry_manager_kwargs: Dict[str, Any] = {},
        **kwargs
    ) -> Label:
        label = Label(master, cnf, **kwargs)
        if geometry_manager == "grid":
            label.grid(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "place":
            label.place(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "pack":
            label.pack(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        return label

    def create_ttk_entry_with_master(
        self,
        widget: Union[str, None] = None,
        geometry_manager: Literal["grid", "place", "pack"] = "grid",
        geometry_manager_cnf: Union[Mapping[str, Any], None] = {},
        geometry_manager_kwargs: Dict[str, Any] = {},
        **kwargs
    ) -> ttk.Entry:
        entry = ttk.Entry(self.master, widget, **kwargs)
        if geometry_manager == "grid":
            entry.grid(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "place":
            entry.place(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "pack":
            entry.pack(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        return entry

    def create_entry_with_master(
        self,
        cnf: Union[Dict[str, Any], None] = {},
        geometry_manager: Literal["grid", "place", "pack"] = "grid",
        geometry_manager_cnf: Union[Mapping[str, Any], None] = {},
        geometry_manager_kwargs: Dict[str, Any] = {},
        **kwargs
    ) -> Entry:
        entry = Entry(self.master, cnf, **kwargs)
        if geometry_manager == "grid":
            entry.grid(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "place":
            entry.place(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "pack":
            entry.pack(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        return entry
    
    @staticmethod
    def create_ttk_entry(
        master: Union[Misc, None] = None,
        widget: Union[str, None] = None,
        geometry_manager: Literal["grid", "place", "pack"] = "grid",
        geometry_manager_cnf: Union[Mapping[str, Any], None] = {},
        geometry_manager_kwargs: Dict[str, Any] = {},
        **kwargs
    ) -> ttk.Entry:
        entry = ttk.Entry(master, widget, **kwargs)
        if geometry_manager == "grid":
            entry.grid(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "place":
            entry.place(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "pack":
            entry.pack(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        return entry

    @staticmethod
    def create_entry(
        master: Union[Misc, None] = None,
        cnf: Union[Dict[str, Any], None] = {},
        geometry_manager: Literal["grid", "place", "pack"] = "grid",
        geometry_manager_cnf: Union[Mapping[str, Any], None] = {},
        geometry_manager_kwargs: Dict[str, Any] = {},
        **kwargs
    ) -> Entry:
        entry = Entry(master, cnf, **kwargs)
        if geometry_manager == "grid":
            entry.grid(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "place":
            entry.place(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        elif geometry_manager == "pack":
            entry.pack(cnf=geometry_manager_cnf, **geometry_manager_kwargs)
        return entry

    