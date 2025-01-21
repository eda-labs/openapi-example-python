from src.banner import banner
from src.client import EDAClient
from src.interface import interface
from src.logging import setup_logging

setup_logging()


def main():
    my_banner = banner(
        ns="clab-vlan",
        name="my-banner",
        motd_text="Let's have some model driven automation going on!",
    )
    my_interface = interface(ns="clab-vlan", name="my-interface")

    eda = EDAClient(base_url="https://devbox.panda-cobra.ts.net")
    # eda.add_to_transaction_delete(my_banner)
    eda.add_to_transaction_replace(my_interface)
    _ = eda.commit_transaction()


if __name__ == "__main__":
    main()
