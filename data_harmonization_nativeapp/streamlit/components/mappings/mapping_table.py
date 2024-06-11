import streamlit as st
import streamlit.components.v1 as components

from components.search_bar import search_bar_component
from services.i18n import Translator
from components.mappings.arrow_icon import arrow_icon_svg


t = Translator().translate


class MappingTable:
    selected_row_class_name = 'selected_row'
    collapsable_class_name = 'collapsable'


    def __init__(self, key: str, data):
        self.key = key
        self.data = data
    

    def render(self) -> str:
        filter_query = f'document.getElementById("{self.key}").querySelectorAll(".data-row");'

        return f"""
        <div id="{self.key}" class="mapping-table-container">
            {self._render_stylesheet()}
            {self._click_row_script()}
            <div class="header_container">
                <h2 class="header-label">{t('CustomMapMappingsHeader')}</h2>
            </div>
            {search_bar_component(key="mapping_table", html_elements_query=filter_query)}
            <div class="content_container">
                {self._render_data(self.data)}
            </div>
        </div>
        """


    def _render_data(self, data: list) -> str:
        return f"""
        <div class="data-headers-container">
            <div class="flex-colum">
                <h4 class="data-header-label source-header-label">{t('CustomMapSourceHeader')}</h4>
            </div>
            <div class="flex-colum">
                <h4 class="data-header-label target-header-label">{t('CustomMapTargetHeader')}</h4>
            </div>
        </div>
        <div class="data-container">
            {self._render_data_rows(data)}
        </div>
        """


    def _render_data_rows(self, data: list) -> str:
        rows = ""
        for row in data:
            rows += self._render_data_row(source=row[0], target=row[1])
        return rows


    def _render_data_row(self, source: str, target: str) -> str:
        id = f'{source}-{target}'.lower()
        src_label = source.split('.')[1].upper()
        trg_label = target.split('.')[1].upper()
        return f"""
        <div id="{id}" class="data-row" data-testid="{id}" onclick="click_row_action(this)">
            <div class="flex-colum">
                <span>{src_label}</span>
            </div>
            <div class="flex-colum flex-colum-middle">
                <div class="arrow-box">
                    {arrow_icon_svg()}
                </div>
            </div>
            <div class="flex-colum">
                <span>{trg_label}</span>
            </div>
        </div>
        """


    def _click_row_script(self) -> str:
        selected_row = self.selected_row_class_name
        collapsable = self.collapsable_class_name

        return f"""
        <script>
            click_row_action = (row) => {{
                let [source, target] = row.id.split('-');
                source = document.getElementById(source);
                target = document.getElementById(target);

                // Clear selected rows if any
                let selected = document.querySelectorAll('.{selected_row}');
                selected.forEach(row => row.classList.remove('{selected_row}'));

                // Select new rows
                row.classList.add('{selected_row}');
                source.classList.add('{selected_row}');
                target.classList.add('{selected_row}');

                // Open sidebars if needed
                let collapsable = document.querySelectorAll('.{collapsable}');
                collapsable.forEach(e => e.checked = false);

                // Clear searchbars if needed
                on_clear_searchbar_action_target_schema_side_bar();
                on_clear_searchbar_action_source_schema_side_bar();

                // Scroll rows if needed
                source.scrollIntoViewIfNeeded(true);
                target.scrollIntoViewIfNeeded(true);
            }}
        </script>
        """


    def _render_stylesheet(self) -> str:
        selected_row_class = self.selected_row_class_name
        return f"""
        <style>
            .mapping-table-container {{
                width: 100%;
                display: flex;
                flex-direction: column;
                padding: 24px 16px;
                gap: 16px;
                border: 1px solid #D5DAE5;
                border-radius: 8px;
            }}

            .header-label {{
                margin: 0;
                line-height: 24px;
                font-size: 20px;
                font-weight: bold;
                text-align: center;
            }}

            .data-headers-container {{
                width: 100%;
                height: 24px;
                display: flex;
                gap: 140px;
            }}

            .data-header-label {{
                line-height: 24px;
                margin: 0;
            }}
            
            .data-container {{
                height: 600px;
                display: flex;
                flex-direction: column;
                overflow-y: auto;
                gap: 6px;
            }}

            .data-row {{
                display: flex;
                align-items: center;
                box-sizing: border-box;
                height: 44px;
                padding: 12px 0;
                gap: 48px;
                font-size: 12px;
                line-height: 20px;
                cursor: pointer;
                box-sizing: border-box;
            }}

            .flex-colum {{
                width: 100%;
                padding: 0 12px;
            }}

            .flex-colum-middle {{
                width: 45px;
                height: 100%;
                padding: 0;
            }}

            .arrow-box {{
                width: inherit;
                height: inherit;
                text-align: center;
            }}

            .data-row:hover,
            .{selected_row_class} {{
                border: 1px solid #0068C9;
                border-radius: 8px;
            }}

            .data-row:hover {{
                border-color: #60B4FF;
            }}
        </style>
        """
