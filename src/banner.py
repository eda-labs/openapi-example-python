from models.com.nokia.eda.siteinfo.v1alpha1 import Banner, Metadata, Spec


def banner(motd_text: str) -> Banner:
    """
    Create a banner
    """

    banner = Banner(
        apiVersion="siteinfo.eda.nokia.com/v1alpha1",
        kind="Banner",
        metadata=Metadata(
            name="banner",
            namespace="clab-vlan",
            labels={"app": "banner"},
        ),
        spec=Spec(motd=motd_text, nodeSelector=["containerlab=managed"]),
    )

    return banner
