
import codefast as cf


def trojan_config(domain: str, password: str):
    cmd = f'curl -L ttoo.lol/trojan.sh | bash -s -- -domain {domain} -password {password}'
    cf.shell(cmd, print_str=True)
