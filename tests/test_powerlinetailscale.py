import pytest

import powerline_tailscale

EXPECTED_LOGGED_OUT = {
    "contents": "(ts) logged out",
    "highlight_groups": ["tailscale"],
    "divider_highlight_group": "tailscale:divider",
}

EXPECTED_DEFAULT_PROFILE = {
    "contents": "(ts) default",
    "highlight_groups": ["tailscale"],
    "divider_highlight_group": "tailscale:divider",
}

EXPECTED_HOME_PROFILE = {
    "contents": "(ts) home",
    "highlight_groups": ["tailscale"],
    "divider_highlight_group": "tailscale:divider",
}

EXPECTED_NO_EXIT_NODE = {
    "contents": "exit node (n)",
    "highlight_groups": ["tailscale_exitnode"],
    "divider_highlight_group": "tailscale:divider",
}

EXPECTED_EXIT_NODE = {
    "contents": "exit node (y)",
    "highlight_groups": ["tailscale_exitnode"],
    "divider_highlight_group": "tailscale:divider",
}

EMPTY_CONFIG = '{"Config": {}}'
EMPTY_PROFILE = '{"ProfileName": "home", "Config": {}}'
DEFAULT_EXIT_NODE = '{"Config": {}, "ExitNodeStatus": {"TailscaleIPs": ["127.0.0.1/32", "::1"]}}'
PROFILE_EXIT_NODE = '{"ProfileName": "home", "Config": {}, "ExitNodeStatus": {"TailscaleIPs": ["127.0.0.1/32", "::1"]}}'
NO_PROFILE_EXIT_NODE = '{"ExitNodeStatus": {"TailscaleIPs": ["127.0.0.1/32", "::1"]}}'


@pytest.fixture
def segment_info():
    return {"environ": {}}


@pytest.fixture
def patch_fetch_value(monkeypatch):
    def _patch_fetch_value(value: str = ""):
        if not value:
            value = "{}"
        monkeypatch.setattr(powerline_tailscale.segments, "_fetch", lambda *args: value)

    return _patch_fetch_value


def test_logged_out(patch_fetch_value, segment_info):
    patch_fetch_value()
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True, show_exit_node_status=True)
    assert output == [EXPECTED_LOGGED_OUT]


def test_default_profile(patch_fetch_value, segment_info):
    patch_fetch_value(EMPTY_CONFIG)
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True, show_exit_node_status=False)
    assert output == [EXPECTED_DEFAULT_PROFILE]


def test_profile_name(patch_fetch_value, segment_info):
    patch_fetch_value(EMPTY_PROFILE)
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True, show_exit_node_status=False)
    assert output == [EXPECTED_HOME_PROFILE]


def test_default_profile_no_exit_node(patch_fetch_value, segment_info):
    patch_fetch_value(EMPTY_CONFIG)
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True, show_exit_node_status=True)
    assert output == [EXPECTED_DEFAULT_PROFILE, EXPECTED_NO_EXIT_NODE]


def test_default_profile_exit_node(patch_fetch_value, segment_info):
    patch_fetch_value(DEFAULT_EXIT_NODE)
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True, show_exit_node_status=True)
    assert output == [EXPECTED_DEFAULT_PROFILE, EXPECTED_EXIT_NODE]


def test_profile_name_no_exit_node(patch_fetch_value, segment_info):
    patch_fetch_value(EMPTY_PROFILE)
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True, show_exit_node_status=True)
    assert output == [EXPECTED_HOME_PROFILE, EXPECTED_NO_EXIT_NODE]


def test_profile_name_exit_node(patch_fetch_value, segment_info):
    patch_fetch_value(PROFILE_EXIT_NODE)
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True, show_exit_node_status=True)
    assert output == [EXPECTED_HOME_PROFILE, EXPECTED_EXIT_NODE]


def test_default_profile_no_exit_node_ip(patch_fetch_value, segment_info):
    patch_fetch_value(EMPTY_CONFIG)
    output = powerline_tailscale.tailscale(
        segment_info, show_profile_name=True, show_exit_node_status=False, show_exit_node=True
    )
    assert output == [EXPECTED_DEFAULT_PROFILE, EXPECTED_NO_EXIT_NODE]


def test_default_profile_exit_node_ip(monkeypatch, patch_fetch_value, segment_info):
    monkeypatch.setitem(EXPECTED_EXIT_NODE, "contents", "127.0.0.1/32")
    patch_fetch_value(DEFAULT_EXIT_NODE)
    output = powerline_tailscale.tailscale(
        segment_info, show_profile_name=True, show_exit_node_status=False, show_exit_node=True
    )
    assert output == [EXPECTED_DEFAULT_PROFILE, EXPECTED_EXIT_NODE]


def test_profile_name_no_exit_node_ip(patch_fetch_value, segment_info):
    patch_fetch_value(EMPTY_PROFILE)
    output = powerline_tailscale.tailscale(
        segment_info, show_profile_name=True, show_exit_node_status=False, show_exit_node=True
    )
    assert output == [EXPECTED_HOME_PROFILE, EXPECTED_NO_EXIT_NODE]


def test_profile_name_exit_node_ip(monkeypatch, patch_fetch_value, segment_info):
    monkeypatch.setitem(EXPECTED_EXIT_NODE, "contents", "127.0.0.1/32")
    patch_fetch_value(PROFILE_EXIT_NODE)
    output = powerline_tailscale.tailscale(
        segment_info, show_profile_name=True, show_exit_node_status=False, show_exit_node=True
    )
    assert output == [EXPECTED_HOME_PROFILE, EXPECTED_EXIT_NODE]


def test_show_no_profile_no_exit_node(monkeypatch, patch_fetch_value, segment_info):
    monkeypatch.setitem(EXPECTED_NO_EXIT_NODE, "contents", "(ts) exit node (n)")
    monkeypatch.setitem(EXPECTED_NO_EXIT_NODE, "highlight_groups", ["tailscale"])
    patch_fetch_value()
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=False, show_exit_node_status=True)
    assert output == [EXPECTED_NO_EXIT_NODE]


def test_show_no_profile_exit_node(monkeypatch, patch_fetch_value, segment_info):
    monkeypatch.setitem(EXPECTED_NO_EXIT_NODE, "contents", "(ts) exit node (y)")
    monkeypatch.setitem(EXPECTED_NO_EXIT_NODE, "highlight_groups", ["tailscale"])
    patch_fetch_value(NO_PROFILE_EXIT_NODE)
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=False, show_exit_node_status=True)
    assert output == [EXPECTED_NO_EXIT_NODE]


def test_show_no_profile_no_exit_node_ip(monkeypatch, patch_fetch_value, segment_info):
    monkeypatch.setitem(EXPECTED_NO_EXIT_NODE, "contents", "(ts) exit node (n)")
    monkeypatch.setitem(EXPECTED_NO_EXIT_NODE, "highlight_groups", ["tailscale"])
    patch_fetch_value()
    output = powerline_tailscale.tailscale(
        segment_info, show_profile_name=False, show_exit_node_status=False, show_exit_node=True
    )
    assert output == [EXPECTED_NO_EXIT_NODE]


def test_show_no_profile_exit_node_ip(monkeypatch, patch_fetch_value, segment_info):
    monkeypatch.setitem(EXPECTED_EXIT_NODE, "contents", "(ts) 127.0.0.1/32")
    monkeypatch.setitem(EXPECTED_EXIT_NODE, "highlight_groups", ["tailscale"])
    patch_fetch_value(NO_PROFILE_EXIT_NODE)
    output = powerline_tailscale.tailscale(
        segment_info, show_profile_name=False, show_exit_node_status=False, show_exit_node=True
    )
    assert output == [EXPECTED_EXIT_NODE]


def test_envvar_notzero_logged_out(patch_fetch_value):
    patch_fetch_value()
    segment_info = {"environ": {"POWERLINE_TAILSCALE": "1"}}
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True)
    assert output == [EXPECTED_LOGGED_OUT]


def test_envvar_zero_logged_out(patch_fetch_value):
    patch_fetch_value()
    segment_info = {"environ": {"POWERLINE_TAILSCALE": "0"}}
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True)
    assert output is None
