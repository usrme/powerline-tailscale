import json
from subprocess import PIPE, Popen
from typing import Union

from powerline.segments import Segment, with_docstring
from powerline.theme import requires_segment_info

SOCKET_PATH = "/var/run/tailscale/tailscaled.sock"
BASE_LOCAL_API_ENDPOINT = "http://local-tailscaled.sock/localapi/v0"
CURL_COMMAND = ["curl", "--unix-socket", SOCKET_PATH]


@requires_segment_info
class TailscaleSegment(Segment):
    def __init__(self):
        self.segment_prefix = "(ts)"
        self.primary_highlight_groups: list[str] = ["tailscale"]
        self.secondary_highlight_groups: list[str] = ["tailscale_exitnode"]
        self.exit_node_ips: Union[list[str], None] = None

    def __call__(
        self,
        segment_info,
        show_profile_name: bool = True,
        show_exit_node_status: bool = True,
        show_exit_node: bool = False,
        **kwargs,
    ):
        try:
            if segment_info["environ"].get("POWERLINE_TAILSCALE") == "0":
                return
        except TypeError:
            return

        if show_exit_node_status or show_exit_node:
            ts_status = json.loads(query_api("status"))
            self.exit_node_ips = get_exit_node_ips(ts_status)

        return self.build_segments(show_profile_name, show_exit_node_status, show_exit_node)

    def build_segments(self, show_profile_name: bool, show_exit_node_status: bool, show_exit_node: bool):
        segments = []

        if show_profile_name:
            ts_prefs = json.loads(query_api("prefs"))
            contents = get_profile_name(ts_prefs)
            contents, highlight_groups = self.set_segment_styling(contents, show_profile_name)
            segments.append(
                {
                    "contents": contents,
                    "highlight_groups": highlight_groups,
                    "divider_highlight_group": "tailscale:divider",
                }
            )
            if "logged out" in contents:
                return segments

        if show_exit_node_status:
            contents = "exit node (n)"
            if self.exit_node_ips:
                contents = "exit node (y)"
            contents, highlight_groups = self.set_segment_styling(contents, show_profile_name, show_exit_node_status)
            segments.append(
                {
                    "contents": contents,
                    "highlight_groups": highlight_groups,
                    "divider_highlight_group": "tailscale:divider",
                }
            )

        # Exit node's value can only be shown if 'show_exit_node_status' is False
        if show_exit_node and not show_exit_node_status:
            contents = "exit node (n)"
            if self.exit_node_ips:
                # If both an IPv4 and IPv6 address exist, it
                # should get the first which is usually IPv4
                contents = self.exit_node_ips[0]
            contents, highlight_groups = self.set_segment_styling(contents, show_profile_name, show_exit_node)
            segments.append(
                {
                    "contents": contents,
                    "highlight_groups": highlight_groups,
                    "divider_highlight_group": "tailscale:divider",
                }
            )

        return segments

    def set_segment_styling(
        self, contents: str, has_first_segment: bool, has_other_segments: bool = False
    ) -> tuple[str, list[str]]:
        highlight_groups = self.secondary_highlight_groups
        if (has_first_segment and not has_other_segments) or (not has_first_segment and has_other_segments):
            contents = f"{self.segment_prefix} {contents}"
            highlight_groups = self.primary_highlight_groups
        return contents, highlight_groups


def query_api(endpoint: str) -> str:
    endpoint = f"{BASE_LOCAL_API_ENDPOINT}/{endpoint}"
    cmd = CURL_COMMAND.copy()
    cmd.append(endpoint)
    return _fetch(cmd)


def _fetch(command: list[str]) -> str:
    proc = Popen(command, stdout=PIPE, stderr=PIPE)
    out, _ = proc.communicate()
    return out.decode("utf-8")


def get_profile_name(ts_prefs: dict) -> str:
    profile_name = ts_prefs.get("ProfileName", None)
    config = ts_prefs.get("Config", None)
    if profile_name is None and config is not None:
        return "default"
    elif profile_name is None and config is None:
        return "logged out"
    return profile_name


def get_exit_node_ips(ts_status: dict) -> list[str]:
    exit_node_status = ts_status.get("ExitNodeStatus", None)
    if exit_node_status is None:
        return []
    exit_node_ips = exit_node_status.get("TailscaleIPs", None)
    if exit_node_ips is None:
        return []
    return exit_node_ips


tailscale = with_docstring(
    TailscaleSegment(),
    """Return the status of Tailscale.

:param bool show_profile_name:
    Show the name of the active profile. If no profile has been created, then show "default".
    If no configuration can be found for the user, then it is assumed that the user is logged
    out and "logged out" is shown.
    True by default.

:param bool show_exit_node_status:
    Show either "exit node (n)" or "exit node (y)" depending on whether connected to an exit
    node.
    True by default.

:param bool show_exit_node:
    Show either "exit node (n)" if not connected to an exit node or the IP address of the
    exit node if connected to one.
    False by default.

Divider highlight group used: ``tailscale:divider``.

Highlight groups used: ``tailscale`` and ``tailscale_exitnode``.
""",
)
