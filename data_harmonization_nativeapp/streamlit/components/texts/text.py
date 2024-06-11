import re
import streamlit as st

from components.stylable_container import stylable_container


DEFAULT_COLOR = '#262730'


def text(
    text: str,
    key: str = None,
    font_size: int = 16,
    font_weight: int = 400,
    font_family: str = 'sans-serif',
    line_height: int = 20,
    color: str = DEFAULT_COLOR,
) -> None:
    key = _default_key(key, text)
    style = _get_style(font_size, font_weight, font_family, line_height, color)

    _render(text, key, style)


def _render(text: str, key: str, css_styles: str) -> None:
    with stylable_container(key, css_styles):
        st.write(text)


def _default_key(key: str, text: str) -> str:
    return key or re.sub('[^a-zA-Z]', '_', text)


def _get_style(
    font_size: int,
    font_weight: int,
    font_family: str,
    line_height: int,
    color: str
) -> str:
    return f'''
    {{
        p {{
            line-height: {line_height}px;
            font-size: {font_size}px;
            font-weight: {font_weight};
            font-family: {font_family};
            color: {color};
        }}
    }}
    '''
