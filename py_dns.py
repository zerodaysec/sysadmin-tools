"""py_dns script."""

import dns
import dns.resolver

VERSION = "1.0.0"

print("\n\n*** Starting DNS Checker {} ***\n".format(VERSION))


def get_mx(
    domain,
):
    """get_mx record."""
    print(f"- Checking {domain}...")
    result = dns.resolver.resolve(
        domain,
        "MX",
    )
    for ipval in result:
        print(
            "IP",
            ipval.to_text(),
        )

    print(f"########################################\n{domain}")


get_mx("rackspace.com")
get_mx("zer0day.net")
