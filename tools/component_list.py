#!/usr/bin/env python3
'''
lists all components in the kicad libraries in a markdown table
'''

import os
import sys
import pathlib
import re

from mdutils.mdutils import MdUtils

OUTFILE = '../component_list.md'

SYMBOL_DIRECTORY = '../src/symbols'
FOOTPRINT_DIRECTORY = '../src/footprints'
KICAD_SYM_FILE_ENDING = '.kicad_sym'
KICAD_FTP_FILE_ENDING = '.kicad_mod'
KICAD_FTP_LIB_FILE_ENDING = '.pretty'


class Symbol:
    def __init__(self, name, footprint):
        self.name = name
        self.footprint = footprint

class SymbolFile:
    def __init__(self, path):
        self.path = path
        self.symbols = self.init_from_path(path)

    def init_from_path(self, path):
        self.path = path
        symbols = []
        with open(path, 'r') as f:
            symbol = None
            for line in f.readlines():
                if self._is_line_identifier(line):
                    start = True
                    name = self._get_symbol_name_from_line(line)
                    symbol = Symbol(name, "")

                if symbol and self._is_line_footprint(line):
                    fp = self._get_footprint_from_line(line)
                    symbol.footprint = fp
                    symbols.append(symbol)
                    symbol = None # we're done!

        return symbols

    @staticmethod
    def _is_line_identifier(line):
        if not line.strip().startswith("(symbol"):
            return False
        name = SymbolFile._get_symbol_name_from_line(line)
        # ignore "(symbol" names ending with _d_d (e.g. _0_1
        return not re.search("_[0-9]+_[0-9]+$", name)

    @staticmethod
    def _get_symbol_name_from_line(line):
        return line.strip().split(' ')[1].strip('"')

    @staticmethod
    def _is_line_footprint(line):
        return line.strip().startswith("(property \"Footprint\"")

    @staticmethod
    def _get_footprint_from_line(line):
        return line.strip().strip("\n").split(" ")[2].strip('"')



class Footprint:
    def __init__(self, name, model):
        self.name = name
        self.model = model

class FootprintLibrary:
    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.footprints = self.init_from_path(self.path)

    def init_from_path(self, libpath):
        self.path = libpath
        footprints = []
        for filepath in self.get_files():
            with open(filepath, 'r') as f:
                footprint = None
                for line in f.readlines():
                    if not footprint and line.strip().startswith("(footprint"):
                        name = self._get_footprint_name_from_line(line)
                        footprint = Footprint(name, "")
                    elif footprint:
                        # we just take the first model, there might be others but
                        # this is ignored here
                        if line.strip().startswith("(model"):
                            model = self._get_model_from_line(line)
                            footprint.model = model
                            footprints.append(footprint)
                            footprint = None
                            break # we're done with this footprint
        return footprints

    def get_files(self):
        files = list(self.path.glob('*' + KICAD_FTP_FILE_ENDING))
        return files

    @staticmethod
    def _get_footprint_name_from_line(line):
        return line.strip().split(' ')[1].strip('"')

    @staticmethod
    def _get_model_from_line(line):
        return line.strip().strip("\n").split(" ")[1].strip('"')


def get_symbol_files():
    files = list(pathlib.Path(SYMBOL_DIRECTORY).glob('*' + KICAD_SYM_FILE_ENDING))
    symfiles = []
    for filename in files:
        symfiles.append(SymbolFile(filename))
    return symfiles


def get_footprint_libs():
    dirs = list(pathlib.Path(FOOTPRINT_DIRECTORY).glob('*' + KICAD_FTP_LIB_FILE_ENDING))
    libs = []
    for libpath in dirs:
        libs.append(FootprintLibrary(libpath))
    return libs


def add_symbol_list(mdFile):

    symfiles = get_symbol_files()

    table_rows = ["Symbol", "Footprint"]

    for symfile in symfiles:
        title = symfile.path.stem
        #mdFile.new_header(level=3, title=title)

        for symbol in symfile.symbols:
            table_rows.append(symbol.name)
            table_rows.append(symbol.footprint if symbol.footprint else "–")

    nrows = len(table_rows) // 2
    if nrows > 0:
        mdFile.new_table(columns = 2, rows = nrows, text = table_rows, text_align='left')


def add_footprint_list(mdFile):

    footprint_libs = get_footprint_libs()

    table_rows = ["Footprint", "3D Model?"]
    
    for lib in footprint_libs:
        for footprint in lib.footprints:
            table_rows.append(footprint.name)
            table_rows.append("no" if footprint.model == "" else "yes")

    nrows = len(table_rows) // 2
    if nrows > 0:
        mdFile.new_table(columns = 2, rows = nrows, text = table_rows, text_align='left')


if __name__ == '__main__':

    try:
        mdFile = MdUtils(file_name=OUTFILE)
        mdFile.new_header(level=1, title='Component List')
        mdFile.new_header(level=2, title='Symbols')
        add_symbol_list(mdFile)
        mdFile.new_header(level=2, title='Footprints')
        add_footprint_list(mdFile)
        mdFile.create_md_file()

    except Exception as e:
        print(e)
        exit(-1)
