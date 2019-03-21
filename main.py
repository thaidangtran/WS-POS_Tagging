#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'thaidang'

from ws.segmenting import *
from posTagger.POSTagger import *
import re

class preprocessing:
    def __init__(self):
        self.standard = {}
        lines = self.read_lines('standard.txt')
        for line in lines:
            tokens = line.split('/')
            self.standard[tokens[0]] = tokens[1]
        self.segment = segmenting('../ws-pos/ws_data/vietnamese_dictionary.txt', '../ws-pos/ws_data/ws_unigram.txt', '../ws-pos/ws_data/ws_bigram.txt')
        self.postagging = POSTagger('../ws-pos/pos_data/pos_trigram.txt', '../ws-pos/pos_data/pos_bigram.txt', '../ws-pos/pos_data/pos_unigram.txt', '../ws-pos/pos_data/pos_emission.txt',
                                    '../ws-pos/pos_data/pos_lexicons.txt', '../ws-pos/pos_data/pos_tagset.txt')
        print '\n=============================================\n'
        return

    def read_lines(self, infile):
        fi = codecs.open(infile, 'r', 'utf-8')
        lines = fi.readlines()
        fi.close()
        lines = [s.rstrip('\r\n') for s in lines]
        while '' in lines:
            lines.remove('')
        return lines

    def normalize_comments(self, sentence):
        sentence = re.sub('\s+', ' ', sentence)
        sentence = re.sub('\?+', '?', sentence)
        sentence = re.sub('\!+', '!', sentence)
        sentence = re.sub('\)+', ')', sentence)
        sentence = re.sub('\]+', ']', sentence)
        sentence = re.sub('\.+', '.', sentence)
        sentence = re.sub('\,+', ',', sentence)

        # check spelling
        for word in self.standard.keys():
            tokens = sentence.split(' ')
            sentence = ''
            for token in tokens:
                if word == token:
                    sentence += self.standard.get(word) + ' '
                else:
                    sentence += token + ' '
        return sentence.strip()

    def ws(self, sentence):
    	sentence = self.normalize_comments(sentence)
    	sentence = self.segment.segment_sentence(sentence)
    	return sentence

    def pos_tagging(self, sentence):
        sentence = self.segment.segment_sentence(sentence)
        return self.postagging.tagging_sentence(sentence)

    def pre_processing(self, sentence):
        sentence = self.normalize_comments(sentence)
        sentence = self.pos_tagging(sentence)
        return sentence

    def pre_processing_file(self, input_file, output_file, option):
        fo = codecs.open(output_file, "wb", "utf-8")
        lines = self.read_lines(input_file)
        for line in lines:
        	if option == 'ws':
        		fo.write(self.ws(line) + "\n")
        	if option == 'pos':
        		fo.write(self.pre_processing(line) + "\n")
        fo.close()
        return None

#================================================== testing ===========================================================#
pp = preprocessing()
#s = u'tôi,không đúng ng đã ntin # ????? dt ip4 này lởm lắm.'
#print pp.pre_processing(s)
#pp.pre_processing_file("D:/comments.txt", "D:/taggedDev.txt")
if len(sys.argv) == 4:
	input_file = sys.argv[1]
	output_file = sys.argv[2]
	option = sys.argv[3]
	pp.pre_processing_file(input_file, output_file, option)
else:
	print "The command is wrong, Please enter again!"