#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'thaidang'

import codecs
from sets import Set

def read_lines(infile):
    fi = codecs.open(infile, 'r', 'utf-8')
    lines = fi.readlines()
    lines = [s.rstrip('\r\n') for s in lines]
    fi.close()
    while '' in lines:
        lines.remove('')
    return lines

def read_tokens(inputFile):
    token_list = []
    lines = read_lines(inputFile)
    for line in lines:
        tokens = line.split(u" ")
        for token in tokens:
            if token != u"":
                token_list.append(token)
    return token_list

def load_tagSet(tagSetFile):
    return read_lines(tagSetFile)


def load_unigram(tag1gramFile):
    unigram = {}
    N = 0 # Sample size
    lines = read_lines(tag1gramFile)
    for line in lines:
        token_list = line.split(" ")
        unigram[token_list[0]] = int(token_list[1])
        N+=int(token_list[1])
    return unigram, len(unigram.keys())-2, N

def load_bigram(tag2gramFile):
    bigram = {}
    line_list = read_lines(tag2gramFile)
    for line in line_list:
        token_list = line.split(" ")
        bigram[token_list[0] + " " + token_list[1]] = int(token_list[2])
    return bigram

def load_trigram(tag3gramFile):
    trigram = {}
    line_list = read_lines(tag3gramFile)
    for line in line_list:
        token_list = line.split(" ")
        trigram[token_list[0] + " " + token_list[1] + " " + token_list[2]] = int (token_list[3])
    return trigram


def load_emission(emissionFile):
    emission = {}
    N = 0
    line_list = read_lines(emissionFile)
    for line in line_list:
        token_list = line.split(" ")
        if len(token_list) == 3:
            emission[token_list[0] + " " + token_list[1]] = int(token_list[2])
            N += int(token_list[2])
    return emission, N

def load_lexicon(lexiconFile):
    lexicon = {}
    line_list = read_lines(lexiconFile)
    for line in line_list:
        pos = line.index(" ")
        lexicon[line[:pos]] = line[pos+1:]
    return lexicon