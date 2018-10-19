#!/bin/env python3

import click
import logging
import coloredlogs

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
    if debug:
        coloredlogs.install(level=logging.DEBUG, fmt="%(levelname)s %(message)s")
    else:
        coloredlogs.install(level=logging.INFO, fmt="%(levelname)s %(message)s")
    ctx.ensure_object(Context)
    ctx.obj.debug = debug
    ctx.obj.config = Config(config_file)


@click.command()
@click.pass_context
def install_game(ctx):
    actions.install_game.run(config=ctx.obj.config)


@click.command()
@click.pass_context
def list_mods(ctx):
    for name, mod_config in ctx.obj.config.mods.items():
        click.echo("%-20s: %s" % (name, mod_config.source))


@click.command()
@click.argument("name")
@click.pass_context
def build_mod(ctx, name):
    mod_config = ctx.obj.config.mods[name]
    actions.build_mod.run(name=name, config=mod_config)

@click.command()
@click.argument("name")
@click.pass_context
def install_mod(ctx, name):
    mod_config = ctx.obj.config.mods[name]
    actions.install_mod.run(name=name, config=mod_config)


main.add_command(install_game)
main.add_command(list_mods)
main.add_command(build_mod)
main.add_command(install_mod)

if __name__ == '__main__':
    main(obj=Context())
