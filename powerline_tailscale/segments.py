import json
from subprocess import PIPE, Popen

from powerline.segments import Segment, with_docstring
from powerline.theme import requires_segment_info


@requires_segment_info
class TailscaleSegment(Segment):
    def __call__(self, pl, segment_info, show_account: bool = True, **kwargs):
        try:
            if segment_info["environ"].get("POWERLINE_TAILSCALE") == "0":
                return
        except TypeError:
            return

        return self.build_segments(show_account)

    def build_segments(self, show_account: bool = True):
        segments = []

        if show_account:
            base = self.get_base_command()
            profile = self.execute(base + ["http://local-tailscaled.sock/localapi/v0/prefs"])
            d = json.loads(profile)
            segments.append(
                {
                    "contents": f"(ts) {d['ProfileName']}",
                    "highlight_groups": ["tailscale"],
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
