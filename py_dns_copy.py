"""py_dns script."""

import dns.resolver
import pandas as pd
import time
import sys

pd.__version__
dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers = ["8.8.8.8"]
filename = "emails.txt"
filename2 = "emails2.txt"
# loading the file. This is just a simple file with email addresses
# consecutive lines
try:
    print(
        "Trying to open file ",
        filename,
    )
    with open(filename) as f:
        domains = [line.rstrip() for line in f]
except:
    print(f"Error while loading{filename}")
    sys.exit("IO error")
else:
    print(
        len(domains),
        "addresses loaded...starting mx lookup.\n\n",
    )
    print(
        domains,
        "",
    )

time.sleep(1)

mxRecords = []
emailAddresses = []
# we use domain.split("@",1)[1] to separate the domain from the email
# addresses the try-catch is necessary to avoid stopping th execution
# when a lookup fails.
for domain in domains:
    try:
        answers = dns.resolver.resolve(
            domain.split(
                "@",
                1,
            )[1],
            "MX",
        )
    except:
        print("some error")
        mxRecord = "some error"
    else:
        print(len(answers))
        mxRecord = answers
        for rec in answers:
            print(rec.resolver.resolve())
    finally:
        mxRecords.append(mxRecord)
        emailAddresses.append(domain)
        print(domain)
        print(mxRecords)
        time.sleep(0.200)
# a 200 ms pause is added for good measure
# the rest of the program uses pandas to export everything neatly to CSV.
# It takes to lists "mxRecords" and "emailAddresses" and converts it to
# a dataframe.
df = pd.DataFrame(
    {
        "EmailAddress": emailAddresses,
        "MXRecords": mxRecords,
    }
)
print(
    "\n",
    str(len(emailAddresses)),
    "records processed",
)
df.to_csv(
    filename2,
    index=False,
)
