#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'thai'

from load_data import *
from tokenize import *
import math
import timeit

class segmenting:

    def __init__(self, vn_dict, unigram_file, bigram_file):
        # load data
        ld = load_data()
        print 'loading vietnamese dictionary'
        self.vn_dict = ld.load_dictionary(vn_dict)
        print 'loading unigram for word segmentation'
        self.unigram, self.vocab = ld.load_unigram(unigram_file)
        print 'loading bigram for word segmentation'
        self.bigram = ld.load_bigram(bigram_file)
        return

    def laplace(self, bigram_count, unigram_count, vocab):
        return math.log((bigram_count + 0.1)*1.0/(unigram_count + 0.1*vocab))

    def compute_bigram(self, cur_word, pre_word):
        bigram_count = self.bigram.get(pre_word + ' ' + cur_word)
        if bigram_count is None:
            bigram_count = 0
        unigram_count = self.unigram.get(pre_word)
        if unigram_count is None:
            unigram_count = 0
        return self.laplace(bigram_count, unigram_count, self.vocab)


    def compute_probability_of_sentence(self, sentence):
        sentence = '<s> ' + sentence + ' <e>'
        tokens = sentence.split(' ')
        prob = 0.0
        for i in range(1, len(tokens)):
            prob += self.compute_bigram(tokens[i], tokens[i-1])
        return prob

    # handle "overlaping" ambiguities
    def match_left_to_right(self, sentence):
        uni = uniStr()
        tokens = sentence.split(' ')
        result = []
        l = len(tokens)
        i = 0
        while i<l:
            # ignore special token that recognized
            if '_' in tokens[i]:
                result.append(tokens[i])
                i += 1
            else:
                word = tokens[i]
                max_word = word
                index = i
                count = 0
                for j in range(i+1, l):
                    word += '_' + tokens[j]
                    count += 1
                    if count == 5:
                        break
                    if uni.to_lower(word) in self.vn_dict:
                        max_word = word
                        index = j
                result.append(max_word)
                i = index + 1
        sentence = ' '.join(result).strip()
        return sentence

    def match_right_to_left(self, sentence):
        uni = uniStr()
        tokens = sentence.split(' ')
        result = []
        l = len(tokens)
        i = l-1
        while i >= 0:
            if '_' in tokens[i]:
                result.append(tokens[i])
                i -= 1
            else:
                word = tokens[i]
                max_word = word
                index = i
                count = 0
                i = i-1
                while i>= 0:
                    word = tokens[i] + '_' + word
                    count += 1
                    if count == 5:
                        break
                    if uni.to_lower(word) in self.vn_dict:
                        max_word = word
                        index = i
                    i = i - 1
                result.append(max_word)
                i = index - 1
        # reverse result
        i = len(result) - 1
        new_result = []
        while i >= 0:
            new_result.append(result[i])
            i -= 1
        return ' '.join(new_result).strip()

    def generate_overlapping_cases(self, sentence):
        cases = []
        if self.match_left_to_right(sentence) == self.match_right_to_left(sentence):
            cases.append(self.match_left_to_right(sentence))
            return cases
        else:
            cases.append(self.match_left_to_right(sentence))
            cases.append(self.match_right_to_left(sentence))
            return cases

    def generate_conjunction_cases(self, sentence):
        uni = uniStr()
        overlapping_cases = self.generate_overlapping_cases(sentence)
        conjunction_cases = []
        for i in range(len(overlapping_cases)):
            tokens = overlapping_cases[i].split(' ')
            for j in range(len(tokens)):
                syllables = tokens[j].split('_')
                if len(syllables) == 2:
                    s = overlapping_cases[i].replace(tokens[j], syllables[0] + ' ' + syllables[1])
                    conjunction_cases.append(s)
                if len(syllables) == 3:
                    if uni.to_lower(syllables[0] + '_' + syllables[1]) in self.vn_dict and syllables[2] in self.vn_dict:
                        s = overlapping_cases[i].replace(tokens[j], syllables[0] + '_' + syllables[1] + ' ' + syllables[2])
                        conjunction_cases.append(s)
                    if uni.to_lower(syllables[1] + '_' + syllables[2]) in self.vn_dict and syllables[0] in self.vn_dict:
                        s = overlapping_cases[i].replace(tokens[j], syllables[0] + ' ' + syllables[1] + '_' + syllables[2])
                        conjunction_cases.append(s)
        return conjunction_cases

    def generate_ambiguous_cases(self, sentence):
        ambiguous_cases = []
        overlapping_cases = self.generate_overlapping_cases(sentence)
        conjunction_cases = self.generate_conjunction_cases(sentence)
        for case in overlapping_cases:
            ambiguous_cases.append(case)
        for case in conjunction_cases:
            ambiguous_cases.append(case)
        return ambiguous_cases

    def choose_best_case(self, sentence):
        ambiguous_cases = self.generate_ambiguous_cases(sentence)
        max_probability = -999999.0
        best_case = ''
        for case in ambiguous_cases:
            probability = self.compute_probability_of_sentence(case)
            if probability > max_probability:
                max_probability = probability
                best_case = case
        return best_case

    def segment_sentence(self, sentence):
        tk = tokenizer()
        sentence = tk.pre_processing(sentence)
        return self.choose_best_case(sentence)

# testing
# s = u'bàn là công cụ học tập'
# s1 = u'Tốc độ truyền thông tin ngày càng tăng.'
# print segment_sentence(s)
# print segment_sentence(s1)
