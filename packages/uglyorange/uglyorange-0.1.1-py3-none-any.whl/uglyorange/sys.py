#!/usr/bin/env python3
import argparse
import codefast as cf
import sys
from .install.ttyd import ttyd_config
from .install.app import app_install
from .install.python import python_install
from .install.supervisor import supervisor_config
from .install.swap import swap_config


def vpsinit():
    """
    VPS initialization tool with selective installation options:
    -all: Install everything
    -app: Install system applications
    -python: Install Python packages
    -supervisor: Install and configure supervisor
    -docker: Install Docker
    -ttyd: Configure TTYD with supervisor
    """
    parser = argparse.ArgumentParser(description='VPS initialization tool')
    parser.add_argument('-all', action='store_true', help='Install everything')
    parser.add_argument('-app', action='store_true',
                        help='Install system applications')
    parser.add_argument('-python', action='store_true',
                        help='Install Python packages')
    parser.add_argument('-supervisor', action='store_true',
                        help='Install supervisor')
    parser.add_argument('-ttyd', action='store_true',
                        help='Configure TTYD with supervisor')
    parser.add_argument('-swap', action='store_true',
                        help='Configure swap size in GB')

    # If no arguments provided, print help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # Install everything if -all is specified
    install_all = args.all

    if install_all or args.app:
        app_install()
    if install_all or args.python:
        python_install()
    if install_all or args.supervisor:
        supervisor_config()
    if install_all or args.ttyd:
        ttyd_config()
    if install_all or args.swap:
        swap_config(args.swap)
