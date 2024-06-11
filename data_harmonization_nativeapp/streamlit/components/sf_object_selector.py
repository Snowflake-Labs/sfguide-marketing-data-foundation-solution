import streamlit as st
import json


class ObjectSelector:
    def __init__(self, sp_session, label, query, key, column_name: str = '"name"', on_change=None, label_visibility='visible'):
        self.sp_session = sp_session
        self.label = label
        self.query = query
        self.key = key
        self.column_name = column_name
        self.on_change = on_change
        self.label_visibility = label_visibility


    def render(self):
        sf_obj_list = self.query_cached_sf_object(self.sp_session, self.query, self.column_name)
        object_selected = st.selectbox(self.label, sf_obj_list, key=self.key, on_change=self.on_change, label_visibility=self.label_visibility)
        return object_selected
    
    def render_array_column(self):
        sf_obj_list = self.query_cached_sf_object(self.sp_session, self.query, self.column_name)
        sf_obj_list = json.loads(sf_obj_list[0][self.column_name.strip('"')])
        object_selected = st.selectbox(self.label, sf_obj_list, key=self.key)
        return object_selected

    @st.cache_data(
        ttl=3600, # clears cache after one hour
        show_spinner='Fetching data...',
        hash_funcs={'components.sf_object_selector.ObjectSelector': lambda _: None})
    def query_cached_sf_object(_self, _sp_session, sql_query: str, column_name: str):
        query_result = _sp_session.sql(sql_query)
        query_result = query_result.select(column_name).collect() if query_result.count() > 0 else []
        return query_result
