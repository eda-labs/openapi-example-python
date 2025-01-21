import logging

from rich import print
from rich.logging import RichHandler

from models.com.nokia.eda.interfaces.v1alpha1 import (
    Interface,
    Member,
    Metadata,
    SpecModel,
)
from src.banner import banner
from src.client import EDAClient

# Replace the basic logging config with Rich handler
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
)
logger = logging.getLogger(__name__)


def main():
    eda = EDAClient(base_url="https://devbox.panda-cobra.ts.net")

    my_banner = banner("This is a test banner")
    eda.add_to_transaction_create(my_banner)
    _ = eda.commit_transaction()

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
