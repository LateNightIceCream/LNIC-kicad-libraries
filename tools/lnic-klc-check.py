#!/usr/bin/env python3
'''
checks all kicad symbols / footprints in the LNIC library
using the kicad-library-utils scripts (git submodule)
'''

import os
import sys
import subprocess
import logging
import pathlib
from fnmatch import fnmatch

logger = None

SYMBOL_DIRECTORY = '../src/symbols'
FOOTPRINT_DIRECTORY = '../src/footprints'
#BODY3D_DIRECTORY = '../src/footprints'
KLC_CHECK_SYMBOL_SCRIPT = 'kicad-library-utils/klc-check/check_symbol.py'
KLC_CHECK_FOOTPRINT_SCRIPT = 'kicad-library-utils/klc-check/check_footprint.py'
KICAD_SYM_FILE_ENDING = '.kicad_sym'
KICAD_FOOTPRINT_FILE_ENDING = '.kicad_mod'

# just for pretty logging
class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def submodule_exists():
    if os.path.isdir('kicad-library-utils/'):
        return True
    else:
        return False


def check_symbols(sym_dir, args):
    files = list(pathlib.Path(sym_dir).glob('*' + KICAD_SYM_FILE_ENDING))
    for f in files:
        subprocess.run([KLC_CHECK_SYMBOL_SCRIPT, f, ' '.join(args)])


def check_footprints(ftp_dir, args):
    root = FOOTPRINT_DIRECTORY
    pattern = '*' + KICAD_FOOTPRINT_FILE_ENDING

    for path, subdirs, files in os.walk(root):
        for name in files:
            if fnmatch(name, pattern):
                fdir = os.path.join(path, name)
                subprocess.run([KLC_CHECK_FOOTPRINT_SCRIPT, fdir, ' '.join(args)])


if __name__ == '__main__':

    logger = logging.getLogger('lnic-klc-check')
    ch = logging.StreamHandler()
    ch.setFormatter(CustomFormatter())
    ch.setLevel(logging.DEBUG)
    logger.addHandler(ch)

    if not submodule_exists():
        logger.error('\'kicad-library-utils\' submodule not found. run: git submodule update --init')
        exit(-1)
    if not os.path.isdir(SYMBOL_DIRECTORY):
        logger.error('Symbol directory \'%s\' not found' % (SYMBOL_DIRECTORY))
        exit(-2)
    if not os.path.isdir(FOOTPRINT_DIRECTORY):
        logger.error('Symbol directory \'%s\' not found.' % (SYMBOL_DIRECTORY))
        exit(-3)

    args = sys.argv[1:]

    print('===================')
    print('CHECKING SYMBOLS')
    print('===================')
    check_symbols(SYMBOL_DIRECTORY, args)
    print('===================')
    print('CHECKING FOOTPRINTS')
    print('===================')
    check_footprints(FOOTPRINT_DIRECTORY, args)
