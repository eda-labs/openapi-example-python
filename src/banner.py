from models.com.nokia.eda.siteinfo.v1alpha1 import Banner, Metadata, Spec

API_VERSION = "siteinfo.eda.nokia.com/v1alpha1"
KIND = "Banner"


def banner(ns: str, name: str, motd_text: str) -> Banner:
    """
    Create a banner
    """

    banner = Banner(
        apiVersion=API_VERSION,
        kind=KIND,
        metadata=Metadata(
            name=name,
            namespace=ns,
            labels={"app": "banner"},
        ),
        spec=Spec(motd=motd_text, nodeSelector=["containerlab=managed"]),
    )

    return banner
