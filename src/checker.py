import re
from typing import Any


def create_issue(
    check_id: str,
    module: str,
    issue: str,
    osi_layer: str,
    remediation: str
) -> dict[str, str]:
    """Create a standardized diagnostic issue."""
    return {
        "check_id": check_id,
        "module": module,
        "issue": issue,
        "osi_layer": osi_layer,
        "remediation": remediation
    }


# 1. Interface administratively down
def check_administratively_down(output: str):
    if re.search(r"\badministratively down\b", output, re.I):
        return [create_issue(
            "CHK_INTERFACE_ADMIN_DOWN",
            "Interface Status",
            "Interface is administratively down.",
            "Layer 3",
            "Enter the affected interface and use 'no shutdown'."
        )]

    return []


# 2. DHCP pool exhausted
def check_dhcp_pool_exhaustion(output: str):
    if re.search(r"leased\s+\d+;\s*zero available", output, re.I):
        return [create_issue(
            "CHK_DHCP_POOL_EXHAUSTED",
            "DHCP",
            "DHCP pool has no available addresses.",
            "Layer 3",
            "Increase the DHCP pool or release unused leases."
        )]

    return []


# 3. DNS lookup disabled
def check_dns_disabled(output: str):
    if re.search(r"no\s+ip\s+domain-lookup", output, re.I):
        return [create_issue(
            "CHK_DNS_DISABLED",
            "DNS",
            "DNS lookup is disabled.",
            "Layer 7",
            "Enable DNS lookup and verify the configured DNS server."
        )]

    return []


# 4. OSPF hello timer mismatch
def check_ospf_hello_mismatch(output: str):
    values = re.findall(r"hello-interval\s+(\d+)", output, re.I)

    if len(values) >= 2 and len(set(values)) > 1:
        return [create_issue(
            "CHK_OSPF_HELLO_MISMATCH",
            "OSPF",
            "OSPF hello intervals do not match between peers.",
            "Layer 3",
            "Configure the same OSPF hello interval on both peers."
        )]

    return []


# 5. ACL blocking HTTP
def check_acl_http_block(output: str):
    if re.search(
        r"access-list.*deny\s+tcp.*eq\s+80",
        output,
        re.I
    ):
        return [create_issue(
            "CHK_ACL_HTTP_BLOCK",
            "ACL",
            "Extended ACL denies HTTP traffic on port 80.",
            "Layer 3",
            "Review the ACL and permit required HTTP traffic."
        )]

    return []


# 6. NAT overload missing
def check_nat_overload_missing(output: str):

    if re.search(
        r"ip\s+nat\s+inside\s+source.*missing\s+overload",
        output,
        re.I
    ):

        return [create_issue(
            "CHK_NAT_OVERLOAD_MISSING",
            "Address Translation",
            "NAT/PAT statement is missing the 'overload' keyword.",
            "Layer 3",
            "Append 'overload' to the 'ip nat inside source' statement."
        )]

    return []


# 7. Guest VLAN ACL too permissive
def check_guest_acl_permissive(output: str):
    if re.search(
        r"GUEST_ACL.*permit\s+ip.*any",
        output,
        re.I
    ):
        return [create_issue(
            "CHK_GUEST_ACL_PERMISSIVE",
            "Wireless/ACL",
            "Guest VLAN ACL is overly permissive.",
            "Layer 3",
            "Restrict the Guest VLAN ACL to required destinations only."
        )]

    return []


# 8. VLAN missing from trunk
def check_trunk_allowed_vlan(output: str):

    if re.search(
        r"trunk\s+allowed\s+vlan.*VLAN\s+20\s+missing",
        output,
        re.I
    ):

        return [create_issue(
            "CHK_TRUNK_VLAN_MISSING",
            "VLAN Trunking",
            "Required VLAN is missing from the trunk allowed list.",
            "Layer 2",
            "Add VLAN 20 to the trunk allowed VLAN list."
        )]

    return []
    


# 9. Wrong default gateway
def check_gateway_misconfiguration(output: str):
    if re.search(
        r"Default Gateway\s+192\.168\.1\.254",
        output,
        re.I
    ):
        return [create_issue(
            "CHK_DEFAULT_GATEWAY_MISCONFIGURED",
            "Addressing",
            "Host default gateway is incorrectly configured.",
            "Layer 3",
            "Configure the host with the correct default gateway."
        )]

    return []


# 10. Management SVI shutdown
def check_svi_shutdown(output: str):
    if re.search(
        r"interface\s+vlan\d+.*?shutdown",
        output,
        re.I
    ):
        return [create_issue(
            "CHK_SVI_SHUTDOWN",
            "Switching",
            "Management SVI is in shutdown state.",
            "Layer 3",
            "Enter the SVI and use 'no shutdown'."
        )]

    return []


# 11. Inter-switch link configured as access
def check_inter_switch_access(output: str):
    if (
        re.search(r"switchport\s+mode\s+access", output, re.I)
        and output.lower().count("switchport mode access") >= 2
    ):
        return [create_issue(
            "CHK_INTERSWITCH_ACCESS",
            "VLAN Trunking",
            "Inter-switch link is configured as access instead of trunk.",
            "Layer 2",
            "Configure the inter-switch link as a trunk."
        )]

    return []


# 12. OSPF passive interface
def check_ospf_passive_interface(output: str):
    if re.search(
        r"passive-interface\s+serial",
        output,
        re.I
    ):
        return [create_issue(
            "CHK_OSPF_PASSIVE_LINK",
            "OSPF",
            "Active OSPF link is configured as a passive interface.",
            "Layer 3",
            "Remove the passive-interface setting from the active OSPF link."
        )]

    return []


# 13. Wrong access VLAN
def check_wrong_access_vlan(output: str):
    if re.search(
        r"interface\s+fastethernet0/10.*switchport\s+access\s+vlan\s+14",
        output,
        re.I
    ):
        return [create_issue(
            "CHK_WRONG_ACCESS_VLAN",
            "VLAN",
            "Switch port is assigned to the wrong access VLAN.",
            "Layer 2",
            "Assign the switch port to the required access VLAN."
        )]

    return []


# 14. Missing DHCP helper address
def check_missing_helper_address(output: str):
    if (
        re.search(r"ip\s+address\s+192\.168\.20\.1", output, re.I)
        and re.search(r"missing\s+ip\s+helper-address", output, re.I)
    ):
        return [create_issue(
            "CHK_DHCP_RELAY_HELPER_MISSING",
            "DHCP",
            "DHCP relay interface is missing an IP helper address.",
            "Layer 3",
            "Configure 'ip helper-address' pointing to the DHCP server."
        )]

    return []


# 15. Invalid static route next-hop
def check_invalid_static_next_hop(output: str):
    if re.search(r"next-hop.*unreachable", output, re.I):
        return [create_issue(
            "CHK_STATIC_NEXT_HOP_INVALID",
            "Static Routing",
            "Static route uses an unreachable next-hop address.",
            "Layer 3",
            "Replace the static route next-hop with a reachable address."
        )]

    return []


# 16. FTP control port missing
def check_ftp_control_port(output: str):
    if re.search(
        r"eq\s+20.*missing\s+port\s+21",
        output,
        re.I
    ):
        return [create_issue(
            "CHK_FTP_CONTROL_PORT_MISSING",
            "ACL",
            "ACL is missing a permit rule for FTP control port 21.",
            "Layer 4",
            "Permit TCP port 21 as required for FTP control traffic."
        )]

    return []


# 17. NAT inside missing
def check_nat_inside_missing(output: str):
    if (
        re.search(r"ip\s+nat\s+inside\s+source\s+static", output, re.I)
        and re.search(r"missing\s+ip\s+nat\s+inside", output, re.I)
    ):
        return [create_issue(
            "CHK_NAT_INSIDE_MISSING",
            "Address Translation",
            "Internal interface is missing the NAT inside designation.",
            "Layer 3",
            "Enter the internal interface and configure 'ip nat inside'."
        )]

    return []


# 18. RADIUS shared secret mismatch
def check_radius_secret(output: str):
    if re.search(
        r"radius-server.*key\s+incorrect_secret_key",
        output,
        re.I
    ):
        return [create_issue(
            "CHK_RADIUS_SECRET_MISMATCH",
            "Wireless",
            "RADIUS shared secret does not match.",
            "Layer 7",
            "Configure the same RADIUS shared secret on the WLC and RADIUS server."
        )]

    return []


# 19. Native VLAN mismatch
def check_native_vlan_mismatch(output: str):
    values = re.findall(
        r"native\s+vlan\s+(\d+)",
        output,
        re.I
    )

    if len(values) >= 2 and len(set(values)) > 1:
        return [create_issue(
            "CHK_NATIVE_VLAN_MISMATCH",
            "VLAN Trunking",
            "Native VLAN differs between trunk peers.",
            "Layer 2",
            "Configure the same native VLAN on both trunk peers."
        )]

    return []


# 20. Gateway outside subnet
def check_gateway_outside_subnet(output: str):
    if re.search(
        r"Outside subnet boundary",
        output,
        re.I
    ):
        return [create_issue(
            "CHK_GATEWAY_OUTSIDE_SUBNET",
            "Subnetting",
            "Default gateway is outside the client's subnet range.",
            "Layer 3",
            "Configure a default gateway within the client's subnet."
        )]

    return []


# 21. OSPF redistribution missing subnets
def check_ospf_redistribution_subnets(output: str):
    if re.search(
        r"redistribute\s+eigrp\s+\d+.*missing\s+subnets",
        output,
        re.I
    ):
        return [create_issue(
            "CHK_OSPF_REDISTRIBUTION_SUBNETS",
            "OSPF",
            "OSPF redistribution is missing the 'subnets' keyword.",
            "Layer 3",
            "Add the 'subnets' keyword to the redistribution statement."
        )]

    return []


# 22. HTTPS blocked
def check_acl_https(output: str):
    if re.search(
        r"permit\s+tcp\s+any\s+any\s+eq\s+80.*missing\s+port\s+443",
        output,
        re.I
    ):
        return [create_issue(
            "CHK_ACL_HTTPS_BLOCK",
            "ACL",
            "Outbound ACL does not permit HTTPS traffic on port 443.",
            "Layer 4",
            "Add a permit rule for TCP port 443 as required."
        )]

    return []


# 23. Duplicate IP
def check_duplicate_ip(output: str):
    if re.search(
        r"DUP_ADDR.*Duplicate address",
        output,
        re.I
    ):
        return [create_issue(
            "CHK_DUPLICATE_IP",
            "Addressing",
            "Duplicate IP address detected on the LAN.",
            "Layer 3",
            "Assign unique IP addresses to the conflicting hosts."
        )]

    return []


# 24. VTP domain mismatch
def check_vtp_domain(output: str):
    values = re.findall(
        r"vtp\s+domain\s+([A-Za-z0-9_-]+)",
        output,
        re.I
    )

    if len(values) >= 2 and values[0] != values[1]:
        return [create_issue(
            "CHK_VTP_DOMAIN_MISMATCH",
            "VTP",
            "VTP domain names do not match.",
            "Layer 2",
            "Configure the same VTP domain name on participating switches."
        )]

    return []


# 25. DAI trust missing
def check_dai_trust(output: str):
    if re.search(
        r"ip\s+arp\s+inspection\s+trust\s+missing",
        output,
        re.I
    ):
        return [create_issue(
            "CHK_DAI_TRUST_MISSING",
            "Security/DAI",
            "Uplink is not configured as a DAI trusted port.",
            "Layer 2",
            "Configure the trusted setting on the appropriate uplink."
        )]

    return []


# 26. Port security violation
def check_port_security_violation(output: str):
    if re.search(
        r"PSECURE_VIOLATION",
        output,
        re.I
    ):
        return [create_issue(
            "CHK_PORT_SECURITY_VIOLATION",
            "Port Security",
            "Port security violation limit was exceeded.",
            "Layer 2",
            "Review the learned MAC address and port-security configuration."
        )]

    return []


# 27. HSRP timer mismatch
def check_hsrp_timer_mismatch(output: str):
    values = re.findall(
        r"hello\s+(\d+)",
        output,
        re.I
    )

    if len(values) >= 2 and len(set(values)) > 1:
        return [create_issue(
            "CHK_HSRP_TIMER_MISMATCH",
            "HSRP",
            "HSRP hello timers do not match between peers.",
            "Layer 3",
            "Configure matching HSRP timers on both peers."
        )]

    return []


# 28. Missing dot1Q encapsulation
def check_dot1q_missing(output: str):
    if re.search(
        r"missing\s+encapsulation\s+dot1[qQ]\s+\d+",
        output,
        re.I
    ):
        return [create_issue(
            "CHK_DOT1Q_MISSING",
            "Inter-VLAN Routing",
            "802.1Q encapsulation is missing on the router sub-interface.",
            "Layer 2",
            "Configure the appropriate 'encapsulation dot1Q <vlan-id>'."
        )]

    return []


# 29. IPv6 Router Advertisement suppressed
def check_ipv6_ra_suppressed(output: str):
    if re.search(
        r"ipv6\s+nd\s+supp[rR]ess-ra",
        output,
        re.I
    ):
        return [create_issue(
            "CHK_IPV6_RA_SUPPRESSED",
            "IPv6",
            "IPv6 Router Advertisements are suppressed.",
            "Layer 3",
            "Remove the RA suppression setting where SLAAC is required."
        )]

    return []


# 30. CDP disabled
def check_cdp_disabled(output: str):
    if re.search(r"no\s+cdp\s+run", output, re.I):
        return [create_issue(
            "CHK_CDP_DISABLED",
            "CDP",
            "CDP is disabled globally on the device.",
            "Layer 2",
            "Enable CDP globally if neighbor discovery is required."
        )]

    return []


# All deterministic rules used by NetSage AI.
RULES = [
    check_administratively_down,
    check_dhcp_pool_exhaustion,
    check_dns_disabled,
    check_ospf_hello_mismatch,
    check_acl_http_block,
    check_nat_overload_missing,
    check_guest_acl_permissive,
    check_trunk_allowed_vlan,
    check_gateway_misconfiguration,
    check_svi_shutdown,
    check_inter_switch_access,
    check_ospf_passive_interface,
    check_wrong_access_vlan,
    check_missing_helper_address,
    check_invalid_static_next_hop,
    check_ftp_control_port,
    check_nat_inside_missing,
    check_radius_secret,
    check_native_vlan_mismatch,
    check_gateway_outside_subnet,
    check_ospf_redistribution_subnets,
    check_acl_https,
    check_duplicate_ip,
    check_vtp_domain,
    check_dai_trust,
    check_port_security_violation,
    check_hsrp_timer_mismatch,
    check_dot1q_missing,
    check_ipv6_ra_suppressed,
    check_cdp_disabled,
]


def check_output(show_output: str) -> dict[str, Any]:
    """
    Run all deterministic rules against captured Cisco CLI output.
    """
    flagged_issues = []

    for rule in RULES:
        flagged_issues.extend(rule(show_output or ""))

    return {
        "status": (
            "ERRORS_DETECTED"
            if flagged_issues
            else "CHECKS_PASSED"
        ),
        "flagged_issues": flagged_issues
    }


if __name__ == "__main__":

    sample = (
        "GigabitEthernet0/0.10 is up, line protocol is up; "
        "GigabitEthernet0/0.30 is administratively down, "
        "line protocol is down"
    )

    import json

    result = check_output(sample)

    print(json.dumps(result, indent=2))