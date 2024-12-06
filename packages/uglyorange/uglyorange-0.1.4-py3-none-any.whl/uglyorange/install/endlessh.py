import codefast as cf


def endlessh_config():
    # docker run -d --name endlessh -p 22:22 signalout/endlessh
    cf.shell(
        "docker run -d --name endlessh -p 22:22 signalout/endlessh", print_str=True)
