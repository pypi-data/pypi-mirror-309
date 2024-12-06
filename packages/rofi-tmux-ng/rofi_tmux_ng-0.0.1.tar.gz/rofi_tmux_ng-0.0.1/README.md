[![Documentation Status](https://readthedocs.org/projects/rofi-tmux/badge/?version=latest)](http://rofi-tmux.readthedocs.io/en/latest/?badge=latest) [![PyPI](https://img.shields.io/pypi/v/rofi-tmux-ng.svg)](https://pypi.python.org/pypi/rofi-tmux-ng)

## rft (rofi-tmux-ng)

![rft](docs/images/rft.png)

Quickly switch tmux sessions & windows via rofi. Integrates with [i3wm](https://i3wm.org/)
for a smoother switching workflow, if you have multiple workspaces.

Note this is a fork of [viniarck/rofi-tmux](https://github.com/viniarck/rofi-tmux/).
Upstream is still active and maintained, but the project you're currently
viewing has somewhat diverged in its architecture -- mainly stopped using
`libtmux` library and instead started employing client-server paradigm to
keep tmux state updated in memory via control client process.

### Features

- Switch or kill any tmux session
- Switch or kill any tmux window, either globally or within the current session
- ~~Switch to any tmuxinator project.~~ not implemented; see upstream if needed
- Cache last tmux session and window for fast switching back and forth,
decreases the number of required keystrokes
- Integration with i3wm for switching to the right workspace seamlessly
- Extensible for other window managers

### Installation

```sh
pipx install rofi-tmux-ng
```

### Screencast

[![rft-demo](https://img.youtube.com/vi/o6tBNFJW28c/0.jpg)](https://www.youtube.com/watch?v=o6tBNFJW28c)

### Usage

TODO: needs work. Following link leads to upstream docs that are not 100%
applicable to this fork.

Check [ReadTheDocs](http://rofi-tmux.readthedocs.io/) for detailed information,
usage and suggested key bindings.

### Contributing

Contributions are more than welcome. Let me know if you want to add other features
or integrations, or if you are having trouble to use rft, open an issue.
Join the [chat on gitter.im/rofi-tmux/community](https://gitter.im/rofi-tmux/community)
if you want to discuss ideas.

### License

MIT
