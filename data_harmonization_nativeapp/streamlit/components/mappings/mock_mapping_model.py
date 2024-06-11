MockTargetUnifiedModel =  [
    {
        "table_name": "DIM_ACCOUNT",
        "columns": [
            "account_id",
            "account_name",
            "account_status",
            "business_country_code",
            "currency_key",
            "timezone_key",
            "created_at",
            "updated_at",
            "status"
        ]
    },
    {
        "table_name": "DIM_LABEL",
        "columns": [
            "label_id",
            "label_name",
            "account_id",
            "object_type",
            "object_id",
            "created_at",
            "updated_at"
        ]
    },
    {
        "table_name": "DIM_AD",
        "columns": [
            "ad_id",
            "ad_name",
            "ad_type",
            "full_ad_url",
            "ad_group_id",
            "campaign_id",
            "account_id",
            "created_at",
            "updated_at"
        ]
    },
    {
        "table_name": "DIM_CAMPAIGN",
        "columns": [
            "campaign_id",
            "campaign_name",
            "account_id",
            "date_start",
            "date_end",
            "status",
            "daily_budget",
            "lifetime_budget",
            "budget_remaining",
            "created_at",
            "updated_at"
        ]
    },
    {
        "table_name": "DIM_AD_GROUP",
        "columns": [
            "ad_group_id",
            "ad_group_name",
            "campaign_id",
            "account_id",
            "created_at",
            "updated_at"
        ]
    },
    {
        "table_name": "METRICS",
        "columns": [
            "date",
            "timezone",
            "geography_object",
            "platform_id",
            "account_id",
            "campaign_id",
            "ad_group_id",
            "keyword_id",
            "label_id",
            "currency_key",
            "impressions",
            "clicks",
            "spend",
            "conversions",
            "value_of_conversions"
        ]
    },
    {
        "table_name": "DIM_PLATFORM",
        "columns": [
            "platform_id",
            "platform_name"
        ]
    },
    {
        "table_name": "DIM_KEYWORD",
        "columns": [
            "keyword_id",
            "keyword",
            "ad_group_id",
            "campaign_id",
            "account_id",
            "created_at",
            "updated_at"
        ]
    }
]

MockFacebookFivetran = [
    ['ACCOUNT_HISTORY.BUSINESS_COUNTRY_CODE', 'DIM_ACCOUNT.business_country_code'],
    ['ACCOUNT_HISTORY.CREATED_TIME', 'DIM_ACCOUNT.created_at'],
    ['ACCOUNT_HISTORY.CURRENCY', 'DIM_ACCOUNT.currency_key'],
    ['ACCOUNT_HISTORY.CURRENCY', 'METRICS.currency_key'],
    ['ACCOUNT_HISTORY.NAME', 'DIM_ACCOUNT.account_name'],
    ['ACCOUNT_HISTORY.TIMEZONE_NAME', 'DIM_ACCOUNT.timezone_key'],
    ['ACCOUNT_HISTORY.TIMEZONE_NAME', 'METRICS.timezone'],
    ['ACCOUNT_HISTORY.ACCOUNT_STATUS', 'DIM_ACCOUNT.account_status'],
    ['ACCOUNT_HISTORY.ID', 'DIM_ACCOUNT.account_id'],

    ['LABEL_HISTORY.id', 'DIM_LABEL.label_id'],
    ['LABEL_HISTORY.updated_time', 'DIM_LABEL.updated_at'],
    ['LABEL_HISTORY.account_id', 'DIM_LABEL.account_id'],
    ['LABEL_HISTORY.created_time', 'DIM_LABEL.created_at'],
    ['LABEL_HISTORY.name', 'DIM_LABEL.label_name'],

    ['AD_HISTORY.id', 'DIM_AD.ad_id'],
    ['AD_HISTORY.updated_time', 'DIM_AD.updated_at'],
    ['AD_HISTORY.account_id', 'DIM_AD.account_id'],
    ['AD_HISTORY.ad_set_id', 'DIM_AD.ad_group_id'],
    ['AD_HISTORY.campaign_id', 'DIM_AD.campaign_id'],
    ['AD_HISTORY.created_time', 'DIM_AD.created_at'],
    ['AD_HISTORY.name', 'DIM_AD.ad_name'],

    ['CAMPAIGN_HISTORY.id', 'DIM_CAMPAIGN.campaign_id'],
    ['CAMPAIGN_HISTORY.updated_time', 'DIM_CAMPAIGN.updated_at'],
    ['CAMPAIGN_HISTORY.account_id', 'DIM_CAMPAIGN.account_id'],
    ['CAMPAIGN_HISTORY.budget_remaining', 'DIM_CAMPAIGN.budget_remaining'],
    ['CAMPAIGN_HISTORY.created_time', 'DIM_CAMPAIGN.created_at'],
    ['CAMPAIGN_HISTORY.daily_budget', 'DIM_CAMPAIGN.daily_budget'],
    ['CAMPAIGN_HISTORY.lifetime_budget', 'DIM_CAMPAIGN.lifetime_budget'],
    ['CAMPAIGN_HISTORY.name', 'DIM_CAMPAIGN.campaign_name'],
    ['CAMPAIGN_HISTORY.start_time', 'DIM_CAMPAIGN.date_start'],
    ['CAMPAIGN_HISTORY.status', 'DIM_CAMPAIGN.status'],
    ['CAMPAIGN_HISTORY.stop_time', 'DIM_CAMPAIGN.date_end'],

    ['AD_SET_HISTORY.id', 'DIM_AD_GROUP.ad_group_id'],
    ['AD_SET_HISTORY.updated_time', 'DIM_AD_GROUP.updated_at'],
    ['AD_SET_HISTORY.account_id', 'DIM_AD_GROUP.account_id'],
    ['AD_SET_HISTORY.campaign_id', 'DIM_AD_GROUP.campaign_id'],
    ['AD_SET_HISTORY.campaign_id', 'METRICS.campaign_id'],
    ['AD_SET_HISTORY.created_time', 'DIM_AD_GROUP.created_at'],
    ['AD_SET_HISTORY.name', 'DIM_AD_GROUP.ad_group_name'],

    ['BASIC_AD.date', 'METRICS.date'],
    ['BASIC_AD.account_id', 'METRICS.account_id'],
    ['BASIC_AD.impressions', 'METRICS.impressions'],
    ['BASIC_AD.inline_link_clicks', 'METRICS.clicks'],
    ['BASIC_AD.spend', 'METRICS.spend'],

    ['AD_CONVERSION.conversion_id', 'METRICS.conversions'],

    ['AD_LABEL.label_id', 'METRICS.label_id'],
]

MockLinkedInOmnata = [
    ['accounts.APP_IDENTIFIER', 'DIM_ACCOUNT.account_id'],
    ['accounts.RECORD_DATA', 'DIM_ACCOUNT.account_name'],
    ['accounts.RECORD_DATA', 'DIM_ACCOUNT.account_status'],
    ['accounts.RECORD_DATA', 'DIM_ACCOUNT.currency_key'],
    ['accounts.RECORD_DATA', 'DIM_ACCOUNT.created_at'],
    ['accounts.RECORD_DATA', 'DIM_ACCOUNT.updated_at'],
    
    ['accounts.RECORD_DATA', 'DIM_CAMPAIGN.account_id'],

    ['ad_analytics_by_campaign_daily.RECORD_DATA', 'METRICS.date'],
    ['ad_analytics_by_campaign_daily.RECORD_DATA', 'METRICS.ad_group_id'],
    ['ad_analytics_by_campaign_daily.RECORD_DATA', 'METRICS.impressions'],
    ['ad_analytics_by_campaign_daily.RECORD_DATA', 'METRICS.clicks'],
    ['ad_analytics_by_campaign_daily.RECORD_DATA', 'METRICS.spend'],

    ['ad_analytics_by_campaign_group_daily.RECORD_DATA', 'DIM_CAMPAIGN.id'],
    ['ad_analytics_by_campaign_group_daily.RECORD_DATA', 'DIM_CAMPAIGN.date_start'],
    ['ad_analytics_by_campaign_group_daily.RECORD_DATA', 'DIM_CAMPAIGN.date_end'],

    ['campaigns.APP_IDENTIFIER', 'DIM_AD_GROUP.id'],
    ['campaigns.RECORD_DATA', 'DIM_AD_GROUP.ad_group_name'],
    ['campaigns.RECORD_DATA', 'DIM_AD_GROUP.campaign_id'],
    ['campaigns.RECORD_DATA', 'DIM_AD_GROUP.account_id'],
    ['campaigns.RECORD_DATA', 'DIM_AD_GROUP.created_at'],
    ['campaigns.RECORD_DATA', 'DIM_AD_GROUP.updated_at'],

    ['campaigns.APP_IDENTIFIER', 'METRICS.platform_id'],
    ['campaigns.RECORD_DATA', 'METRICS.account_id'],
    ['campaigns.RECORD_DATA', 'METRICS.campaign_id'],
    ['campaigns.RECORD_DATA', 'METRICS.currency_key'],

    ['campaigns.RECORD_DATA', 'DIM_CAMPAIGN.daily_budget'],
    ['campaigns.RECORD_DATA', 'DIM_CAMPAIGN.status'],
]
