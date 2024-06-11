import streamlit as st
import streamlit.components.v1 as components


# Insert a container into a component to style specific elements
def key_container(key: str, class_name: str = '') -> "DeltaGenerator":
    style_text = f"<div data-testid=\"{key}\"></div>"

    container = st.container()
    container.markdown(style_text, unsafe_allow_html=True)

    components.html(f"""
        <script>
            frameElement.parentElement.style.display = 'none';
            var reference = window.parent.document.querySelector('[data-testid="{key}"]');
            var mdContainer = reference.parentElement.parentElement.parentElement;
            var container = mdContainer.nextSibling;
            container.id = '{key}';
            container.setAttribute('data-testid', '{key}');
            container.classList.add('{class_name}');
            mdContainer.remove();
        </script>
    """, height=0)
    return container
