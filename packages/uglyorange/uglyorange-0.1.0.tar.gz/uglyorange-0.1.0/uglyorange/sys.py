#!/usr/bin/env python3
from abc import ABC, abstractmethod
import argparse
import os
import shutil
import codefast as cf
import subprocess
import sys


class SafelyFileRemover(argparse.ArgumentParser):
    def __init__(self):
        super().__init__(description='remove file or directory safely')
        self.add_argument('paths', nargs='+',
                          help='files or directories to remove')

    def remove_file_or_dir(self, paths: list):
        for path in paths:
            if os.path.exists(path):
                base_name = os.path.basename(path)
                tmp_path = os.path.join('/tmp', base_name)

                if os.path.isfile(path):
                    shutil.move(path, tmp_path)
                    cf.info(f"File {path} moved to {tmp_path}")
                elif os.path.isdir(path):
                    shutil.move(path, tmp_path)
                    cf.info(f"Directory {path} moved to {tmp_path}")
            else:
                cf.info(f"{path} does not exist")

    @staticmethod
    def entrypoint():
        SafelyFileRemover().remove_file_or_dir(SafelyFileRemover().parse_args().paths)


def is_sudo_required():
    try:
        result = subprocess.run(
            ["sudo", "-n", "true"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False


class AbstractInstaller(ABC):
    @abstractmethod
    def install(self):
        pass


class AppInstaller(AbstractInstaller):
    def __init__(self, apps: list):
        self.apps = apps

    def update(self):
        if is_sudo_required():
            cf.shell("sudo apt update -y", print_str=True)
        else:
            cf.shell("apt update -y", print_str=True)

    def install(self):
        self.update()
        for app in self.apps:
            cf.info(f"Installing {app}")
            if is_sudo_required():
                cf.shell(f"sudo apt install -y {app}", print_str=True)
            else:
                cf.shell(f"apt install -y {app}", print_str=True)


class PythonPackageInstaller(AbstractInstaller):
    def __init__(self, packages: list):
        self.packages = packages

    def is_break_system_package_manager(self):
        # Check if pip version is >= 23.3
        try:
            import pip
            version = pip.__version__.split('.')
            major = int(version[0])
            minor = int(version[1])
            return major >= 23 and minor >= 3
        except (ImportError, ValueError, IndexError):
            return False

    def install(self):
        for package in self.packages:
            if self.is_break_system_package_manager():
                cf.shell(
                    f"pip3 install {package} --break-system-packages", print_str=True)
            else:
                cf.shell(f"pip3 install {package}", print_str=True)


class DockerInstaller(AbstractInstaller):
    def install(self):
        commands = [
            'curl -fsSL https://get.docker.com -o /tmp/get-docker.sh',
            '{} bash /tmp/get-docker.sh'.format(is_sudo_required()
                                                and 'sudo' or '')
        ]
        for cmd in commands:
            cf.shell(cmd, print_str=True)


class SupervisorInstaller(AbstractInstaller):
    def __init__(self):
        self.config_dir = "/etc/supervisor"
        self.config_file = f"{self.config_dir}/supervisord.conf"

    def create_default_config(self):
        default_config = """[unix_http_server]
file=/tmp/supervisor.sock

[supervisord]
logfile=/tmp/supervisord.log
logfile_maxbytes=50MB
logfile_backups=10
loglevel=info
pidfile=/tmp/supervisord.pid
nodaemon=false
minfds=1024
minprocs=200

[rpcinterface:supervisor]
supervisor.rpcinterface_factory = supervisor.rpcinterface:make_main_rpcinterface

[supervisorctl]
serverurl=unix:///tmp/supervisor.sock

[include]
files = /etc/supervisor/conf.d/*.conf
"""
        sudo_prefix = "sudo" if is_sudo_required() else ""
        cf.shell(f"{sudo_prefix} mkdir -p {self.config_dir}/conf.d",
                 print_str=True)

        with open("/tmp/supervisord.conf", "w") as f:
            f.write(default_config)
        cf.shell(
            f"{sudo_prefix} mv /tmp/supervisord.conf {self.config_file}", print_str=True)

    def install(self):
        self.create_default_config()
        sudo_prefix = "sudo" if is_sudo_required() else ""
        cf.shell(f"{sudo_prefix} supervisord -c {self.config_file}",
                 print_str=True)


class TTYDConfigurator:
    def __init__(self):
        self.config_dir = "/etc/supervisor/conf.d"
        self.config_file = f"{self.config_dir}/ttyd.conf"

    def get_ttyd_path(self):
        possible_paths = [
            "/usr/local/bin/ttyd",
            "/usr/bin/ttyd"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        raise FileNotFoundError("ttyd executable not found")

    def configure(self):
        try:
            ttyd_path = self.get_ttyd_path()
            ttyd_config = f"""[program:ttyd]
command={ttyd_path} -c tom:passport123 -t fontFamily='Courier New' -t fontSize=18 -W -p 7059 bash
autostart=true
autorestart=true
stderr_logfile=/var/log/ttyd.err.log
stdout_logfile=/var/log/ttyd.out.log
"""
            sudo_prefix = "sudo" if is_sudo_required() else ""

            # Create config file
            with open("/tmp/ttyd.conf", "w") as f:
                f.write(ttyd_config)

            # Move to final location
            cf.shell(
                f"{sudo_prefix} mv /tmp/ttyd.conf {self.config_file}",
                print_str=True
            )
            cf.info("TTYD configuration created successfully")

            # Reload supervisor
            cf.shell(
                f"{sudo_prefix} supervisorctl reload",
                print_str=True
            )
        except FileNotFoundError as e:
            cf.info(f"Error: {str(e)}")
            return False
        except Exception as e:
            cf.info(f"Error configuring TTYD: {str(e)}")
            return False
        return True


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

    # If no arguments provided, print help and exit
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # Install everything if -all is specified
    install_all = args.all

    if install_all or args.app:
        app_installer = AppInstaller([
            "vim", "neofetch", "curl", "emacs", "fish", "docker.io", "docker-compose",
            "net-tools", "vnstat", "tree", "htop", "ttyd", "sysstat" 
        ])
        app_installer.install()

    if install_all or args.python:
        python_installer = PythonPackageInstaller([
            "httpie", "supervisor", "uvicorn", "fastapi", "pydantic", "httpx"
        ])
        python_installer.install()

    if install_all or args.supervisor:
        supervisor_installer = SupervisorInstaller()
        supervisor_installer.install()

    if install_all or args.ttyd:
        ttyd_configurator = TTYDConfigurator()
        ttyd_configurator.configure()
