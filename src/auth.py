import httpx

# Keycloak configuration
EDA_API_URL = "https://devbox.panda-cobra.ts.net"
EDA_VERSION = "v24.12.1"
KC_KEYCLOAK_URL = f"{EDA_API_URL}/core/httpproxy/v1/keycloak/"
KC_REALM = "master"
KC_CLIENT_ID = "admin-cli"
KC_USERNAME = "admin"
KC_PASSWORD = "admin"
EDA_REALM = "eda"
API_CLIENT_ID = "eda"

# Step 1: Get an access token
token_url = f"{KC_KEYCLOAK_URL}/realms/{KC_REALM}/protocol/openid-connect/token"
token_data = {
    "grant_type": "password",
    "client_id": KC_CLIENT_ID,
    "username": KC_USERNAME,
    "password": KC_PASSWORD,
}
headers = {"Content-Type": "application/x-www-form-urlencoded"}


async def get_client_secret() -> str:
    async with httpx.AsyncClient(verify=False) as client:
        # Fetch access token
        token_response = await client.post(token_url, data=token_data, headers=headers)
        token_response.raise_for_status()
        access_token = token_response.json()["access_token"]

        # Step 2: Fetch the `eda` client ID and secret
        admin_api_url = f"{KC_KEYCLOAK_URL}/admin/realms/{EDA_REALM}/clients"
        auth_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # Fetch clients
        clients_response = await client.get(admin_api_url, headers=auth_headers)
        clients_response.raise_for_status()
        clients = clients_response.json()

        # Find the `eda` client
        eda_client = next(
            (client for client in clients if client["clientId"] == API_CLIENT_ID), None
        )

        if not eda_client:
            raise Exception("Client `eda` not found in realm `eda-realm`")

        # Fetch the client secret
        client_id = eda_client["id"]
        client_secret_url = f"{admin_api_url}/{client_id}/client-secret"
        secret_response = await client.get(client_secret_url, headers=auth_headers)
        secret_response.raise_for_status()
        client_secret = secret_response.json()["value"]

        return client_secret


async def get_access_token(client_secret: str) -> str:
    token_endpoint = (
        f"{KC_KEYCLOAK_URL}/realms/{EDA_REALM}/protocol/openid-connect/token"
    )

    token_data = {
        "client_id": API_CLIENT_ID,
        "grant_type": "password",
        "scope": "openid",
        "username": "admin",
        "password": "admin",
        "client_secret": client_secret,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(token_endpoint, data=token_data, headers=headers)
        response.raise_for_status()
        return response.json()["access_token"]
