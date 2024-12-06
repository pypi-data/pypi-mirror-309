#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .rft import RFT
from .tmux import Tmux
from .exceptions import TerminateTaskGroup
from .common import load_config, write_state
import logging
import sys
import asyncio
import signal
from tendo import singleton


class Daemon(object):

    def __init__(self, debug=False):
        """Initialize ."""

        self.lock = singleton.SingleInstance()
        self.logger = logging.getLogger(__name__)
        log_lvl = logging.DEBUG if debug else logging.INFO
        logging.basicConfig(stream=sys.stdout, level=log_lvl)

        self._config = load_config()

        self.tmux = Tmux(self._config)
        if self._config.get('wm') == 'i3':
            from .i3wm import i3WM
            self.wm = i3WM(self._config, self.tmux)
        else:
            self.wm = None
        self.rft = RFT(self._config, self.tmux, self.wm)


    def start(self):
        asyncio.run(self.main())


    async def listen_unix_sock(self):
        """Start listening on a UNIX socket accepting
           commands from client

        """
        server = await asyncio.start_unix_server(self.handle_client, path=self._config.get('socket_path'))
        async with server:
            await server.serve_forever()


    async def handle_client(self, reader, writer):
        req = (await reader.readline()).decode().rstrip('\n')
        self.logger.debug(f'received {req}')

        req = req.split(' ', 1)

        match(req[0]):
            case 'sw':
                req = req[1].split(' ', 1)
                await self.rft.switch_window(global_scope=bool(req[0]),
                                             session_name=req[1] if req[1] else None)
            case 'kw':
                req = req[1].split(' ', 1)
                await self.rft.kill_window(global_scope=bool(req[0]),
                                           session_name=req[1] if req[1] else None)
            case 'ss':
                await self.rft.switch_session()
            case 'ks':
                self.logger.error('[ks] not implemented')
            case _:
                self.logger.error(f'unknown command [{req[0]}]')

        # response = str(eval(request)) + '\n'
        # writer.write(response.encode('utf8'))
        # await writer.drain()
        writer.close()
        await writer.wait_closed()   # TODO: needed?


    async def main(self):
        try:
            async with asyncio.TaskGroup() as tg:
                if self.wm:
                    tg.create_task(self.wm.start())
                tg.create_task(self.tmux.run_tmux_cc())
                tg.create_task(self.listen_unix_sock())

                for signame in self._config.get('sw_signals'):
                    asyncio.get_running_loop().add_signal_handler(getattr(signal, signame),
                                                                  lambda: tg.create_task(self.rft.switch_window()))
                for signame in self._config.get('ss_signals'):
                    asyncio.get_running_loop().add_signal_handler(getattr(signal, signame),
                                                                  lambda: tg.create_task(self.rft.switch_session()))

                await asyncio.sleep(0.1)  # so tmux._tmux_proc is init'd & started first
                await self.tmux.init()
        except* TerminateTaskGroup as exc_group:
            ttg = exc_group.exceptions[0]
            self.logger.debug(f'TerminateTaskGroup caught, exiting with code {ttg.exit_code}, store_state={ttg.store_state}...')
            if ttg.store_state:
                self.logger.debug('storing state...')
                write_state(self._config, self.tmux.get_state())
                self.logger.debug('state stored')

            sys.exit(ttg.exit_code)

