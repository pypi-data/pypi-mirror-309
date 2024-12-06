import os
import json
from datetime import datetime

STATE_VER = 1  # bump this whenever persisted state data structure changes
TIME_DIFF_DELTA_THRESHOLD_S = 10


HOMEDIR = os.environ.get('HOME')
EMPTY_STATE = {
        'timestamp': 0,
        'ver': -1,
        'tmux': {}
        }

def load_config() -> dict:
    """Load json config file ~/.rft.

    Currently supported window managers: 'i3'

    """
    conf = {
            'wm': 'i3',
            'tmux_title_rgx': '{session}',
            'ignored_sessions': [],
            'sw_signals': ['SIGUSR1'],
            'ss_signals': ['SIGUSR2'],
            'socket_path': '/tmp/.rofi-tmux-ipc.sock',
            'state_f_path': '/tmp/.rofi-tmux.state',
            'state': None,  # will be read from state_f_path
            'tmux_cc_cmd': ["tmux", "-C", "attach", "-f",
                            "no-output,no-detach-on-destroy,ignore-size,active-pane"]  # note single -C flag as per https://github.com/tmux/tmux/issues/3085
    }
    conf.update(_read_dict_from_file(os.path.join(HOMEDIR, '.rft')))

    conf['state'] = _load_state(conf['state_f_path'])

    # self.logger.debug('effective config: {}'.format(conf))
    return conf


def _load_state(file_loc) -> dict:
    s = _read_dict_from_file(file_loc)

    t = s.get('timestamp', 0)
    v = s.get('ver', -1)
    if (_now() - t <= TIME_DIFF_DELTA_THRESHOLD_S and v == STATE_VER):
        return s
    return EMPTY_STATE.copy()


def write_state(conf, tmux_state) -> None:
    data = {
            'timestamp': _now(),
            'ver': STATE_VER,
            'tmux': tmux_state
            }

    try:
        with open(conf['state_f_path'], 'w') as f:
            f.write(
                json.dumps(
                    data,
                    indent=4,
                    sort_keys=True,
                    separators=(',', ': '),
                    ensure_ascii=False))
        # self.logger.debug('wrote cache: {}'.format(self._cache))
    except IOError as e:
        raise e


def _read_dict_from_file(file_loc) -> dict:
    if not (os.path.isfile(file_loc) and os.access(file_loc, os.R_OK)):
        return {}

    try:
        with open(file_loc, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f'error trying to read file {file_loc}')
        return {}


def _now() -> int:
    return int(datetime.now().timestamp())


