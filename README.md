# brightcontrol

> AI vibecoded!

A minimal, modern GTK4 popup for controlling screen brightness with [`brightnessctl`](https://github.com/Hummer12007/brightnessctl). Built for NixOS and the [oxwm](https://github.com/tonybanters/oxwm) status bar, but it works with any X11/Wayland setup.

## Features

- Two buttons: decrease and increase brightness (5% steps)
- Live percentage and progress bar
- Keyboard shortcuts: `+` / `-`, arrow keys, `Esc` to close
- Mouse wheel support
- Closes automatically when it loses focus
- Never sets brightness to 0%, so the screen can't go fully black

## Requirements

- Python 3 with PyGObject
- GTK 4
- `brightnessctl`

On NixOS, all of this is handled by the included `default.nix` and `shell.nix`.

## Try it

```bash
nix-shell
python brightcontrol.py
```

## Install on NixOS

Copy `brightcontrol.py` and `default.nix` into your system configuration, for example `/etc/nixos/brightcontrol/`. If you use flakes, run `git add` on the folder so the flake can see it.

Then add it to your `configuration.nix`:

```nix
environment.systemPackages = with pkgs; [
  brightnessctl
  (callPackage ./brightcontrol/default.nix { })
];
```

Rebuild your system and run `brightcontrol` from any terminal.

## oxwm integration

In `~/.config/oxwm/config.lua`, add `click` to your brightness block:

```lua
oxwm.bar.block.shell({
    format = "[{}]",
    command = "brightnessctl -m | cut -d, -f4",
    interval = 2,
    color = colors.mid,
    underline = false,
    click = "brightcontrol",
}),
```

To open the popup as a floating window, add a rule:

```lua
oxwm.rule.add({ title = "brightcontrol", floating = true })
```

Validate with `oxwm --validate` and reload with `Mod+Shift+R`.

## Customization

- **Step size:** change `STEP` at the top of `brightcontrol.py`
- **Colors:** edit the CSS block in the same file (accent color is `#e8c170`)

## Troubleshooting

- **Permission denied from brightnessctl:** make sure your user is in the `video` group.
- **Window is tiled instead of floating:** check the window class with `xprop WM_CLASS` and adjust the oxwm rule.

## License

MIT
