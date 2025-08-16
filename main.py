from src.client import EDAClient
from src.logging import setup_logging
from src.virtualnetwork import virtualnetwork

setup_logging()


def main():
    eda = EDAClient(
        base_url="https://<your_group_id>.srexperts.net:9443",
        username="admin",
        password="<fill in the password>",
    )
    my_virtualnetwork = virtualnetwork(ns="eda", name="my-vnet-using-python")
    eda.add_to_transaction_create(my_virtualnetwork)
    eda.commit_transaction()


if __name__ == "__main__":
    main()
