import pytest
import json
import os

from pkg_resources import resource_filename
current_path = resource_filename('JsonOperate', 'tests')


@pytest.fixture
def simple_json_data():
    json_path = os.path.join(current_path, 'HipTD_thor_valid_srs_tdd_bwv_CB008322_G_frCfg1208_td_jumping_trigger_snapshot.json')
    with open(json_path, 'r') as f:
        data = json.load(f)
        return data

@pytest.fixture
def complex_json_data():
    json_path = os.path.join(current_path, 'HipTD_THOR_56_CAP6_FDD_32x4RX_10MHz_COMP.json')
    with open(json_path, 'r') as f:
        data = json.load(f)
        return data