import re
import streamlit as st

from streamlit.type_util import Key, to_key
from streamlit.runtime.state import (WidgetArgs, WidgetCallback, WidgetKwargs)
from components.stylable_container import stylable_container
from components.icon import Icon
from typing_extensions import Literal
from typing import Optional


# Custom button, wrapper for streamlit button
# @arg style string of css properties expample: "background-color: red; color: white"
def button(
    label: str = "",
    key: Optional[Key] = None,
    help: Optional[str] = None,
    on_click: Optional[WidgetCallback] = None,
    args: Optional[WidgetArgs] = None,
    kwargs: Optional[WidgetKwargs] = None,
    type: Literal["primary", "secondary", "critical"] = "secondary",
    disabled: bool = False,
    use_container_width: bool = False,
    styles: str = "",
    icon: Icon = None
) -> bool:
    key = _default_key(key, label)
    style = f"""
        button {{
            text-wrap: nowrap;
            {_get_type_style(type)}
            {_get_icon_style(icon, label != "")}
            {styles}
            
        }}
        """
    type = type if type != "critical" else "secondary"
    with stylable_container(key=key, css_styles=style):
        btn = st.button(label=label, key=key, help=help, on_click=on_click, args=args, kwargs=kwargs, type=type, disabled=disabled, use_container_width=use_container_width)

    return btn

def _default_key(key: str, text: str) -> str:
    return key or re.sub('[^a-zA-Z]', '_', text)

def _get_type_style(type: Literal["primary", "secondary", "critical"] = "secondary") -> str:
    return """
        background-color: red; 
        color: white;
        """ if type == "critical" else ""

def _get_icon_style(icon: Icon, is_labeled: bool) -> str:
    return f"""
        {icon.get_bg_style()} 
        {_get_icon_padding_style(icon, is_labeled)}
        """ if icon is not None else ""

def _get_icon_padding_style(icon: Icon, is_labeled: bool):
    offset = 8
    if is_labeled: padding = f"padding-{icon.alignment}: {icon.width + offset}px;"
    else: padding = f"padding: 0 {icon.width / 2 + offset}px;"
    return padding
