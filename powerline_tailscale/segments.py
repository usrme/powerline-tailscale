import json
from subprocess import PIPE, Popen

from powerline.segments import Segment, with_docstring
from powerline.theme import requires_segment_info


@requires_segment_info
class TailscaleSegment(Segment):
    def __call__(self, pl, segment_info, show_exit_node: bool = True, **kwargs):
        try:
            if segment_info["environ"].get("POWERLINE_TAILSCALE") == "0":
                return
        except TypeError:
            return

        return self.build_segments(show_exit_node)

    def build_segments(self, show_exit_node: bool):
        segments = []

        base = self.get_base_command()
        profile = self.execute(base + ["http://local-tailscaled.sock/localapi/v0/prefs"])
        d = json.loads(profile)
        profile_name = d.get("ProfileName", None)
        config = d.get("Config", None)

        if profile_name is None and config is not None:
            contents = "(ts) default"
        elif profile_name is None and config is None:
            contents = "(ts) logged out"
        else:
            contents = f"(ts) {profile_name}"

        segments.append(
            {
                "contents": contents,
                "highlight_groups": ["tailscale"],
                "divider_highlight_group": "tailscale:divider",
            }
        )

        if show_exit_node:
            contents = "no exit node"
            exit_node_ips = None

            status = self.execute(base + ["http://local-tailscaled.sock/localapi/v0/status"])
            d = json.loads(status)
            exit_node = d.get("ExitNodeStatus", None)

            if exit_node is not None:
                exit_node_ips = exit_node.get("TailscaleIPs", None)
            if exit_node_ips is not None:
                contents = exit_node_ips[0]

            segments.append(
                {
                    "contents": contents,
                    "highlight_groups": ["tailscale_exitnode"],
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


tailscale = with_docstring(TailscaleSegment(), """Return the status of Tailscale.""")
