import streamlit as st
import streamlit.components.v1 as components

from modules_backend.add_platform_analytics_model_backend import open_md
from components.tooltip import tooltip_stylesheet, tooltip_component

class Accordion:
  def __init__(self, id: str, table_name: str, columns: list, mappings: list, zindex: int = 0, onclick: str = None):
      self.id = id
      self.table_name = table_name
      self.columns = columns
      self.mappings = mappings
      self.zindex = zindex
      self.onclick = onclick

  def render(self) -> str:
    return f'''
    <div id={self.id} class="accordion">
      {self._get_style()}
      {self._on_filter_action(self.id)}
      {self._render_accordion()}
    </div>
    '''

  def _render_accordion(self) -> str:
    return f'''
    <input type="checkbox" class="collapsable accordion-input" id="cb-{self.table_name}" checked="false">
    <label for="cb-{self.table_name}" class="accordion-header tooltip" onclick="{self._onclick_action()}">
      <p onload="{self._is_text_overflow_action()}">{self.table_name}</p>
      {tooltip_component(self.table_name)}
    </label>
    <div class="content-container">
      <ul class="element-list">
        {self._columns(self.table_name, self.columns, self.mappings)}
      </ul>
    </div>
    '''

  def _is_text_overflow_action(self) -> str:
    return "if (this.offsetWidth < this.scrollWidth) this.className='is-overflow'"

  def _onclick_action(self) -> str:
    return """
      setTimeout(function(el) {
        el.scrollIntoView({ behavior: 'smooth'})
      }, 20, this);
    """

  def _on_filter_action(self, key: str) -> str:
    # Hiddes the accordion when no child is visible
    return f'''
    <script>
      on_filter_action_{key} = () => {{
        let accordion = document.getElementById('{key}')
        let elements =  accordion.querySelector('ul').children;
        for (let e of elements) 
          if (e.style.display != 'none') {{
            accordion.style.display = '';
            return;
          }}

        // Hidde accordion if no element is visible
        accordion.style.display = 'none';
      }}
    </script>
    '''

  def _columns(self, table_name: str, columns: list, mappings: list) -> str:
    html = ""
    for column in columns:
        id = f'{table_name}.{column}'.lower()
        column = column.upper()
        callback = f'onclick="{self.onclick}(this)"' if self.onclick else ''
        is_disabled = 'disabled' if id not in mappings else ''
        html += f"<li id='{id}' class='element {is_disabled}' data-testid='{id}' {callback}>{column}</li>"
    return html


  def _get_style(self) -> str:
    return f'''
      {tooltip_stylesheet()}
      <style>

#{self.id} {{
  z-index: {self.zindex}
}}

.accordion {{
  position: relative;
  margin-bottom: 16px;
}}

/* Core styles/functionality */
.accordion-input {{
  position: absolute;
  opacity: 0;
  z-index: -1;
}}

.content-container {{
  height:1%;
  max-height: 0;
  overflow: hidden;
  transition: all 0.35s;
}}

.accordion-input:not(:checked) ~ .content-container {{
  max-height: fit-content;
}}

.element-list {{
  list-style: none;
  display: flex;
  flex-direction: column;
  padding: 0;
  margin: 0;
  gap: 6px;
}}

.element {{
  height: 24px;
  align-content: center;
  font-size: 12px;
  font-family: sans-serif;
  padding: 0 12px;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
  cursor: pointer;
  box-sizing: border-box;
}}

.element.disabled {{
  opacity: .4;
}}

.element:hover:not(.disabled) {{
    border: 1px solid #60B4FF;
    border-radius: 8px;
}}

/* Visual styles */
.accordion-header {{
  display: flex;
  cursor: pointer;
  margin: 0 8px 6px 0;
  position: sticky;
  font-weight: 600;
  font-size: 14px;
  justify-content: space-between;
  background-color: white;
  top: 0;
}}
.accordion-header::after {{
  content: "\\276F";
  width: 1em;
  height: 1em;
  text-align: center;
  transform: rotate(90deg);
  transition: all 0.35s;
}}
.accordion-header p {{
  margin: 0;
  padding-right: 12px;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}}

.accordion-input:not(:checked) + .accordion-header::after {{
  transform: rotate(270deg);
}}
</style>   
'''