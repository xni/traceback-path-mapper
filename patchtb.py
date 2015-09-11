#!/usr/bin/env python3

import argparse
import os
import re
import sys


class BaseError(Exception):
    pass


class ConfigNotFoundError(BaseError):
    pass


def patch_traceback(input_stream, output_stream, config):
    def _patch_path(matchobj):
        remote_path = matchobj.group('path')
        for replace_option in config:
            if remote_path.startswith(replace_option[0]):
                remote_path = remote_path.replace(*replace_option)
                break
        patched_line = '{}{}{}'.format(
            matchobj.group(1),
            remote_path,
            matchobj.group(3))
        return patched_line

    tb_line = re.compile(
        r'(\s*File ")(?P<path>.*)(", line \d+, in \w+\s*)'
    )
    for line in input_stream:
        output_line = tb_line.sub(_patch_path, line)
        output_stream.write(output_line)


def main():
    arguments = parse_arguments()
    config = read_config(arguments.config)
    patch_traceback(arguments.input, arguments.output, config)


def read_config(config_file):
    config = []
    for line in config_file:
        strip_line = line.strip()
        if strip_line.startswith('#'):
            continue
        if not strip_line:
            continue
        config.append(strip_line.split(':'))
    return config


def parse_arguments():
    def open_config_file(path):
        path = os.path.expanduser(path)
        if not os.path.exists(path):
            raise ConfigNotFoundError(path)
        return open(path, 'r')

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        help='Path to paths-mapping file',
                        type=open_config_file,
                        default='~/.patchtb')

    parser.add_argument('-i', '--input',
                        help='Path to input file (default=stdin)',
                        type=argparse.FileType('r'),
                        default=sys.stdin)

    parser.add_argument('-o', '--output',
                        help='Path to output file (default=stdout)',
                        type=argparse.FileType('w'),
                        default=sys.stdout)

    return parser.parse_args()


if __name__ == '__main__':
    sys.exit(main())

