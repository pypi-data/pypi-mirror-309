#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import rft.daemon as daemon


@click.command
@click.option(
    '--debug',
    is_flag=True,
    help='Enables logging at debug level.')
def main(debug):
    """RFT (rofi-tmux) switcher."""
    d = daemon.Daemon(debug=debug)
    d.start()


if __name__ == "__main__":
    main()
