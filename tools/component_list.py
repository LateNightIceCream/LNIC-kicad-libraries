#!/usr/bin/env python3
'''
lists all components in the kicad libraries in a markdown table
'''

import os
import sys
import pathlib

from mdutils.mdutils import MdUtils

OUTFILE = '../component_list.md'

SYMBOL_DIRECTORY = '../src/symbols'
FOOTPRINT_DIRECTORY = '../src/footprints'
KICAD_SYM_FILE_ENDING = '.kicad_sym'

def get_symbol_files(dir):
    files = list(pathlib.Path(dir).glob('*' + KICAD_SYM_FILE_ENDING))
    return files

def is_symbol_identifier_line(line):
    return line.strip().startswith('(symbol') and '(in_bom' in line

def get_symbol_name_from_identifier_line(line):
    return line.strip().split(' ')[1].strip('"')

def add_symbol_list(mdFile):
    files = list(pathlib.Path(SYMBOL_DIRECTORY).glob('*' + KICAD_SYM_FILE_ENDING))
    symbols = {}
    for filename in files:
        symbols[filename] = []
        with open(filename, 'r') as f:
            for line in f.readlines():
                if is_symbol_identifier_line(line):
                    name = get_symbol_name_from_identifier_line(line)
                    symbols[filename].append(name)

    for lib in symbols:
        title = lib.stem
        #mdFile.new_header(level=2, title=title)
        #mdFile.new_paragraph(title, bold_italics_code='b')
        table_rows = [title]
        for sym in symbols[lib]:
            table_rows.append(sym)

        nrows = len(table_rows)
        if nrows > 0:
            mdFile.new_table(columns = 1, rows = nrows, text = table_rows, text_align='left')


if __name__ == '__main__':

    try:
        mdFile = MdUtils(file_name=OUTFILE)
        mdFile.new_header(level=1, title='Component List')
        mdFile.new_header(level=2, title='Symbols')
        add_symbol_list(mdFile)
        mdFile.new_header(level=2, title='Footprints')
        # TODO: list footprints
        mdFile.create_md_file()

    except Exception as e:
        print(e)
        exit(-1)
