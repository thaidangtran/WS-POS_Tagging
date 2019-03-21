#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'thaidang'

from ws.segmenting import *
from posTagger.POSTagger import *
from posTagger.train_model import *
import re

class trainHMM:
	def __init__(self, training_file):
		t = train()
		add_extra_label(training_file, 'pos.train.txt')
		t.generate_lexicon('pos.train.txt')
		t.generate_unigram('pos.train.txt')
		t.generate_bigram('pos.train.txt')
		t.generate_trigram('pos.train.txt')
		t.generate_emission('pos.train.txt')

if len(sys.argv) == 2:
	training_file = sys.argv[1]
	tr = trainHMM(training_file)
