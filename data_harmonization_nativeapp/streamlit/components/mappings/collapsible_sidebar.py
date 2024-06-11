import streamlit as st
import streamlit.components.v1 as components

from components.mappings.accordion import Accordion
from components.search_bar import search_bar_component
from modules_backend.add_platform_analytics_model_backend import open_md
from dtos.table_model import TableModel
from typing import List, Literal


class CollapsibleSideBar:
    selected_row_class_name = 'selected_row'
    collapsable_class_name = 'collapsable'
    accordion_callbacks = []


    def __init__(self,
        label: str,
        key: str,
        data: List[TableModel],
        mappings: List[str],
        orientation: Literal["left", "right"] = "left"
    ) -> None:
        self.label = label
        self.key = key
        self.orientation = orientation
        self.data = data
        self.mappings = mappings
    
    def render(self) -> str:
        return f'''
        <div id="{self.key}" class="sidebar-container sidebar-container-{self.orientation}">
            {self._render_stylesheet()}
            {self._click_row_script()}
            {self._filter_callback_script()}
            {self._render_sidebar()}
        </div>
        '''

    def _render_sidebar(self) -> str:
        filter_query = f'document.getElementById("{self.key}").querySelectorAll("li");'
        filer_callback = f'on_filter_{self.orientation}_action'

        return f'''
        <input type="checkbox" id="toggler_{self.orientation}" class="collapsable checkbox" checked='true'/>
        <aside class="aside-wrapper aside-{self.orientation}">
            <div class="aside-element">
                <label for="toggler_{self.orientation}" class="visible-label visible-label-{self.orientation}">
                    {self._render_arrow_icon()}
                    <h1 class="visible-header"><span>{self.label}</span></h1>
                </label>
            </div>
            <div class="aside-element">
                {search_bar_component(self.key, html_elements_query=filter_query, callback=filer_callback)}
            </div>
            <h2 class="aside-element hidden-label hidden-label-{self.orientation}">{self.label}</h2>
            <div class="aside-element main-content main-content-{self.orientation}">
                {self._generate_accordions()}
            </div>
        </aside>
        '''


    def _render_arrow_icon(self) -> str:
        collapsed_arrow = open_md('arrowback.svg')
        expanded_arrow = open_md('arrowforward.svg')
        is_invert = self.orientation == 'left'
        
        return f'''
        <div class="sidebar-toggle sidebar-toggle-{self.orientation}">
            <div class="arrow-icon expanded-arrow">{expanded_arrow if is_invert else collapsed_arrow}</div>
            <div class="arrow-icon collapsed-arrow">{collapsed_arrow if is_invert else expanded_arrow}</div>
        </div>
        '''


    def _generate_accordions(self) -> str:
        result = ""
        length = len(self.data)
        for i, table in enumerate(self.data):
            key = table.table_name
            callback = f'click_column_{self.orientation}_action'
            zindex = length - i
            result += Accordion(key, key, table.columns, self.mappings, zindex, callback).render()
            self._add_accordion_filter_callback(key)
        return result


    def _add_accordion_filter_callback(self, key: str) -> None: 
        callback_fun = f'on_filter_action_{key}'
        self.accordion_callbacks.append(callback_fun)


    def _filter_callback_script(self) -> str:
        accordion_callbacks = '();\n'.join(self.accordion_callbacks) + '();'
        return f"""
        <script>
            on_filter_{self.orientation}_action = () => {{
                {accordion_callbacks}
            }}
        </script>
        """


    def _click_row_script(self) -> str:
        selected_row = self.selected_row_class_name
        collapsable = self.collapsable_class_name

        is_source = self.orientation == 'left'
        query = "'[data-testid^=\"'+row.id+'-\"]'" if is_source else "'[data-testid$=\"-'+row.id+'\"]'"

        return f"""
        <script>
        click_column_{self.orientation}_action = (row) => {{
            var row, source, target = null;

            // Clear selected rows if any
            let selected = document.querySelectorAll('.{selected_row}');
            selected.forEach(row => row.classList.remove('{selected_row}'));

            // Select new rows
            let mapping_rows = document.querySelectorAll({query});
            for (row of mapping_rows) {{
                var [source, target] = row.id.split('-');

                source = document.getElementById(source);
                target = document.getElementById(target);
                
                row.classList.add('{selected_row}');
                if (target != row) target.classList.add('{selected_row}');
                if (source != row) source.classList.add('{selected_row}');
            }}

            // Open sidebars if needed
            let collapsable = document.querySelectorAll('.{collapsable}');
            collapsable.forEach(e => e.checked = false);

            // Scroll rows if needed
            row?.scrollIntoViewIfNeeded(true);
            source?.scrollIntoViewIfNeeded(true);
            target?.scrollIntoViewIfNeeded(true);
        }}
        </script>
        """


    def _render_stylesheet(self) -> str:
        return f"""
        <style>
        .sidebar-container {{
            min-width: 58px;
            border: 1px solid #D5DAE5;
            border-radius: 8px;
            box-sizing: border-box;
        }}

        .sidebar-container:has(input.checkbox:not(:checked)) {{
            min-width: 276px;
        }}

        .{self.selected_row_class_name} {{
            border: 1px solid #0068C9;
            border-radius: 8px;
        }}
        
        aside {{
            width: 276px;
            min-height: 400px;
            position: fixed;
            display: flex;
            flex-direction: column;
        }}

        .aside-right {{
            right: 0;
        }}
        
        .aside-wrapper {{
            height: 770px;
            display: flex;
            flex-direction: column;
            box-sizing: border-box;
            padding: 24px 1px;
            gap: 16px;
        }}

        .aside-wrapper > .aside-element {{
            padding: 0 16px;
        }}

        .search-bar-container {{
            margin-bottom: 16px
        }}

        .visible-label {{
            width: 100%;
            height: 24px;
            display: flex;
            flex-wrap: nowrap;
            gap: 12px;
            cursor: pointer;
        }}

        .visible-header {{
            line-height: 24px;
            font-size: 16px;
            position: relative;
            margin: 0 0 16px 0;
        }}
        
        .sidebar-toggle {{
            height: 25px;
            padding: 2.5px 0;
        }}
        
        .arrow-icon > svg {{
            height: 12px;
            stroke: black;
            stroke-width: 2;
        }}
        
        input.checkbox {{
            display: none;
        }}
        
        /* Toggler Functionality */
        input.checkbox:checked ~ .aside-left {{
            left: -210px;
        }}
                        
        input.checkbox:checked ~ .aside-right {{
            right: -210px;
        }}

        input.checkbox:checked ~ aside .main-content {{
            display: none;
        }}
        
        input.checkbox:not(:checked) ~ aside .hidden-label {{
            display: none;
        }}

        input.checkbox:checked ~ aside .visible-header {{
            display: none;
        }}

        input.checkbox:checked ~ aside .search-bar {{
            display: none;
        }}

        input.checkbox:not(:checked) ~ aside .sidebar-toggle .expanded-arrow{{
            display:none;
        }}

        input.checkbox:checked ~ aside .sidebar-toggle .collapsed-arrow{{
            display:none;
        }}

        input.checkbox:checked ~ aside .visible-label-left {{
            flex-direction: row-reverse;
        }}
        
        .hidden-label {{
            margin: 0;
            position: relative;
            writing-mode: vertical-rl;
            text-orientation: mixed;
            text-wrap: nowrap;
            font-size: 20px;
            line-height: 24px;
            transform: scale(-1);
        }}

        .hidden-label-left {{
            align-self: baseline;
        }}
                        
        .main-content{{
            overflow-y: auto;
            overflow-x: hidden;
            height: 100%;
            padding-right: 16px;
        }}

        .main-content-container {{
            display: flex;
            flex-direction: column;
            padding: 0 12px;
            margin: 0;
        }}
    </style>
    """
