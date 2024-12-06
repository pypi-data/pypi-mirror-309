#!/usr/bin/env python3
from abc import ABC, abstractmethod
import argparse
import os
import shutil
import codefast as cf
import subprocess


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


def vpsinit():
    """
    1. Install apps, including [vim, neofetch, curl, emacs, tree, htop. etc]
    2. Install python packages, including [supervisor, uvicorn, fastapi, pydantic, httpx]
    """
    app_installer = AppInstaller(
        ["vim", "neofetch", "curl", "emacs", "tree", "htop", "ttyd"])
    app_installer.install()

    python_installer = PythonPackageInstaller(
        ["supervisor", "uvicorn", "fastapi", "pydantic", "httpx"])
    python_installer.install()

    docker_installer = DockerInstaller()
    docker_installer.install()
