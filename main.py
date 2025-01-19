import logging

from models.com.nokia.eda.interfaces.v1alpha1 import (
    Interface,
    Member,
    Metadata,
    SpecModel,
)
from src.client import Client

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    c = Client(base_url="https://devbox.panda-cobra.ts.net")
    c.auth()
    logger.info(f"Access Token: {c.token}")

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
