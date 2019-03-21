#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'thaidang'

import codecs
from sets import Set
import sys
import os

def get_lines(inFile):
    fi = codecs.open(inFile, 'r', 'utf-8')
    lines = fi.readlines()
    fi.close()
    lines = [s.rstrip('\r\n') for s in lines]
    while '' in lines:
        lines.remove('')
    return lines

def get_tokens(inFile):
    lines = get_lines(inFile)
    tokens_list = []
    for line in lines:
        tokens = line.split(' ')
        for token in tokens:
            if token != '':
                tokens_list.append(token)
    return tokens_list