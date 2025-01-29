import logging
from typing import Any, List, Literal, Optional

import httpx
from pydantic import BaseModel
from pydantic_eda.core import (
    GroupVersionKind,
    NsCrGvkName,
    Transaction,
    TransactionContent,
    TransactionCr,
    TransactionDetails,
    TransactionId,
    TransactionType,
    TransactionValue,
)

# transaction types
_CREATE = "create"
_DELETE = "delete"
_MODIFY = "modify"
_REPLACE = "replace"
TxType = Literal["create", "delete", "modify", "replace"]

logger = logging.getLogger(__name__)

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

        super().__init__(headers=self.headers, verify=False)

        # acquire the token during initialization
        self.auth()

    def auth(self) -> None:
        """Authenticate and get access token"""
        logger.info("Authenticating with EDA API server")

        self.token = self._get_access_token()
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

    def add_to_transaction_create(self, resource: BaseModel) -> None:
        """Add resource to the create list of a transaction"""

        self.add_to_transaction(resource, _CREATE)

    def add_to_transaction_replace(self, resource: BaseModel) -> None:
        """Add resource to the replace list of a transaction"""

        self.add_to_transaction(resource, _REPLACE)

    def add_to_transaction_modify(self, resource: BaseModel) -> None:
        """Add resource to the modify list of a transaction"""

        self.add_to_transaction(resource, _MODIFY)

    def add_to_transaction_delete(self, resource: BaseModel) -> None:
        """Add resource to the delete list of a transaction"""

        self.add_to_transaction(resource, _DELETE)

    def add_to_transaction(self, resource: BaseModel, type: TxType) -> None:
        """Add resource to transaction"""

        # convert the resource instance of whatever actual type to a TransactionContent
        content = TransactionContent(
            **resource.model_dump(
                exclude_unset=True, exclude_none=True, exclude_defaults=True
            )
        )

        if (
            content.apiVersion is None
            or content.kind is None
            or content.metadata is None
        ):
            raise ValueError(
                f"Resource {content.apiVersion} {content.kind} is not a valid resource"
            )

        logger.info(
            f"Adding '{content.kind}' resource from '{content.apiVersion}' to the '{type}' transaction list"
        )

        tx_type_mapping = {
            "create": TransactionType(create=TransactionValue(value=content)),
            "delete": TransactionType(
                delete=NsCrGvkName(
                    gvk=GroupVersionKind(
                        group=content.apiVersion.split("/")[0],
                        version=content.apiVersion.split("/")[1],
                        kind=content.kind,
                    ),
                    name=content.metadata.name,
                    namespace=content.metadata.namespace,
                )
            ),
            "modify": TransactionType(modify=TransactionValue(value=content)),
            "replace": TransactionType(replace=TransactionValue(value=content)),
        }

        tx_cr = TransactionCr(type=tx_type_mapping[type])

        if self.transaction is None:
            self.transaction = Transaction(
                crs=[tx_cr],
                description="",
                dryRun=False,
            )
        else:
            self.transaction.crs.append(tx_cr)

    def commit_transaction(self) -> Any:
        """Commit transaction"""

        # convert the transaction instance to a dict
        if self.transaction is None:
            raise ValueError("No transaction to commit")

        self.transaction.retain = True
        self.transaction.resultType = "normal"

        content = self.transaction.model_dump_json(
            exclude_unset=True, exclude_none=True, exclude_defaults=True
        )

        # logger.info(f"Committing transaction: {content}")

        response = self.post(
            url=self.transaction_endpoint,
            content=content,
        )
        if response.status_code != 200:
            raise ValueError(response.text)

        tx_id: TransactionId = TransactionId(**response.json())
        if tx_id.id is None:
            raise ValueError(f"Transaction ID is None: {response.text}")

        logger.info(f"Transaction {tx_id.id} committed")

        tx_details: TransactionDetails = self.get_transaction_details(tx_id.id)
        errs = self.tx_must_succeed(tx_details)
        if errs:
            logger.error(f"Transaction {tx_id.id} errors:\n  - " + "\n  - ".join(errs))
        logger.info(f"Transaction {tx_id.id} state: {tx_details.state}")

    def get_transaction_details(self, tx_id: int) -> TransactionDetails:
        """Get transaction"""

        params = {
            "waitForComplete": "true",
            # "failOnErrors": "true"
        }
        response = self.get(
            url=f"{self.transaction_endpoint}/details/{tx_id}",
            params=params,
        )
        if response.status_code != 200:
            raise ValueError(response.text)

        # logger.info(f"Transaction {tx_id} details:\n{response.json()}")

        return TransactionDetails(**response.json())

    def _get_client_secret(self) -> str:
        client = self
        token_url = f"{self.kc_url}/realms/{KC_REALM}/protocol/openid-connect/token"
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
        admin_api_url = f"{self.kc_url}/admin/realms/{EDA_REALM}/clients"
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

    def _get_access_token(self) -> str:
        client_secret = self._get_client_secret()
        token_endpoint = (
            f"{self.kc_url}/realms/{EDA_REALM}/protocol/openid-connect/token"
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

        response = self.post(token_endpoint, data=token_data, headers=headers)
        response.raise_for_status()
        return response.json()["access_token"]

    def tx_must_succeed(self, tx_details: TransactionDetails) -> List[str] | None:
        """Check if transaction succeeded"""
        if not tx_details.success:
            return tx_details.generalErrors
