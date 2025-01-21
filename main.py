from src.banner import banner
from src.client import EDAClient
from src.logging import setup_logging

setup_logging()


def main():
    eda = EDAClient(base_url="https://devbox.panda-cobra.ts.net")

    my_banner = banner(
        ns="clab-vlan",
        name="my-banner",
        motd_text="Let's have some model driven automation going on!",
    )
    eda.add_to_transaction_delete(my_banner)
    _ = eda.commit_transaction()


if __name__ == "__main__":
    main()
