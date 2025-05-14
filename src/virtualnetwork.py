import pydantic_eda.apps.services.v1alpha1.models as service

router = service.VirtualNetworkSpecRouter(
    name="vnet-router",
    spec=service.VirtualNetworkSpecRouterSpec(
        eviPool="evi-pool",
        tunnelIndexPool="tunnel-index-pool",
        type="EVPNVXLAN",
        vniPool="vni-pool",
    ),
)

bd_300 = service.VirtualNetworkSpecBridgeDomain(
    name="vnet-bridge-domain-300",
    spec=service.VirtualNetworkSpecBridgeDomainSpec(
        eviPool="evi-pool",
        tunnelIndexPool="tunnel-index-pool",
        type="EVPNVXLAN",
        vniPool="vni-pool",
    ),
)

vlan_300 = service.VirtualNetworkSpecVlan(
    name="vnet-vlan-300",
    spec=service.VirtualNetworkSpecVlanSpec(
        bridgeDomain=bd_300.name,
        interfaceSelector=["edge-type=compute"],
        uplink=service.VirtualNetworkSpecVlanSpecUplink(uplinkVLANID="pool"),
        vlanID="300",
    ),
)


bd_312 = service.VirtualNetworkSpecBridgeDomain(
    name="vnet-bridge-domain-312",
    spec=service.VirtualNetworkSpecBridgeDomainSpec(
        eviPool="evi-pool",
        tunnelIndexPool="tunnel-index-pool",
        type="EVPNVXLAN",
        vniPool="vni-pool",
    ),
)

vlan_312 = service.VirtualNetworkSpecVlan(
    name="vnet-vlan-312",
    spec=service.VirtualNetworkSpecVlanSpec(
        bridgeDomain=bd_312.name,
        interfaceSelector=["edge-type=compute"],
        uplink=service.VirtualNetworkSpecVlanSpecUplink(uplinkVLANID="pool"),
        vlanID="312",
    ),
)

irb_300 = service.VirtualNetworkSpecIrbInterface(
    name="vnet-irb-300",
    spec=service.VirtualNetworkSpecIrbInterfaceSpec(
        bridgeDomain=bd_300.name,
        hostRoutePopulate=service.VirtualNetworkSpecIrbInterfaceSpecHostRoutePopulate(dynamic=True, static=True),
        ipAddresses=[
            service.VirtualNetworkSpecIrbInterfaceSpecIpAddress(
                ipv4Address=service.VirtualNetworkSpecIrbInterfaceSpecIpAddressIpv4Address(ipPrefix="10.30.0.1/24", primary=True)
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

irb_312 = service.VirtualNetworkSpecIrbInterface(
    name="vnet-irb-312",
    spec=service.VirtualNetworkSpecIrbInterfaceSpec(
        bridgeDomain=bd_312.name,
        hostRoutePopulate=service.VirtualNetworkSpecIrbInterfaceSpecHostRoutePopulate(dynamic=True, static=True),
        ipAddresses=[
            service.VirtualNetworkSpecIrbInterfaceSpecIpAddress(
                ipv4Address=service.VirtualNetworkSpecIrbInterfaceSpecIpAddressIpv4Address(ipPrefix="10.30.2.1/24", primary=True)
            ),
            service.VirtualNetworkSpecIrbInterfaceSpecIpAddress(
                ipv6Address=service.VirtualNetworkSpecIrbInterfaceSpecIpAddressIpv6Address(
                    ipPrefix="fd00:fdfd:0:3002::1/64", primary=True
                )
            ),
        ],
        router=router.name,
    ),
)


routed_if_client11 = service.VirtualNetworkSpecRoutedInterface(
    name="vnet-routed-interface-client11",
    spec=service.VirtualNetworkSpecRoutedInterfaceSpec(
        interface="leaf11-client11",
        ipv4Addresses=[service.VirtualNetworkSpecRoutedInterfaceSpecIpv4Address(ipPrefix="10.30.1.1/24", primary=True)],
        ipv6Addresses=[
            service.VirtualNetworkSpecRoutedInterfaceSpecIpv6Address(ipPrefix="fd00:fdfd:0:3001::1/64", primary=True)
        ],
        router=router.name,
        vlanID="311",
        vlanPool="vlan-pool",
    ),
)

routed_if_client13 = service.VirtualNetworkSpecRoutedInterface(
    name="vnet-routed-interface-client13",
    spec=service.VirtualNetworkSpecRoutedInterfaceSpec(
        interface="leaf13-client13",
        ipv4Addresses=[service.VirtualNetworkSpecRoutedInterfaceSpecIpv4Address(ipPrefix="10.30.3.1/24", primary=True)],
        ipv6Addresses=[
            service.VirtualNetworkSpecRoutedInterfaceSpecIpv6Address(ipPrefix="fd00:fdfd:0:3003::1/64", primary=True)
        ],
        router=router.name,
        vlanID="313",
        vlanPool="vlan-pool",
    ),
)


def virtualnetwork(ns: str, name: str) -> service.VirtualNetwork:
    vnet = service.VirtualNetwork(
        apiVersion="services.eda.nokia.com/v1alpha1",
        kind="VirtualNetwork",
        metadata=service.VirtualNetworkMetadata(name=name, namespace=ns, labels={"role": "exercise"}),
        spec=service.VirtualNetworkSpec(
            routers=[
                router,
            ],
            routedInterfaces=[
                routed_if_client11,
                routed_if_client13,
            ],
            bridgeDomains=[
                bd_300,
                bd_312,
            ],
            vlans=[
                vlan_300,
                vlan_312,
            ],
            irbInterfaces=[
                irb_300,
                irb_312,
            ],
        ),
    )

    return vnet
