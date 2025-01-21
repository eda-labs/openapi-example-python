import models.com.nokia.eda.interfaces.v1alpha1 as iface


def interface(ns: str, name: str) -> iface.Interface:
    iface_ = iface.Interface(
        apiVersion="interfaces.eda.nokia.com/v1alpha1",
        kind="Interface",
        metadata=iface.Metadata(
            name=name,
            namespace=ns,
        ),
        spec=iface.SpecModel(
            description="This is a test interface",
            mtu=1500,
            members=[
                iface.Member(
                    interface="ethernet-1-1",
                    node="srl1",
                ),
            ],
        ),
    )

    return iface_
