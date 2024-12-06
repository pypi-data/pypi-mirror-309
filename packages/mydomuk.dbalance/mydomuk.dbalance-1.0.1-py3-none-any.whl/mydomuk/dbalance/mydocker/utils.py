from docker import DockerClient
from ..logger import infolog, debuglog
from time import sleep
from ..logger import infolog

def connect(url, hostname: str = None, quiet: bool = False):
    if url:
        if ":" in url:
            addr = url
        else:
            addr = url + ":2375"
        if quiet is False:
            if hostname:
                debuglog(f"Connecting to Docker API for {hostname} using {addr}")
            else:
                debuglog(f"Connecting to Docker API using {addr}")
    else:
        if quiet is False:
            debuglog("Connecting to Docker API using Unix Socket")
        addr = "unix://var/run/docker.sock"

    return DockerClient(
        base_url=addr,
        user_agent="DBALANCE",
        timeout=1
    )


def filter_name(name, filters):
    last_match_type = "+"
    if filters is not None:
        if len(filters) == 0:
            return True
        for limit in filters:
            matched = False
            match_type = None
            special_char = True
            negate = False
            startswith = True
            includes = False
            equals = False
            while special_char:
                char1 = limit[0]
                if char1 in "^~=":
                    limit = limit[1:]
                    if char1 == "^":
                        negate = True
                else:
                    special_char = False

                if char1 == "^":
                    negate = True
                elif char1 == "~":
                    startswith = False
                    includes = True
                    equals = False
                elif char1 == "=":
                    equals = True
                    startswith = False
                    includes = False

            if negate:
                last_match_type = "-"
                if equals:
                    if name == limit:
                        matched = True
                        match_type= "-"
                elif startswith:
                    if name.startswith(limit):
                        matched = True
                        match_type = "-"
                elif includes:
                    if limit in name:
                        matched = True
                        match_type = "-"
            else:
                last_match_type = "+"
                if equals:
                    if name == limit:
                        matched = True
                        match_type = "+"
                elif startswith:
                    if name.startswith(limit):
                        matched = True
                        match_type = "+"
                elif includes:
                    if limit in name:
                        matched = True
                        match_type = "+"
            if matched:
                break
        if matched:
            if match_type == "-":
                return False
            else:
                return True
        else:
            if last_match_type == "+":
                return False
            else:
                return True
    return True


def exec_with_retry(cmd: callable, retry_count: int = 3, delay: int = 1, exceptions: list[Exception] = None) -> any:
    result = None
    while retry_count > 0:
        try:
            result = cmd()
            break
        except Exception as e:
            if exceptions is None or e in exceptions:
                retry_count -= 1
                infolog(f"Command Errored, retrying : {e}")
                sleep(delay)
            else:
                raise e
    return result
