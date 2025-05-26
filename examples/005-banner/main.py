import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

import pydantic_eda.apps.siteinfo.v1alpha1.models as siteinfo

from common.client import EDAClient
from common.logging import setup_logging

setup_logging()

NS = "eda"


def main():
    eda = EDAClient(base_url="https://devbox.netdevops.me:9444")

    my_banner = siteinfo.Banner(
        apiVersion="siteinfo.eda.nokia.com/v1alpha1",
        kind="Banner",
        metadata=siteinfo.BannerMetadata(
            namespace=NS,
            name="my-banner",
        ),
        spec=siteinfo.BannerSpec(
            loginBanner="Pydantic EDA says Hi",
            nodes=["leaf1"],
        ),
    )

    eda.add_to_transaction_create(my_banner)
    _ = eda.commit_transaction()


if __name__ == "__main__":
    main()
