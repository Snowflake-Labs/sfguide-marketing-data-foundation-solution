from components.texts.text import DEFAULT_COLOR, text as text_component


TITLE = {
    'font_size': 24,
    'font_weight': 600,
    'font_family': 'sans-serif',
    'line_height': 24,
}

SUBTITLE = {
    'font_size': 20,
    'font_weight': 600,
    'font_family': 'sans-serif',
    'line_height': 24,
}

MEDIUM_BOLD = {
    'font_size': 16,
    'font_weight': 600,
    'font_family': 'sans-serif',
    'line_height': 20,
}

MEDIUM = {
    'font_size': 16,
    'font_weight': 400,
    'font_family': 'sans-serif',
    'line_height': 20,
}

SMALL_BOLD = {
    'font_size': 14,
    'font_weight': 600,
    'font_family': 'sans-serif',
    'line_height': 20,
}

SMALL = {
    'font_size': 14,
    'font_weight': 400,
    'font_family': 'sans-serif',
    'line_height': 20,
}

EXTRA_SMALL = {
    'font_size': 12,
    'font_weight': 400,
    'font_family': 'sans-serif',
    'line_height': 20,
}

def title(text: str, key: str = None, color: str = DEFAULT_COLOR) -> None:
    text_component(text=text, key=key, color=color, **TITLE)

def subtitle(text: str, key: str = None, color: str = DEFAULT_COLOR) -> None:
    text_component(text=text, key=key, color=color, **SUBTITLE)

def text_medium_bold(text: str, key: str = None, color: str = DEFAULT_COLOR) -> None:
    text_component(text=text, key=key, color=color, **MEDIUM_BOLD)

def text_medium(text: str, key: str = None, color: str = DEFAULT_COLOR) -> None:
    text_component(text=text, key=key, color=color, **MEDIUM)

def text_small_bold(text: str, key: str = None, color: str = DEFAULT_COLOR) -> None:
    text_component(text=text, key=key, color=color, **SMALL_BOLD)

def text_small(text: str, key: str = None, color: str = DEFAULT_COLOR) -> None:
    text_component(text=text, key=key, color=color, **SMALL)

def text_extra_small(text: str, key: str = None, color: str = DEFAULT_COLOR) -> None:
    text_component(text=text, key=key, color=color, **EXTRA_SMALL)
