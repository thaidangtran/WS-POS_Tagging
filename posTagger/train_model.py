#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'thaidang'

from count_ngram.io import *
from count_ngram.counting import *
from sets import Set

__author__ = 'thai'

class train:

    def __init__(self):
        return

    def generate_lexicon(self, inFile):
        print 'generating lexicon ...'
        #lines = get_lines(inFile)
        tokens = get_tokens(inFile)
        lexicons = {}
        for token in tokens:
            if '\\' in token:
                pos = token.index('\\')
                if not lexicons.has_key(token[:pos]):
                    lexicons[token[:pos]] = token[pos+1:]
                else:
                    s = lexicons.get(token[:pos])
                    if token[pos+1:] not in s:
                        lexicons[token[:pos]] = s + ' ' + token[pos+1:]
        fo = codecs.open('pos_lexicons.txt', 'wb', 'utf-8')
        for key in lexicons.keys():
            fo.write(key + ' ' + lexicons.get(key) + '\n')
        fo.close()
        return None

    def generate_unigram(self, inFile):
        print 'generating unigram ... '
        lines = get_lines(inFile)
        tagSet = []
        unigram = {}
        for line in lines:
            tokens = line.split(' ')
            for token in tokens:
                if '\\' in token:
                    pos = token.index('\\')
                    if not unigram.has_key(token[pos+1:]):
                        unigram[token[pos+1:]] = 1
                    else:
                        count = unigram.get(token[pos+1:]) + 1
                        unigram[token[pos+1:]] = count
                else:
                    if not unigram.has_key(token):
                        unigram[token] = 1
                    else:
                        count = unigram.get(token) + 1
                        unigram[token] = count
        fo = codecs.open('pos_unigram.txt', 'wb', 'utf-8')
        fo1 = codecs.open('pos_tagset.txt', 'wb', 'utf-8')
        for key in unigram.keys():
            fo1.write(key + '\n')
            fo.write(key + ' ' + str(unigram.get(key)) + '\n')
        fo.close()
        fo1.close()
        return None

    def get_tag(self, token):
        if '\\' in token:
            pos = token.index('\\')
            tag = token[pos+1:]
        else:
            tag = token
        return tag

    def generate_bigram(self, inFile):
        print 'generating bigram ...'
        lines = get_lines(inFile)
        bigram = {}
        for line in lines:
            tokens = line.split(' ')
            for i in range(len(tokens)-1):
                s = self.get_tag(tokens[i]) + ' ' + self.get_tag(tokens[i+1])
                if not bigram.has_key(s):
                    bigram[s] = 1
                else:
                    count = bigram.get(s) + 1
                    bigram[s] = count
        fo = codecs.open('pos_bigram.txt', 'wb', 'utf-8')
        for key in bigram.keys():
            fo.write(key + ' ' + str(bigram.get(key)) + '\n')
        fo.close()
        return None

    def generate_trigram(self, inFile):
        print 'generating trigram ...'
        lines = get_lines(inFile)
        trigram = {}
        for line in lines:
            tokens = line.split(' ')
            for i in range(len(tokens)-2):
                s = self.get_tag(tokens[i]) + ' ' + self.get_tag(tokens[i+1]) + ' ' + self.get_tag(tokens[i+2])
                if not trigram.has_key(s):
                    trigram[s] = 1
                else:
                    count = trigram.get(s) + 1
                    trigram[s] = count
        fo = codecs.open('pos_trigram.txt', 'wb', 'utf-8')
        for key in trigram.keys():
            fo.write(key + ' ' + str(trigram.get(key)) + '\n')
        fo.close()
        return None

    def generate_emission(self, inFile):
        print 'generating emission ...'
        emission = {}
        lines = get_lines(inFile)
        for line in lines:
            tokens = line.split(' ')
            for i in range(len(tokens)):
                if '\\' in tokens[i]:
                    pos = tokens[i].index('\\')
                    tokens[i] = tokens[i][:pos] + ' ' + tokens[i][pos+1:]
                    if not emission.has_key(tokens[i]):
                        emission[tokens[i]] = 1
                    else:
                        count = emission.get(tokens[i]) + 1
                        emission[tokens[i]] = count
        fo = codecs.open('pos_emission.txt', 'wb', 'utf-8')
        for key in emission.keys():
            fo.write(key + ' ' + str(emission.get(key)) + '\n')
        fo.close()
        return None


# testing
t = train()
#add_extra_label('combination_00.txt', 'pos.train.txt')
#t.generate_lexicon('pos.train.txt')
#t.generate_unigram('pos.train.txt')
#t.generate_bigram('pos.train.txt')
#t.generate_trigram('pos.train.txt')
#t.generate_emission('pos.train.txt')








