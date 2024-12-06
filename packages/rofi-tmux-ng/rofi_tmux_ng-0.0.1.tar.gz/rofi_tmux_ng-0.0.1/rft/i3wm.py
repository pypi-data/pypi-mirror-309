#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .window_manager import WindowManager
from .exceptions import TerminateTaskGroup
import asyncio
import i3ipc
from i3ipc.aio import Connection
import logging
from re import escape
from collections import defaultdict

xprop_hidden_win_flag = b'_NET_WM_STATE_HIDDEN'

class i3WM(WindowManager):
    """Abstraction to handle i3wm"""

    def __init__(self, conf, tmux) -> None:
        """Constructor

        """
        self._conf = conf
        self._tmux = tmux
        self.logger = logging.getLogger(__name__)
        super(i3WM, self).__init__()

    async def start(self):
        self._i3 = await Connection().connect()
        self._i3.on('shutdown', self.on_shutdown)
        await self._i3.main()


    async def focus_tmux_window(self, session) -> None:
        """Focuses window where given tmux session is running in

        :session: tmux session whose window to focus

        """
        if not session:
            return

        tree = await self._i3.get_tree()
        tmux_win = self._find_tmux_window(session, tree)
        if tmux_win:
            self.logger.debug('i3 focusing window running tmux session [{}]'.format(session['name']))
            await tmux_win.command('focus')

    async def is_tmux_win_visible(self, session) -> bool:
        """Verifies if window where given tmux session is running in is visible

        :session: tmux session whose visibility to check

        """
        if not session:
            return False

        tree = await self._i3.get_tree()
        tmux_win = self._find_tmux_window(session, tree)
        if tmux_win:
            return await self._is_win_visible(tmux_win, tree)
        return False


    async def _is_win_visible(self, i3_win, tree) -> bool:
        """Verify if given i3ipc.Con housing our tmux session is visible on our
        screen(s).

        :i3_win: i3ipc.Con housing tmux session whose visibility to test.

        """

        is_win_on_any_visible_ws = await self._is_win_on_any_visible_ws(i3_win, tree)
        if not is_win_on_any_visible_ws:
            return False

        try:
            xprop = await check_output(['xprop', '-id', str(i3_win.window)])
            # print(f'XROP is visible: {xprop_hidden_win_flag not in xprop}')
            return xprop_hidden_win_flag not in xprop
        except FileNotFoundError:
            # if xprop not found, fall back to just checking if tmux win is on our current worksapce:
            self.logger.debug('xprop utility is not found - please install it.')
            self.logger.debug('will decide visibility simply by checking if tmux is on our current workspace')
            # return self._is_tmux_win_on_current_ws(i3_win, tree)
            return is_win_on_any_visible_ws   # TODO: always true here, is this what we want?


    def _is_tmux_win_on_current_ws(self, i3_win, tree) -> bool:
        """Verifies if tmux is in the current (ie focused) i3 workspace

        :i3_win: i3ipc.Con housing our tmux session

        """
        i3_ws = i3_win.workspace()
        return i3_ws and i3_ws.id == tree.find_focused().workspace().id


    async def _is_win_on_any_visible_ws(self, i3_win, tree) -> bool:
        """Verifies if i3 win is on a ws that's on an active output, i.e.
        on a currently visible workspace

        :i3_win: i3ipc.Con housing our tmux session

        """
        outputs = await self._i3.get_outputs()
        ws_list = [output.current_workspace for output in outputs if output.active]
        i3_ws_id = i3_win.workspace().id
        for ws in tree.workspaces():
            if ws.name in ws_list:
                # for w in ws.leaves():
                    # if i3_win.window == w.window:
                        # return True
                if ws.id == i3_ws_id:
                    return True
        return False


    def _find_tmux_window(self, session, tree) -> i3ipc.Con:
        """Finds and returns i3 Container instance housing tmux window that's
        currently attached to provided session.

        :session: tmux session whose window to find.

        """
        session_name = escape(session['name'])
        win = self._tmux.get_window(session['active_window_id'])
        window_name = escape(win['name'])
        rgx = self._conf['tmux_title_rgx'].format_map(defaultdict(str,
                session = session_name,
                window = window_name
        ))

        # just in case filter by container type - we want regular & floating window containers:
        tmux_win = [w for w in tree.find_named(rgx) if w.type.endswith('con')]

        if tmux_win:
            if len(tmux_win) > 1:
                self.logger.debug('found [{}] windows using regex [{}], but expected 1'
                        .format(len(tmux_win), rgx))
                self.logger.debug('you should likely make conf.tmux_title_rgx more limiting')
            return tmux_win[0]

        self.logger.debug('found no windows using regex [{}]'.format(rgx))
        return None


    def on_shutdown(self, i3conn, e):
        self.logger.info(f'on_shutdown() invoked with e.change = {e.change}, terminating...')
        raise TerminateTaskGroup(5, store_state=e.change == 'restart')


# check_output for asyncio.
# from https://stackoverflow.com/a/70120267/1803648
async def check_output(args, **kwargs) -> bytes:
    p = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        **kwargs,
    )
    stdout_data, stderr_data = await p.communicate()
    return stdout_data if p.returncode == 0 else b''

