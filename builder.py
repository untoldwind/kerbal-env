#!/bin/env python3

import click

from lib.config import Config
from lib import actions

class Context:
    def __init__(self):
        self.debug = False

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.option('--config', 'config_file', default='config.toml')
@click.pass_context
def main(ctx, debug, config_file):
    ctx.ensure_object(Context)
    ctx.obj.debug = debug
    ctx.obj.config = Config(config_file)

@click.command()
@click.pass_context
def install_game(ctx):
    actions.install_game.run(config = ctx.obj.config, debug = ctx.obj.debug)

main.add_command(install_game)

if __name__ == '__main__':
    main(obj = Context())