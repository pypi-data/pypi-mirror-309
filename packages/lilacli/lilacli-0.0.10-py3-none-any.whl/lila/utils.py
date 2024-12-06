import os
import re

from typing import Dict, Set


def get_vars(content: str) -> Set[str]:
    # Searches for all ${VAR_NAME} and returns them as a set
    regex = re.compile(r"\${(.*?)}")
    return set(regex.findall(content))


def get_vars_from_env(content: str) -> Dict[str, str]:
    vars_ = get_vars(content)
    for var in vars_:
        if var not in os.environ:
            raise RuntimeError(f"Environment variable {var} not set and used in the test.")

    ret = {var: os.environ[var] for var in vars_}
    return ret
