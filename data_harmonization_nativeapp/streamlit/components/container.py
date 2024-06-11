import streamlit as st
from components.stylable_container import stylable_container
from globals import LIGHT_GRAY_3


def container(key: str, height: int = None, scrollable: bool = False, customStyle = None) -> "DeltaGenerator":
    
    style = f"""
        {{
            display: block;
            border: 1px solid {LIGHT_GRAY_3};
            border-radius: 8px;
            padding: 24px 16px;
            {_get_height_style(height)}
            {_get_overflow_style(scrollable)}
            {str(customStyle)}
        }}
    """

    return stylable_container(key = key, css_styles = style)


def _get_height_style(height: int) -> str:
    style = f'height: {height}px; max-height: {height}px;'
    return style if height is not None else ''


def _get_overflow_style(scrollable: bool) -> str:
    style = 'overflow-y: auto; overflow-x: hidden;'
    return style if scrollable else ''
