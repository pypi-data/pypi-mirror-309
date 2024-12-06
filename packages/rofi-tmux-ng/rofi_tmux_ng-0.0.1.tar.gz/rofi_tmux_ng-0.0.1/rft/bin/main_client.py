#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# TODO: consider pyro5 for rpc

import click
import rft.client as rft
import rft.version as version


@click.group
@click.pass_context
@click.option(
    '--debug',
    is_flag=True,
    help='Enables logging at debug level.')
def main(ctx, debug):
    """Client (rofi-tmux) switcher."""
    ctx.obj = rft.Client(debug=debug)


@main.command
@click.pass_obj
def ss(ctx):
    """Switch tmux session.

    :param ctx: context
    """
    ctx.send_cmd('ss')


@main.command
@click.pass_obj
def ks(ctx):
    """Kill tmux session.

    :param ctx: context
    """
    ctx.send_cmd('ks')


@main.command
@click.option(
    '--session_name',
    default='',
    help='limit the scope to this this session')
@click.option(
    '--global_scope',
    default=True,
    type=bool,
    help='true, if you want to consider all windows')
@click.pass_obj
def sw(ctx, session_name, global_scope):
    """Switch tmux window.

    :param ctx: context
    :param session_name: tmux session name
    :param global_scope: True to consider all windows
    """
    ctx.send_cmd(f'sw {int(global_scope)} {session_name}')


@main.command
@click.option(
    '--session_name',
    default='',
    help='limit the scope to this this session')
@click.option(
    '--global_scope',
    default=True,
    type=bool,
    help='true, if you want to consider all windows')
@click.pass_obj
def kw(ctx, session_name, global_scope):
    """Kill tmux window.

    :param ctx: context
    :param session_name: tmux session name
    :param global_scope: True to consider all windows
    """
    ctx.send_cmd(f'kw {int(global_scope)} {session_name}')


@main.command
@click.pass_obj
def lp(ctx):
    """Load tmuxinator project.

    :param ctx: context
    """
    ctx.load_tmuxinator()


@main.command
def v():
    """Print version."""
    print(version.__version__)


if __name__ == "__main__":
    main()
