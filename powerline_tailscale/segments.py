import json
from subprocess import PIPE, Popen
from typing import Union

from powerline.segments import Segment, with_docstring
from powerline.theme import requires_segment_info

SEGMENT_PREFIX = "(ts)"


@requires_segment_info
class TailscaleSegment(Segment):
    def __init__(self):
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
            self.exit_node_ips = self._get_exit_node_ips()

        return self.build_segments(show_profile_name, show_exit_node_status, show_exit_node)

    def build_segments(self, show_profile_name: bool, show_exit_node_status: bool, show_exit_node: bool):
        segments = []

        if show_profile_name:
            base = self.get_base_command()
            profile = self.execute(base + ["http://local-tailscaled.sock/localapi/v0/prefs"])
            d = json.loads(profile)
            profile_name = d.get("ProfileName", None)
            config = d.get("Config", None)

            if profile_name is None and config is not None:
                contents = "default"
            elif profile_name is None and config is None:
                contents = "logged out"
            else:
                contents = profile_name

            segments.append(
                {
                    "contents": f"{SEGMENT_PREFIX} {contents}",
                    "highlight_groups": ["tailscale"],
                    "divider_highlight_group": "tailscale:divider",
                }
            )

        if show_exit_node_status:
            highlight_groups = ["tailscale_exitnode"]
            contents = "exit node (n)"

            if self.exit_node_ips is not None:
                contents = "exit node (y)"

            if not show_profile_name and show_exit_node_status:
                contents = f"{SEGMENT_PREFIX} {contents}"
                highlight_groups = ["tailscale"]

            segments.append(
                {
                    "contents": contents,
                    "highlight_groups": highlight_groups,
                    "divider_highlight_group": "tailscale:divider",
                }
            )

        # Exit node's value can only be shown if 'show_exit_node_status' is False
        if show_exit_node and not show_exit_node_status:
            highlight_groups = ["tailscale_exitnode"]
            contents = "exit node (n)"

            if self.exit_node_ips is not None:
                # If both an IPv4 and IPv6 address exist, it should get the first
                # which is usually IPv4
                contents = self.exit_node_ips[0]

            if not show_profile_name and show_exit_node:
                contents = f"{SEGMENT_PREFIX} {contents}"
                highlight_groups = ["tailscale"]

            segments.append(
                {
                    "contents": contents,
                    "highlight_groups": highlight_groups,
                    "divider_highlight_group": "tailscale:divider",
                }
            )

        return segments

    def execute(self, command):
        proc = Popen(command, stdout=PIPE, stderr=PIPE)
        out, _ = proc.communicate()
        return out.decode("utf-8")

    def get_base_command(self):
        return ["curl", "--unix-socket", "/var/run/tailscale/tailscaled.sock"]

    # TODO: This might not need to be an instance method, but rather just a function
    # that reads a dictionary '{"ExitNodeStatus": {"TailscaleIPs": ["abc", "xyz"]}}'
    def _get_exit_node_ips(self) -> Union[list[str], None]:
        base = self.get_base_command()
        status = self.execute(base + ["http://local-tailscaled.sock/localapi/v0/status"])
        d = json.loads(status)
        exit_node_status = d.get("ExitNodeStatus", None)
        if exit_node_status is None:
            return None

        exit_node_ips = exit_node_status.get("TailscaleIPs", None)
        if exit_node_ips is None:
            return None

        return exit_node_ips


tailscale = with_docstring(TailscaleSegment(), """Return the status of Tailscale.""")
