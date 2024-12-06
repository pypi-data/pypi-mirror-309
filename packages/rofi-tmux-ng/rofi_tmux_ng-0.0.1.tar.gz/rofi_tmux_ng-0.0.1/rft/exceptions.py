#!/usr/bin/env python
# -*- coding: utf-8 -*-

class TerminateTaskGroup(Exception):
    """Exception raised to terminate a task group."""

    def __init__(self, exit_code=1, store_state=False):
        self.exit_code = exit_code
        self.store_state = store_state

