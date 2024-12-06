from .types import AbstractConfiger
import codefast as cf
import os


class TTYDConfigurator(AbstractConfiger):
    def __init__(self):
        self.config_dir = "/etc/supervisor/conf.d"
        self.config_file = f"{self.config_dir}/ttyd.conf"

    def snap_install(self):
        cf.shell("snap install ttyd", print_str=True)

    def get_ttyd_path(self):
        possible_paths = [
            "/usr/local/bin/ttyd",
            "/usr/bin/ttyd",
            "/snap/bin/ttyd",
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        raise FileNotFoundError("ttyd executable not found")

    def config(self):
        try:
            self.snap_install()
            ttyd_path = self.get_ttyd_path()
            ttyd_config = f"""[program:ttyd]
command={ttyd_path} -c tom:passport123 -t fontFamily='Courier New' -t fontSize=18 -W -p 7059 bash
autostart=true
autorestart=true
stderr_logfile=/var/log/ttyd.err.log
stdout_logfile=/var/log/ttyd.out.log
"""
            with open(self.config_file, "w") as f:
                f.write(ttyd_config)
            cf.info("TTYD configuration created successfully")
            cf.shell(f"supervisorctl reload", print_str=True)
        except FileNotFoundError as e:
            cf.info(f"Error: {str(e)}")
            return False
        except Exception as e:
            cf.info(f"Error configuring TTYD: {str(e)}")
            return False
        return True

def ttyd_config():
    TTYDConfigurator().config()
