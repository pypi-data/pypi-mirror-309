#!/usr/bin/env python3
import argparse
import codefast as cf
import sys
from .install.ttyd import ttyd_config
from .install.app import app_install
from .install.python import python_install
from .install.supervisor import supervisor_config
from .install.swap import swap_config
from .install.endlessh import endlessh_config
from .install.trojan import trojan_config


def vpsinit():
    """
    VPS initialization tool with selective installation options:
    -all: Install everything
    -app: Install system applications
    -python: Install Python packages
    -supervisor: Install and configure supervisor
    -docker: Install Docker
    -ttyd: Configure TTYD with supervisor
    -trojan: Install and configure Trojan proxy
    """
    parser = argparse.ArgumentParser(description='VPS initialization tool')
    parser.add_argument('-app', action='store_true',
                        help='Install system applications')
    parser.add_argument('-python', action='store_true',
                        help='Install Python packages')
    parser.add_argument('-supervisor', action='store_true',
                        help='Install supervisor')
    parser.add_argument('-ttyd', action='store_true',
                        help='Configure TTYD with supervisor')
    parser.add_argument('-endlessh', action='store_true',
                        help='Configure endlessh')
    parser.add_argument('-swap', type=int, metavar='SIZE',
                        help='Configure swap size in GB')
    parser.add_argument('-trojan', nargs=2, metavar=('DOMAIN', 'PASSWORD'),
                        help='Install Trojan proxy (requires domain and password)')

    # If no arguments provided, print help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()
    if args.app:
        app_install()
    if args.python:
        python_install()
    if args.supervisor:
        supervisor_config()
    if args.ttyd:
        ttyd_config()
    if args.endlessh:
        endlessh_config()
    if args.swap is not None:
        swap_config(args.swap or 2)
    if args.trojan:
        trojan_config(domain=args.trojan[0], password=args.trojan[1])
