from typing import Optional

import httpx
from pydantic import BaseModel, HttpUrl

from models.core import (
    Transaction,
    TransactionContent,
    TransactionCr,
    TransactionType,
    TransactionValue,
)

EDA_VERSION = "v24.12.1"

KC_REALM = "master"
KC_CLIENT_ID = "admin-cli"
KC_USERNAME = "admin"
KC_PASSWORD = "admin"
EDA_REALM = "eda"
API_CLIENT_ID = "eda"


class EDAClient(httpx.Client):
    def __init__(self, base_url: str):
        self.base_url: str = base_url
        self.kc_url: str = self.base_url.join("/core/httpproxy/v1/keycloak")

        self.headers: dict[str, str] = {}
        self.token: str = ""
        self.transaction: Optional[Transaction] = None
        self.transaction_endpoint: str = self.base_url.join("/core/transaction/v1")

        # acquire the token during initialization
        self.auth()
        super().__init__(headers=self.headers, verify=False)

    def auth(self) -> None:
        """Authenticate and get access token"""
        self.token = _get_access_token(self)
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def add_to_transaction_create(self, resource: BaseModel) -> None:
        """Add resource to transaction"""
        # convert the resource instance of whatever actual type to a TransactionContent
        content = TransactionContent(
            **resource.model_dump(exclude_unset=True, exclude_defaults=True)
        )

        if self.transaction is None:
            self.transaction = Transaction(
                crs=[
                    TransactionCr(
                        type=TransactionType(create=TransactionValue(value=content))
                    )
                ],
                description="",
                dryRun=False,
            )
        else:
            self.transaction.crs.append(
                TransactionCr(
                    type=TransactionType(create=TransactionValue(value=content))
                )
            )

    # def run_transaction(self) -> Any:
    #     """Run transaction"""
    #     # convert the transaction instance to a dict
    #     transaction_dict = self.transaction.model_dump(
    #         exclude_unset=True, exclude_defaults=True
    #     )


def _get_client_secret(kc_url: str) -> str:
    with httpx.Client(verify=False) as client:
        token_url = f"{kc_url}/realms/{KC_REALM}/protocol/openid-connect/token"
        token_data = {
            "grant_type": "password",
            "client_id": KC_CLIENT_ID,
            "username": KC_USERNAME,
            "password": KC_PASSWORD,
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}

        # Fetch access token
        token_response = client.post(token_url, data=token_data, headers=headers)
        token_response.raise_for_status()
        access_token = token_response.json()["access_token"]

        # Step 2: Fetch the `eda` client ID and secret
        admin_api_url = f"{kc_url}/admin/realms/{EDA_REALM}/clients"
        auth_headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # Fetch clients
        clients_response = client.get(admin_api_url, headers=auth_headers)
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
        secret_response = client.get(client_secret_url, headers=auth_headers)
        secret_response.raise_for_status()
        client_secret = secret_response.json()["value"]

        return client_secret


def _get_access_token(self: EDAClient) -> str:
    client_secret = _get_client_secret(self.kc_url)
    token_endpoint = f"{self.kc_url}/realms/{EDA_REALM}/protocol/openid-connect/token"

    token_data = {
        "client_id": API_CLIENT_ID,
        "grant_type": "password",
        "scope": "openid",
        "username": "admin",
        "password": "admin",
        "client_secret": client_secret,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    with httpx.Client(verify=False) as client:
        response = client.post(token_endpoint, data=token_data, headers=headers)
        response.raise_for_status()
        return response.json()["access_token"]
