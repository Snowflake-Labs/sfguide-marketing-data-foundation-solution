import streamlit as st
from services.session import session
from services.container import is_service_active, start_service, get_endpoint, stop_service


@st.cache_resource
def connect_to_snowflake():
    return session()


def main():
    sp_session = connect_to_snowflake()

    st.title('Marketing Data Foundation')
    
    if is_service_active(sp_session):
        endpoint = get_endpoint(sp_session)
        is_ready = not endpoint.startswith('Endpoints provisioning in progress')
        st.subheader('Container service endpoint:')
        if is_ready:
            st.markdown(f'[{endpoint}](https://{endpoint})')
            st.button('Stop service', on_click=stop_service, args=[sp_session])
        else:
            st.write(endpoint)
            st.button('Refresh')
    else:
        st.write('App service is not active')
        st.button('Start service', type='primary', on_click=start_service, args=[sp_session])

    

if __name__ == '__main__':
    main()
