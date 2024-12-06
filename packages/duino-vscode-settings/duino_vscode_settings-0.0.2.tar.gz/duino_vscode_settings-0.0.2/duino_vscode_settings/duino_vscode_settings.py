#!/usr/bin/env python3
"""
This program takes the same arguments as the compiler, extracts the -D (defines) and -I
(include paths) and generates a VSCode settings file with those options.

It also supports multiple configurations, so you could have say an Arduino configuration
and a Linux configuration.

Usage:
    make_vscode_settings.py filename -- compiler options
"""

import argparse
import json
import os
import shlex
import sys

from typing import Any, Dict, List, Union

OPTION_DEFS: List[str] = []


# pylint: disable=too-many-instance-attributes
class Settings:
    """Class which will create a VSCode c_cpp_properties.json given a compile command line."""

    def __init__(self):
        self.option_defs: List[str] = []
        self.option_incs: List[str] = []
        self.option_prefix: str = ''
        self.workspace = os.getcwd()
        self.option: str = ''
        self.compiler_path = 'g++'
        self.compiler_c_standard: str = 'gnu11'
        self.compiler_cpp_standard: str = 'g++17'
        self.debug = self.debug_disabled_func

    @staticmethod
    def debug_enabled_func(*args) -> None:
        """Function called when debugging is enabled."""
        print(*args)

    @staticmethod
    def debug_disabled_func(*_args) -> None:
        """Function called when debugging is disabled."""

    def set_debug(self, dbg: bool) -> None:
        """Sets the debug function."""
        if dbg:
            self.debug = self.debug_enabled_func
        else:
            self.debug = self.debug_disabled_func

    def process_def(self, defn: str) -> None:
        """Adds a define to self.option_defs."""
        self.debug(f'  process_def({defn})')
        self.option_defs.append(defn)

    def process_inc(self, inc: str) -> None:
        """Adds a directory to self.option_incs, adding workspaceFolder as needed"""
        self.debug(f'  process_inc({inc})')
        if inc.startswith('/tmp/'):
            return
        if inc.startswith(self.workspace):
            inc = '${workspaceFolder}/' f'{inc[len(self.workspace):]}'
        self.debug(f'  adding INCLUDE {inc}')
        self.option_incs.append(inc)

    def process_iprefix(self, prefix: str) -> None:
        """Sets a prefix to use with -iwithprefixbefore"""
        self.debug(f'  process_iprefix({prefix})')
        if prefix.endswith('/'):
            self.option_prefix = prefix[:-1]
        else:
            self.option_prefix = prefix

    def process_iwithprefixbefore(self, inc: str) -> None:
        """Adds the prefix directory to `inc`."""
        self.debug(f'  process_iwithprefixbefore({inc})')
        if inc.startswith('/'):
            self.process_inc(f'{self.option_prefix}{inc}')
        else:
            self.process_inc(f'{self.option_prefix}/{inc}')

    def process_std(self, option: str) -> None:
        """Handles the -std=option"""
        self.debug(f'  process_std({option})')
        if '++' in self.compiler_path:
            self.compiler_cpp_standard = option
        else:
            self.compiler_c_standard = option

    def process_at(self, filename: str) -> None:
        """Process an option file specified as @filename"""
        self.debug(f'  process_at({filename})')
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                self.process_option_line(line)

    OPTIONS = {
        '-D': process_def,
        '-I': process_inc,
        '-iprefix': process_iprefix,
        '-iwithprefixbefore': process_iwithprefixbefore,
        '-std': process_std,
        '@': process_at,
    }

    def process_option(self, option: str) -> None:
        """Processes a single option."""
        self.debug(f'process_option({option})')
        if self.option:
            # We're processing the actual option value
            fn = Settings.OPTIONS[self.option]
            self.option = ''
            fn(self, option)
            return
        if option in Settings.OPTIONS:
            # We're proceesing an option who's value is the next argument
            self.option = option
            return
        for key, fn in Settings.OPTIONS.items():
            if option.startswith(f'{key}='):
                # Hande key=val
                fn(self, option[len(key) + 1:])
                return
            if option.startswith(key):
                # Handle keyval (like -Ddir)
                fn(self, option[len(key):])

    def process_option_line(self, line: str) -> None:
        """Processes a single line from an option file."""
        line_options = shlex.split(line, posix=True)
        for line_option in line_options:
            self.process_option(line_option)

    def find_configuration(self, configurations: List, cfg_name: str) -> Dict:
        """
        Searches for a named configuration and returns it, if found.
        If not found, a new empty configuration is created.
        """
        for configuration in configurations:
            if 'name' in configuration:
                if configuration['name'] == cfg_name:
                    return configuration
        configuration = {'name': cfg_name}
        configurations.append(configuration)
        return configuration

    def set_if_not_in(self, d: Dict, key: str, val: Any) -> None:
        """If `key` doesn't exist in the dictionary, then it will set it to `value`."""
        if key not in d:
            d[key] = val

    def make_settings(self, filename: str, config_name: str,
                      options: List[str]):
        """Makes a settings file."""
        self.compiler_path = options[0]

        for option in options:
            self.process_option(option)

        self.option_defs.sort()

        # Read in the existing config, if it exists
        cfg = {}
        if os.path.isfile(filename):
            print(f'Reading {filename} ...')
            with open(filename, encoding="utf-8") as f:
                cfg = json.loads(f.read())
        if 'configurations' not in cfg:
            cfg['configurations'] = []

        configurations = cfg['configurations']
        configuration = self.find_configuration(configurations, config_name)
        self.set_if_not_in(configuration, 'compilerPath', self.compiler_path)
        if config_name == 'Linux':
            self.set_if_not_in(configuration, 'compilerArgs', '-m64')
            self.set_if_not_in(configuration, 'intelliSenseMode', 'gcc-x64')
        else:
            self.set_if_not_in(configuration, 'intelliSenseMode', 'gcc-arm')
        configuration['defines'] = self.option_defs
        configuration['includePath'] = self.option_incs
        print(configuration['includePath'])
        self.set_if_not_in(configuration, 'cStandard',
                           self.compiler_c_standard)
        self.set_if_not_in(configuration, 'cppStandard',
                           self.compiler_cpp_standard)
        configuration['mergeConfigurations'] = True

        print(f'Writing {filename} ...')
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(cfg, indent=4, sort_keys=True))

        print('Done')

    def parse_args(self) -> Union[argparse.Namespace, None]:
        """Parses the command line arguments."""
        default_config = 'Arduino'
        parser = argparse.ArgumentParser(
            usage='%(prog)s [options] FILENAME -- COMPILER-OPTIONS ...',
            add_help=False,
            description=
            'Generates a VSCode settings file using compiler options.',
        )
        parser.add_argument(
            '-c',
            '--config',
            type=str,
            help=
            f'Name of configuration to write/update (default {default_config}).',
            default=default_config,
        )
        parser.add_argument(
            '-d',
            '--debug',
            action='store_true',
            help='Turn on debug mode',
            default=False,
        )
        parser.add_argument('-h',
                            '--help',
                            action='store_true',
                            help='Print this help and exit.')
        parser.add_argument('filename',
                            metavar='FILENAME',
                            type=str,
                            help='File to store settings in.')
        parser.add_argument('options',
                            metavar='COMPILER-OPTIONS',
                            type=str,
                            nargs='*',
                            help='Compiler options.')
        try:
            args = parser.parse_args(sys.argv[1:])
        except SystemExit:
            return None
        if args.help:
            parser.print_help()
            return None

        self.set_debug(args.debug)

        return args

    def main(self):
        """Main body of the program."""
        args = self.parse_args()
        if not args:
            return
        self.debug('Filename =', args.filename)
        self.debug('Options =', args.options)
        self.make_settings(args.filename, args.config, args.options)


if __name__ == '__main__':
    settings = Settings()
    settings.main()
