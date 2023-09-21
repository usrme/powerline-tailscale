# Powerline Tailscale

A Powerline segment for showing the status of Tailscale.

## Requirements

## Installation

Using Pip:

```bash
pip install powerline-tailscale
```

## Configuration

Only three highlight groups are necessary to be defined in order for `powerline-tailscale` to work. These can be set up in `~/.config/powerline/colorschemes/default.json`:

```json
{
  "name": "Default",
    "groups": {
      "tailscale":                 { "fg": "white", "bg": "gray2","attrs": [] },
      "tailscale_exitnode":        { "fg": "white", "bg": "steelblue","attrs": [] },
      "tailscale:divider":         { "fg": "white", "bg": "steelblue", "attrs": [] }
    }
}
```

After that, enable the segment by modifying the relevant Powerline theme. If you are using the default, then in `~/.config/powerline/themes/shell/default.json`:

```json
{
  "function": "powerline_tailscale.tailscale",
    "args": {
      "show_profile_name": true,
      "show_exit_node_status": true,
      "show_exit_node": true
  }
}
```
