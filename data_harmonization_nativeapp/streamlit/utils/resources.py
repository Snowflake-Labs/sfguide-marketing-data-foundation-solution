from utils.assets import image_b64


def SnowflakeIcon():
    return getImageString('Snowflake.png')

def SidebarLogo():
    return getImageString('SideBarLogo.png')

def getAirbyteLogo():
    return getImageString('airbyte.png')

def getOmnataLogo():
    return getImageString('omnata.png')

def get_gift_icon():
    return getImageString('icons/gift.png')

def get_hand_edit_icon():
    return getImageString('icons/hand_edit.png')

def get_cloud_upload_icon():
    return getImageString('icons/cloud_upload.svg')

def get_database_icon():
    return getImageString('icons/database.svg')

def get_cm_assistan_icon():
    return getImageString('icons/assistants/CMAssistantIcon.png')

def get_de_assistan_icon():
    return getImageString('icons/assistants/DEAssistantIcon.png')

# Gets providers icons

def get_facebook_icon():
    return getImageString('icons/providers/facebook.png')

def get_linkedin_icon():
    return getImageString('icons/providers/linkedin.png')

def get_salesforce_icon():
    return getImageString('icons/providers/salesforce.png')

def get_google_ads_icon():
    return getImageString('icons/providers/google.png')

# Gets connectors icons

def get_fivetran_icon():
    return getImageString('icons/connectors/fivetran.png')

def get_omnata_icon():
    return getImageString('icons/connectors/omnata.png')

def getImageString(image_name: str):
    return image_b64(image_name)
