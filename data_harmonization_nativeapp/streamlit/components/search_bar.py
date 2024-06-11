from typing import List


def search_bar_component(key: str, html_elements_query: str = None, callback: str = '') -> str:
    return _render(key, html_elements_query, callback)


def _render(key: str, html_elements_query: str, callback: str) -> str:
    return f"""
    <div id="{_get_search_bar_key(key)}" class="search-bar">
        {_style_sheet()}
        {_search_script(key, html_elements_query, callback)}
        {_clear_input_script(key)}
        <input type="text" class="search-input" placeholder="🔍 Search" oninput="on_search_action_{key}(event)">
    </div>
    """


def _search_script(key: str, html_elements_query: str, callback: str) -> str:
    if html_elements_query is None: return ""
    callback = f'{callback}()' if callback else ''
    return f"""
    <script>
        on_search_action_{key} = (event) => {{
            let value = event.target.value;
            let elements = {html_elements_query};
            
            // filters elements by hidding theme
            elements.forEach(e => e.style.display = e.id.includes(value) ? '' : 'none');

            {callback}
        }}
    </script>
    """


def _clear_input_script(key: str) -> str:
    return f"""
    <script>
        on_clear_searchbar_action_{key} = () => {{
            let input = document.getElementById('{_get_search_bar_key(key)}').querySelector('input');
            input.value = '';
            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
        }}
    </script>
    """


def _style_sheet():
    return f"""
    <style>
        .search-bar {{
            display: flex;
            height: 40px;
            width: 100%;
        }}
        .search-input {{
            display: block;
            width: 100%;
            height: 100%;
            padding: 8px;
            border: 1px;
            border-radius: 8px;
            background-color: #F0F2F6;
            box-sizing: border-box;
            outline-color: #0068C9;
        }}
        .search-input::placeholder {{
            font-size: 16px;
            font-family: sans-serif;
        }}
    </style>
    """


def _get_search_bar_key(key: str) -> str:
    return f'{key}_search_bar'
