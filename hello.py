import asyncio

from models.com.nokia.eda.interfaces.v1alpha1 import (
    Interface,
    Member,
    Metadata,
    SpecModel,
)
from src import auth


async def get_api_token():
    client_secret = await auth.get_client_secret()
    access_token = await auth.get_access_token(client_secret)
    print(f"Access Token: {access_token}")


def main():
    # Run the asynchronous function
    asyncio.run(get_api_token())

    # iface = Interface(
    #     apiVersion="interfaces.eda.nokia.com/v1alpha1",
    #     kind="Interface",
    #     metadata=Metadata(
    #         name="test",
    #         namespace="clab-vlan",
    #         labels={"app": "test"},
    #     ),
    #     spec=SpecModel(
    #         description="This is a test interface",
    #         enabled=True,
    #         members=[
    #             Member(
    #                 node="leaf1",
    #                 interface="ethernet-1-1",
    #             )
    #         ]
    #     )
    # )
    # print(iface.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
