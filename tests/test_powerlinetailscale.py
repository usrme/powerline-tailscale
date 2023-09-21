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


@pytest.fixture
def segment_info():
    return {"environ": {}}


def test_logged_out(monkeypatch, segment_info):
    monkeypatch.setattr(powerline_tailscale.segments, "_fetch", lambda *args: "{}")
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True, show_exit_node_status=True)
    assert output == [EXPECTED_LOGGED_OUT]


def test_default_profile(monkeypatch, segment_info):
    monkeypatch.setattr(powerline_tailscale.segments, "_fetch", lambda *args: '{"Config": {}}')
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True, show_exit_node_status=False)
    assert output == [EXPECTED_DEFAULT_PROFILE]


def test_profile_name(monkeypatch, segment_info):
    monkeypatch.setattr(powerline_tailscale.segments, "_fetch", lambda *args: '{"ProfileName": "home", "Config": {}}')
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True, show_exit_node_status=False)
    assert output == [EXPECTED_HOME_PROFILE]


def test_default_profile_no_exit_node(monkeypatch, segment_info):
    monkeypatch.setattr(powerline_tailscale.segments, "_fetch", lambda *args: '{"Config": {}}')
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True, show_exit_node_status=True)
    assert output == [EXPECTED_DEFAULT_PROFILE, EXPECTED_NO_EXIT_NODE]


def test_default_profile_exit_node(monkeypatch, segment_info):
    monkeypatch.setattr(
        powerline_tailscale.segments,
        "_fetch",
        lambda *args: '{"Config": {}, "ExitNodeStatus": {"TailscaleIPs": ["127.0.0.1/32", "::1"]}}',
    )
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True, show_exit_node_status=True)
    assert output == [EXPECTED_DEFAULT_PROFILE, EXPECTED_EXIT_NODE]


def test_profile_name_no_exit_node(monkeypatch, segment_info):
    monkeypatch.setattr(powerline_tailscale.segments, "_fetch", lambda *args: '{"ProfileName": "home", "Config": {}}')
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True, show_exit_node_status=True)
    assert output == [EXPECTED_HOME_PROFILE, EXPECTED_NO_EXIT_NODE]


def test_profile_name_exit_node(monkeypatch, segment_info):
    monkeypatch.setattr(
        powerline_tailscale.segments,
        "_fetch",
        lambda *args: '{"ProfileName": "home", "Config": {}, "ExitNodeStatus": {"TailscaleIPs": ["127.0.0.1/32", "::1"]}}',  # noqa: E501
    )
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True, show_exit_node_status=True)
    assert output == [EXPECTED_HOME_PROFILE, EXPECTED_EXIT_NODE]


def test_default_profile_no_exit_node_ip(monkeypatch, segment_info):
    monkeypatch.setattr(powerline_tailscale.segments, "_fetch", lambda *args: '{"Config": {}}')
    output = powerline_tailscale.tailscale(
        segment_info, show_profile_name=True, show_exit_node_status=False, show_exit_node=True
    )
    assert output == [EXPECTED_DEFAULT_PROFILE, EXPECTED_NO_EXIT_NODE]


def test_default_profile_exit_node_ip(monkeypatch, segment_info):
    monkeypatch.setitem(EXPECTED_EXIT_NODE, "contents", "127.0.0.1/32")
    monkeypatch.setattr(
        powerline_tailscale.segments,
        "_fetch",
        lambda *args: '{"Config": {}, "ExitNodeStatus": {"TailscaleIPs": ["127.0.0.1/32", "::1"]}}',
    )
    output = powerline_tailscale.tailscale(
        segment_info, show_profile_name=True, show_exit_node_status=False, show_exit_node=True
    )
    assert output == [EXPECTED_DEFAULT_PROFILE, EXPECTED_EXIT_NODE]


def test_profile_name_no_exit_node_ip(monkeypatch, segment_info):
    monkeypatch.setattr(powerline_tailscale.segments, "_fetch", lambda *args: '{"ProfileName": "home", "Config": {}}')
    output = powerline_tailscale.tailscale(
        segment_info, show_profile_name=True, show_exit_node_status=False, show_exit_node=True
    )
    assert output == [EXPECTED_HOME_PROFILE, EXPECTED_NO_EXIT_NODE]


def test_profile_name_exit_node_ip(monkeypatch, segment_info):
    monkeypatch.setitem(EXPECTED_EXIT_NODE, "contents", "127.0.0.1/32")
    monkeypatch.setattr(
        powerline_tailscale.segments,
        "_fetch",
        lambda *args: '{"ProfileName": "home", "Config": {}, "ExitNodeStatus": {"TailscaleIPs": ["127.0.0.1/32", "::1"]}}',  # noqa: E501
    )
    output = powerline_tailscale.tailscale(
        segment_info, show_profile_name=True, show_exit_node_status=False, show_exit_node=True
    )
    assert output == [EXPECTED_HOME_PROFILE, EXPECTED_EXIT_NODE]


def test_show_no_profile_no_exit_node(monkeypatch, segment_info):
    monkeypatch.setitem(EXPECTED_NO_EXIT_NODE, "contents", "(ts) exit node (n)")
    monkeypatch.setitem(EXPECTED_NO_EXIT_NODE, "highlight_groups", ["tailscale"])
    monkeypatch.setattr(powerline_tailscale.segments, "_fetch", lambda *args: "{}")
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=False, show_exit_node_status=True)
    assert output == [EXPECTED_NO_EXIT_NODE]


def test_show_no_profile_exit_node(monkeypatch, segment_info):
    monkeypatch.setitem(EXPECTED_NO_EXIT_NODE, "contents", "(ts) exit node (y)")
    monkeypatch.setitem(EXPECTED_NO_EXIT_NODE, "highlight_groups", ["tailscale"])
    monkeypatch.setattr(
        powerline_tailscale.segments,
        "_fetch",
        lambda *args: '{"ExitNodeStatus": {"TailscaleIPs": ["127.0.0.1/32", "::1"]}}',
    )
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=False, show_exit_node_status=True)
    assert output == [EXPECTED_NO_EXIT_NODE]


def test_show_no_profile_no_exit_node_ip(monkeypatch, segment_info):
    monkeypatch.setitem(EXPECTED_NO_EXIT_NODE, "contents", "(ts) exit node (n)")
    monkeypatch.setitem(EXPECTED_NO_EXIT_NODE, "highlight_groups", ["tailscale"])
    monkeypatch.setattr(powerline_tailscale.segments, "_fetch", lambda *args: "{}")
    output = powerline_tailscale.tailscale(
        segment_info, show_profile_name=False, show_exit_node_status=False, show_exit_node=True
    )
    assert output == [EXPECTED_NO_EXIT_NODE]


def test_show_no_profile_exit_node_ip(monkeypatch, segment_info):
    monkeypatch.setitem(EXPECTED_EXIT_NODE, "contents", "(ts) 127.0.0.1/32")
    monkeypatch.setitem(EXPECTED_EXIT_NODE, "highlight_groups", ["tailscale"])
    monkeypatch.setattr(
        powerline_tailscale.segments,
        "_fetch",
        lambda *args: '{"ExitNodeStatus": {"TailscaleIPs": ["127.0.0.1/32", "::1"]}}',
    )
    output = powerline_tailscale.tailscale(
        segment_info, show_profile_name=False, show_exit_node_status=False, show_exit_node=True
    )
    assert output == [EXPECTED_EXIT_NODE]


def test_envvar_notzero_logged_out(monkeypatch):
    segment_info = {"environ": {"POWERLINE_TAILSCALE": "1"}}
    monkeypatch.setattr(powerline_tailscale.segments, "_fetch", lambda *args: "{}")
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True)
    assert output == [EXPECTED_LOGGED_OUT]


def test_envvar_zero_logged_out(monkeypatch):
    segment_info = {"environ": {"POWERLINE_TAILSCALE": "0"}}
    monkeypatch.setattr(powerline_tailscale.segments, "_fetch", lambda *args: "{}")
    output = powerline_tailscale.tailscale(segment_info, show_profile_name=True)
    assert output is None
