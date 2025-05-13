import pydantic_eda.com.nokia.eda.services.v1alpha1 as service

router = service.Router(
    name="vnet-router",
    spec=service.SpecModel15(
        eviPool="evi-pool",
        tunnelIndexPool="tunnel-index-pool",
        type="EVPNVXLAN",
        vniPool="vni-pool",
    ),
)

bd_300 = service.BridgeDomain(
    name="vnet-bridge-domain-300",
    spec=service.SpecModel6(
        eviPool="evi-pool",
        tunnelIndexPool="tunnel-index-pool",
        type="EVPNVXLAN",
        vniPool="vni-pool",
    ),
)

vlan_300 = service.Vlan(
    name="vnet-vlan-300",
    spec=service.SpecModel16(
        bridgeDomain="vnet-bridge-domain-300",
        interfaceSelector=["edge-type=compute"],
        uplink=service.Uplink(uplinkVLANID="pool"),
        vlanID="300",
    ),
)


bd_312 = service.BridgeDomain(
    name="vnet-bridge-domain-312",
    spec=service.SpecModel6(
        eviPool="evi-pool",
        tunnelIndexPool="tunnel-index-pool",
        type="EVPNVXLAN",
        vniPool="vni-pool",
    ),
)

vlan_312 = service.Vlan(
    name="vnet-vlan-312",
    spec=service.SpecModel16(
        bridgeDomain="vnet-bridge-domain-312",
        interfaceSelector=["edge-type=compute"],
        uplink=service.Uplink(uplinkVLANID="pool"),
        vlanID="312",
    ),
)

irb_300 = service.IrbInterface(
    name="vnet-irb-300",
    spec=service.SpecModel8(
        bridgeDomain="vnet-bridge-domain-300",
        hostRoutePopulate=service.HostRoutePopulate(dynamic=True, static=True),
        ipAddresses=[
            service.IpAddress(
                ipv4Address=service.Ipv4Address(ipPrefix="10.30.0.1/24", primary=True)
            ),
            service.IpAddress(
                ipv6Address=service.Ipv6Address(
                    ipPrefix="fd00:fdfd:0:3000::1/64", primary=True
                )
            ),
        ],
        router="vnet-router",
    ),
)

irb_312 = service.IrbInterface(
    name="vnet-irb-312",
    spec=service.SpecModel8(
        bridgeDomain="vnet-bridge-domain-312",
        hostRoutePopulate=service.HostRoutePopulate(dynamic=True, static=True),
        ipAddresses=[
            service.IpAddress(
                ipv4Address=service.Ipv4Address(ipPrefix="10.30.2.1/24", primary=True)
            ),
            service.IpAddress(
                ipv6Address=service.Ipv6Address(
                    ipPrefix="fd00:fdfd:0:3002::1/64", primary=True
                )
            ),
        ],
        router="vnet-router",
    ),
)


routed_if_client11 = service.RoutedInterface(
    name="vnet-routed-interface-client11",
    spec=service.SpecModel14(
        interface="leaf11-client11",
        ipv4Addresses=[service.Ipv4Address(ipPrefix="10.30.1.1/24", primary=True)],
        ipv6Addresses=[
            service.Ipv6Address(ipPrefix="fd00:fdfd:0:3001::1/64", primary=True)
        ],
        router="vnet-router",
        vlanID="311",
        vlanPool="vlan-pool",
    ),
)

routed_if_client13 = service.RoutedInterface(
    name="vnet-routed-interface-client13",
    spec=service.SpecModel14(
        interface="leaf13-client13",
        ipv4Addresses=[service.Ipv4Address(ipPrefix="10.30.3.1/24", primary=True)],
        ipv6Addresses=[
            service.Ipv6Address(ipPrefix="fd00:fdfd:0:3003::1/64", primary=True)
        ],
        router="vnet-router",
        vlanID="313",
        vlanPool="vlan-pool",
    ),
)


def virtualnetwork(ns: str, name: str) -> service.VirtualNetwork:
    vnet = service.VirtualNetwork(
        apiVersion="services.eda.nokia.com/v1alpha1",
        kind="VirtualNetwork",
        metadata=service.VirtualNetworkMetadata(name=name, namespace=ns, labels={"role": "exercise"}),
        spec=service.SpecModel17(
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
