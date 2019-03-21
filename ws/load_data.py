#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'thai'

from count_ngram.io import *

class load_data:

    def __init__(self):
        return

    def load_dictionary(self, dictFile):
        vn_dict = Set([])
        lines = get_lines(dictFile)
        vn_dict = Set(lines)
        return vn_dict

    def load_unigram(self, unigramFile):
        unigram = {}
        lines = get_lines(unigramFile)
        for line in lines:
            tokens = line.split(u' ')
            if len(tokens) == 2:
                unigram[tokens[0]] = int(tokens[1])
        return unigram, len(unigram.keys())

    def load_bigram(self, bigramFile):
        bigram = {}
        lines = get_lines(bigramFile)
        for line in lines:
            tokens = line.split(u' ')
            if len(tokens) == 3:
                bigram[tokens[0] + ' ' + tokens[1]] = int(tokens[2])
        return bigram



