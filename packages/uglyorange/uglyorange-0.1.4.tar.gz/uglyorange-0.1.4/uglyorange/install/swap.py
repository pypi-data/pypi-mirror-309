from .types import AbstractConfiger
import codefast as cf
import os


class SwapConfigurator(AbstractConfiger):
    def __init__(self, size: int):
        # size in GB
        self.size = size
        assert self.size > 0, "Swap size must be greater than 0"
        assert self.size <= 10, "Swap size must be less than 10 GB"

    def config(self):
        '''
        1. create swap file
        2. enable swap
        3. add swap to fstab
        '''
        cf.shell(
            f"dd if=/dev/zero of=/swapfile bs=100M count={self.size * 10} status=progress",
            print_str=True
        )
        cf.shell("mkswap /swapfile", print_str=True)
        cf.shell("chmod 600 /swapfile", print_str=True)
        cf.shell("swapon /swapfile", print_str=True)
        cf.shell("echo '/swapfile none swap sw 0 0' >> /etc/fstab", print_str=True)


def swap_config(size: int):
    SwapConfigurator(size).config()
