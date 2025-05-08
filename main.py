from src.client import EDAClient
from src.virtualnetwork import virtualnetwork
from src.logging import setup_logging

setup_logging()


def main():
    eda = EDAClient(base_url="https://YOUR_EDA_EXT_DOMAIN_NAME:PORT")
    
    my_virtualnetwork = 

    eda.add_to_transaction_create(my_virtualnetwork)
    eda.commit_transaction()


if __name__ == "__main__":
    main()
