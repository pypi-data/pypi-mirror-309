#!/usr/bin/env python3
import codefast as cf
from .types import AbstractInstaller


class PythonPackageInstaller(AbstractInstaller):
    def __init__(self, packages: list):
        self.packages = packages

    def install(self):
        for package in self.packages:
            cf.shell(
                f"pip3 install {package} --break-system-packages",
                print_str=True
            )


def python_install():
    libs = [
        "httpie", "supervisor", "uvicorn", "fastapi", "pydantic", "httpx"
    ]
    PythonPackageInstaller(libs).install()
