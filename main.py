import argparse
import logging
import os

import constants
from commands.run import execute_run
from commands.show import execute_show

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('commit-analysis')

# borrowed as a resolution from https://github.com/pre-commit/pre-commit/issues/217
os.environ.pop('__PYVENV_LAUNCHER__', None)


def add_command_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        'command', choices=constants.COMMANDS, default='run'
    )


def add_workdir_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '-d', '--workdir', dest='workdir', default='.', required=False
    )


def add_outputdir_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '-o', '--outputdir', dest='outputdir', default='.', required=False
    )


def add_commanddir_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '-c', '--commanddir', dest='commanddir', default='.', required=False
    )


def add_level_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '-l', '--level', dest='level', default=-1, required=False
    )


def add_filename_option(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        '-f', '--filename', dest='filename', default='commit-analysis.csv', required=False
    )


def parse_and_delegate(parser: argparse.ArgumentParser) -> None:
    args = parser.parse_args()
    logger.info(args.command)
    os.chdir(args.workdir)
    if args.command == "run":
        execute_run(int(args.level), args.commanddir, args.outputdir, args.filename)
    elif args.command == "show":
        execute_show(args.outputdir, args.filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='commit-analysis')
    add_workdir_option(parser)
    add_level_option(parser)
    add_filename_option(parser)
    add_outputdir_option(parser)
    add_commanddir_option(parser)
    add_command_option(parser)
    parse_and_delegate(parser)


