import pydantic_eda.apps.services.v1.models as service


def virtualnetwork(ns: str, name: str) -> service.VirtualNetwork:
    ...
    # create a virtual network
