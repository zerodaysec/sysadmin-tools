"""py_dns script."""

import dns
import dns.resolver

VERSION = "1.0.0"

print("\n\n*** Starting DNS Checker {} ***\n".format(VERSION))


def get_mx(domain):
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

import sys

get_mx(sys.argv[0])
