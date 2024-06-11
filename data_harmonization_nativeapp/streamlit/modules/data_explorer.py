
import components
import streamlit as st
from components.error_handler import errorHandling
from globals import CAMPAIGN_PERFORMANCE_TABLE, DATE_COLUMN, CLICKS_COLUMN, SPEND_PER_CLICKS_COLUMN, YEAR_DATA_COLUMN, FACEBOOK_ADS_COLUMN, LINKEDIN_ADS_COLUMN, SNOW_COMP_COLUMN, OMNATA_OLD, OMNATA
from modules_backend.model_data_explorer_backend import *
from services.i18n import Translator
import plotly.express as px

@errorHandling
def data_explorer_page():
   t = Translator().translate
   sp_session = connect_to_snowflake()
   components.title(t('DataExplorer'))

   model_information = get_model_information()
   col1, col2 = st.columns(2)
   with col1:
      databases = sp_session.sql('SHOW DATABASES').select(QUOTED_NAME_KEY).collect()
      selected_database = st.selectbox(t('SelectorDatabase'), databases, index = get_value_index(databases, model_information[DATABASE_KEY]) if model_information else 0)
   with col2:
      try:
         schemas = sp_session.sql(f'SHOW SCHEMAS IN {selected_database}').select(QUOTED_NAME_KEY).collect()
         selected_schema = st.selectbox(t('SelectorSchema'), schemas, index = get_value_index(schemas, model_information[SCHEMA_KEY]) if model_information else 0)
      except:
         selected_schema = st.selectbox(t('SelectorSchema'), [])

   metrics = sp_session.sql(f"SELECT TABLE_NAME FROM {APPLICATION}.{INFORMATION_SCHEMA}.{TABLES_TABLE} WHERE TABLE_SCHEMA = '{selected_schema}' AND TABLE_NAME = '{CAMPAIGN_PERFORMANCE_TABLE}'", params=[f'{selected_database}.{selected_schema}']).collect()
   if metrics:
      st.write('#')
      st.write('#')

      with st.container():
         colx1, coly1, colz1 = st.columns(3)
         with colx1:
            components.subtitle(t('SpendPerDate'))
            df_spend_per_day = get_spend_per_day(sp_session, selected_database, selected_schema, CAMPAIGN_PERFORMANCE_TABLE)
            fig = px.line(df_spend_per_day, x=DATE_COLUMN, y=SPEND_COLUMN, width=277, height=350, markers=True)
   
            st.plotly_chart(fig, use_container_width = True)

            overall_spend = get_total_spend(sp_session, selected_database, selected_schema, CAMPAIGN_PERFORMANCE_TABLE)


         with coly1:
            components.subtitle(t('ReactionsPerDate'))
            df_clicks_per_day = get_clicks_per_day(sp_session, selected_database, selected_schema, CAMPAIGN_PERFORMANCE_TABLE)
            fig = px.line(df_clicks_per_day, x=DATE_COLUMN, y=CLICKS_COLUMN, width=277, height=350,markers=True)
   
            st.plotly_chart(fig, use_container_width = True)

            Total_clicks = df_clicks_per_day[CLICKS_COLUMN].sum()

         with colz1:
            components.subtitle(t('SpendPerReactions'))
            df_spend_per_clicks = get_spend_per_clicks(sp_session, selected_database, selected_schema, CAMPAIGN_PERFORMANCE_TABLE)
            fig = px.line(df_spend_per_clicks, x=DATE_COLUMN, y=SPEND_PER_CLICKS_COLUMN, width=277, height=350,markers=True)
   
            st.plotly_chart(fig, use_container_width = True)


         colx2, coly2, colz2 = st.columns(3)
         with colx2:
            overall_spend = get_total_spend(sp_session, selected_database, selected_schema, CAMPAIGN_PERFORMANCE_TABLE)
            colx2.metric(f':orange[{t("OverallSpend")}]', '$ {0}'.format(format_num(overall_spend)))
         with coly2:
            Total_clicks = df_clicks_per_day[CLICKS_COLUMN].sum()
            coly2.metric(f':orange[{t("OverallClicks")}]', format_num(Total_clicks))
         with colz2:
            avg_spend_per_clicks = df_spend_per_clicks[SPEND_PER_CLICKS_COLUMN].sum()/df_spend_per_clicks.shape[0]
            colz2.metric(f':orange[{t("AverageSpend/Clicks")}]', '$ {0}'.format(round(avg_spend_per_clicks, 3)))

         st.divider()
         
         colx3, coly3, colz3 = st.columns(3)
         with colx3:
            components.subtitle(t('PlatformSpendOverYears'))
            df_spend = get_spend_by_year(sp_session, selected_database, selected_schema, CAMPAIGN_PERFORMANCE_TABLE)
            st.bar_chart(df_spend, x=YEAR_DATA_COLUMN, y=[FACEBOOK_ADS_COLUMN, LINKEDIN_ADS_COLUMN], height=350)
         with coly3:
            components.subtitle(t('PlatformAndImpressions'))
            df_impressions = get_impressions_by_year(sp_session, selected_database, selected_schema, CAMPAIGN_PERFORMANCE_TABLE)
            st.bar_chart(df_impressions, x=YEAR_DATA_COLUMN, y=[FACEBOOK_ADS_COLUMN, LINKEDIN_ADS_COLUMN], height=350)
         with colz3:
            components.subtitle(t('SpendByAdAccount'))
            df_account_spend_by_year = get_account_spend_by_year(sp_session, selected_database, selected_schema, CAMPAIGN_PERFORMANCE_TABLE)
            df_account_spend_by_year.rename(columns=lambda x: x.replace("'", ""), inplace=True)
            columns_names = df_account_spend_by_year.columns.values.tolist()[1:]
            st.bar_chart(df_account_spend_by_year, x=YEAR_DATA_COLUMN, y=columns_names, height=300)

         colx4, coly4, colz4 = st.columns(3)
         with colx4:
            Total_Linkedin_spend = df_spend[LINKEDIN_ADS_COLUMN].sum()
            st.metric(f':orange[{t("LinkedinInvestment")}]', '$ {0}'.format(format_num(Total_Linkedin_spend)))
            Total_FB_spend = df_spend[FACEBOOK_ADS_COLUMN].sum()
            st.metric(f':orange[{t("FacebookInvestment")}]', '$ {0}'.format(format_num(Total_FB_spend)))
         with coly4:
            Total_Linkedin_impressions = df_impressions[LINKEDIN_ADS_COLUMN].sum()
            st.metric(f':orange[{t("LinkedinImpressions")}]', '{0}'.format(format_num(Total_Linkedin_impressions)))
            Total_FB_impressions = df_impressions[FACEBOOK_ADS_COLUMN].sum()
            st.metric(f':orange[{t("FacebookImpressions")}]', '{0}'.format(format_num(Total_FB_impressions)))
         with colz4:
            account_with_spend = get_account_with_spend(sp_session, selected_database, selected_schema, CAMPAIGN_PERFORMANCE_TABLE)
            st.markdown(account_with_spend.style.hide(axis="index").to_html(), unsafe_allow_html=True)
            
         st.divider()

         colx5, coly5, colz5 = st.columns(3)
         with colx5:
            components.subtitle(f':blue[{t("Top5CampaignWithHighestSpendClicks")}]')
         with coly5:
            components.subtitle(f':blue[{t("Top5AdsGroupsWithHighestImpressions")}]')
         with colz5:
            components.subtitle(f':blue[{t("Top5AdsGroupsWithHighestClicks")}]')
         
         colx5, coly5, colz5 = st.columns(3)
         with colx5:
            df_top_5_spend_per_clicks = get_top_5_spend_per_clicks(sp_session, selected_database, selected_schema, CAMPAIGN_PERFORMANCE_TABLE)
            st.markdown(df_top_5_spend_per_clicks.style.hide(axis="index").to_html(), unsafe_allow_html=True)

         with coly5:
            df_top_5_ads_with_impressions = get_top_5_ad_groups_with_impressions(sp_session, selected_database, selected_schema, CAMPAIGN_PERFORMANCE_TABLE)
            st.markdown(df_top_5_ads_with_impressions.style.hide(axis="index").to_html(), unsafe_allow_html=True)

         with colz5:
            df_top_5_ads_with_clicks = get_top_5_ad_groups_with_clicks(sp_session, selected_database, selected_schema, CAMPAIGN_PERFORMANCE_TABLE)
            st.markdown(df_top_5_ads_with_clicks.style.hide(axis="index").to_html(), unsafe_allow_html=True)