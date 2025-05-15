import pydantic_eda.apps.services.v1alpha1.models as service


def virtualnetwork(ns: str, id: int) -> service.VirtualNetwork:
    router = service.VirtualNetworkSpecRouter(
        name=f"vnet-router-{id}",
        spec=service.VirtualNetworkSpecRouterSpec(
            eviPool="evi-pool",
            tunnelIndexPool="tunnel-index-pool",
            type="EVPNVXLAN",
            vniPool="vni-pool",
        ),
    )

    bd = service.VirtualNetworkSpecBridgeDomain(
        name=f"vnet-bridge-domain-{id}",
        spec=service.VirtualNetworkSpecBridgeDomainSpec(
            eviPool="evi-pool",
            tunnelIndexPool="tunnel-index-pool",
            type="EVPNVXLAN",
            vniPool="vni-pool",
        ),
    )

    vlan = service.VirtualNetworkSpecVlan(
        name=f"vnet-vlan-{id}",
        spec=service.VirtualNetworkSpecVlanSpec(
            bridgeDomain=bd.name,
            interfaceSelector=["edge-type=compute"],
            uplink=service.VirtualNetworkSpecVlanSpecUplink(uplinkVLANID="pool"),
            vlanID=str(300 + id),
        ),
    )

    irb = service.VirtualNetworkSpecIrbInterface(
        name=f"vnet-irb-{id}",
        spec=service.VirtualNetworkSpecIrbInterfaceSpec(
            bridgeDomain=bd.name,
            hostRoutePopulate=service.VirtualNetworkSpecIrbInterfaceSpecHostRoutePopulate(
                dynamic=True, static=True
            ),
            ipAddresses=[
                service.VirtualNetworkSpecIrbInterfaceSpecIpAddress(
                    ipv4Address=service.VirtualNetworkSpecIrbInterfaceSpecIpAddressIpv4Address(
                        ipPrefix="10.30.0.1/24", primary=True
                    )
                ),
                service.VirtualNetworkSpecIrbInterfaceSpecIpAddress(
                    ipv6Address=service.VirtualNetworkSpecIrbInterfaceSpecIpAddressIpv6Address(
                        ipPrefix="fd00:fdfd:0:3000::1/64", primary=True
                    )
                ),
            ],
            router=router.name,
        ),
    )

    vnet = service.VirtualNetwork(
        apiVersion="services.eda.nokia.com/v1alpha1",
        kind="VirtualNetwork",
        metadata=service.VirtualNetworkMetadata(
            name=f"vnet-api-example-{id}",
            namespace=ns,
            labels={"role": "pydantic-example"},
        ),
        spec=service.VirtualNetworkSpec(
            routers=[
                router,
            ],
            bridgeDomains=[
                bd,
            ],
            vlans=[
                vlan,
            ],
            irbInterfaces=[
                irb,
            ],
        ),
    )

    return vnet
