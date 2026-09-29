from pathlib import Path

import pytest
from nornir import InitNornir
from nornir.core import Nornir
from nornir.core.state import GlobalState

global_data = GlobalState(dry_run=True)


@pytest.fixture(scope="session", autouse=True)
def nr() -> Nornir:
    """Initializes nornir"""
    dir_path = Path(__file__).resolve().parent

    nornir = InitNornir(
        inventory={
            "plugin": "SimpleInventory",
            "options": {
                "host_file": f"{dir_path}/inventory_data/hosts.yaml",
                "group_file": f"{dir_path}/inventory_data/groups.yaml",
                "defaults_file": f"{dir_path}/inventory_data/defaults.yaml",
            },
        },
        dry_run=True,
    )
    nornir.data = global_data
    return nornir


@pytest.fixture(autouse=True)
def reset_data() -> None:
    global_data.dry_run = True
    global_data.reset_failed_hosts()
