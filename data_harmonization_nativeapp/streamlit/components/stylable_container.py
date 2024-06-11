import streamlit as st

# Insert a container into a component to style specific elements
# @arg css_styles of type str or str[]
def stylable_container(key: str, css_styles) -> "DeltaGenerator":
    if isinstance(css_styles, str):
        css_styles = [css_styles]

    # Remove spacing added by markdown
    css_styles.append("> div:first-child { display: none; }")

    style_text = "\n<style>"

    for style in css_styles:
        style_text += f"""
div[data-testid="stVerticalBlock"]:has(> div.element-container > div.stMarkdown > div[data-testid="stMarkdownContainer"] > p > span.{key}) {style}
"""

    style_text += f"</style>\n<span class=\"{key}\"></span>"

    container = st.container()
    container.markdown(style_text, unsafe_allow_html=True)
    return container
