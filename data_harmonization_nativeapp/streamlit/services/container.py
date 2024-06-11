
def is_service_active(sp_session) -> bool:
    services = sp_session.sql('SHOW services;').collect()
    return len(services) > 0


def get_endpoint(sp_session) -> str:
    endpoint_query = sp_session.sql(f"SHOW ENDPOINTS IN SERVICE CORE.FRONTEND_SERVICE;").collect()
    return endpoint_query[0]['ingress_url']


def start_service(sp_session):
    compute_pool = get_compute_pool()
    start_query = f"CALL CONFIG.start_app('{compute_pool}');"
    sp_session.sql(start_query).collect()


def stop_service(sp_session):
    compute_pool = get_compute_pool()
    stop_query = f"ALTER COMPUTE POOL {compute_pool} STOP ALL;"
    sp_session.sql(stop_query).collect()


def get_compute_pool():
    # TODO get compute pool from config file
    return 'DATA_HARMONIZATION_COMPUTE_POOL'
