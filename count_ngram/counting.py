#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'thaidang'

from io import *

def add_extra_label(inFile, outFile):
    lines = get_lines(inFile)
    for i in range(len(lines)):
        lines[i] = '<s> ' + '<s> ' + lines[i] + ' <e>'
    fo = codecs.open(outFile, 'wb', 'utf-8')
    for line in lines:
        fo.write(line + '\n')
    fo.close()
    return None

def count_unigram(inFile, outFile):
    print 'counting unigram ...'
    lines = get_lines(inFile)
    fo = codecs.open(outFile, 'wb', 'utf-8')
    unigram = {}
    for line in lines:
        tokens = line.split(' ')
        for token in tokens:
            if token != '':
                if not unigram.has_key(token):
                    unigram[token] = 1
                else:
                    count = unigram.get(token) + 1
                    unigram[token] = count
    for key in unigram.keys():
        fo.write(key + ' ' + str(unigram.get(key)) + '\n')
    fo.close()
    return None

def count_bigram(inFile, outFile):
    print 'counting bigram ... '
    fo = codecs.open(outFile, 'wb', 'utf-8')
    lines = get_lines(inFile)
    bigram = {}
    for line in lines:
        tokens = line.split(' ')
        for i in range(len(tokens)-1):
            s = tokens[i] + ' ' + tokens[i+1]
            if not bigram.has_key(s):
                bigram[s] = 1
            else:
                count = bigram.get(s) + 1
                bigram[s] = count
    for key in bigram.keys():
        fo.write(key + ' ' + str(bigram.get(key)) + '\n')
    fo.close()
    return None

def count_trigram(inFile, outFile):
    print 'counting trigram ...'
    lines = get_lines(inFile)
    fo = codecs.open(outFile, 'wb', 'utf-8')
    trigram = {}
    for line in lines:
        tokens = line.split(' ')
        for i in range(len(tokens)-2):
            s = tokens[i] + ' ' + tokens[i+1] + ' ' + tokens[i+2]
            if not trigram.has_key(s):
                trigram[s] = 1
            else:
                count = trigram.get(s) + 1
                trigram[s] = count
    for key in trigram.keys():
        fo.write(key + ' ' + str(trigram.get(key)) + '\n')
    fo.close()
    return None

# === train model for pos-tagging ===#

