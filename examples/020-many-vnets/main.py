import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from vnet import virtualnetwork

from common.client import EDAClient
from common.logging import setup_logging

setup_logging()

NS = "eda"


def main():
    num_vnets = 100

    eda = EDAClient(base_url="https://1.dev.srexperts.net:9443")

    for i in range(num_vnets):
        my_vnet = virtualnetwork(ns=NS, id=i)

        eda.add_to_transaction_create(my_vnet)

    _ = eda.commit_transaction()


if __name__ == "__main__":
    main()
