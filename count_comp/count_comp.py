import os

import pyTigerGraph as tg
import argparse

def main():
    parser = argparse.ArgumentParser("TigerGraph count (and compare)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog = '''
Host names are combined from command line and file; file data overwrites command line data.

Format of file (JSON):

{
    "host1": {
        host: "<host>",
        graphname="<graphname>",
        username="<username>",
        password="<password>",
        restppPort="<restppPort>",
        gsPort="<gsPort>",
        apiToken="<gsPort>",
        secret="<secret>",
        gsqlVersion="<gsqlVersion>",
        useCert=<true_or_false>,
        certPath="<certPath>"
    },
    ...
}

All keys are options, defaults will be used for missing ones.
If `secret` is provided, `apiToken` will be ignored and new token will be requested.''')
    parser.add_argument("hosts", type=str, nargs="*", help="One or more hostnames")
    parser.add_argument("-f", "--file", type=str, help="Host file name; a JSON document describing hosts, see below")

    args = parser.parse_args()

    hosts = {}

    # Getting hosts from command line
    hostlist = args.hosts
    for h in hostlist:
        hosts[h] = {}

    # Getting hosts from config file
    if args.file:
        if not os.path.exists(args.file):
            print(f"ERROR: host file {args.file} cannot be found." )
            exit(1)
        hostfile

if __name__ == "__main__":
    main()

# EOF
