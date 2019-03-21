#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'thaidang'

from load_model import *
from ws.uni_str import *
import math

class compute:

    def __init__(self, trigram_file, bigram_file, unigram_file, emission_file, lexicon_file, tagset_file):
        # load model
        print 'loading trigram of tags'
        self.trigram = load_trigram(trigram_file)
        print 'loading bigram of tags'
        self.bigram = load_bigram(bigram_file)
        print 'loading unigram of tags'
        self.unigram, self.tag_vocab, self.total = load_unigram(unigram_file)
        print 'loading emission'
        self.emis, self.N = load_emission(emission_file)
        print 'loading lexicons'
        self.lexicon = load_lexicon(lexicon_file)
        print 'loading tags set'
        self.tag_set = load_tagSet(tagset_file)
        self.oo = -9999999.0
        self.uni = uniStr()
        return

    def transition(self, tag, tag1, tag2):
        count = self.trigram.get(tag2 + u" " + tag1 + u" " + tag)
        if count is None:
            t2t1t_count = 0
        else:
            t2t1t_count = count
        count = self.bigram.get(tag2 + " " + tag1)
        if count is None:
            t2t1_count = 0
        else:
            t2t1_count = count
        count = self.bigram.get(tag1 + " " + tag)
        if count is None:
            t1t_count = 0
        else:
            t1t_count = count
        t1_count = self.unigram.get(tag1)
        if t1_count is None:
            t1_count = 0
        if self.unigram.get(tag) is None:
            Pt = (0 + 0.1) * 1.0/(self.total + 0.1*self.tag_vocab)
        else:
            Pt = (self.unigram.get(tag) + 0.1)*1.0/(self.total + 0.1*self.tag_vocab)
        return math.log10(self.interpolation_transition(t2t1t_count, t2t1_count, t1t_count, t1_count, Pt))

    def emission(self, word, tag):
        count = self.emis.get(word + " " + tag)
        if count is None:
            numerator = 0
        else:
            numerator = count
        count = self.unigram.get(tag)
        if count is None:
            denominator = 0
        else:
            denominator = count
        return math.log10(self.interpolation_emission(numerator, denominator, self.N))

    # lamda = 0.1
    def laplace(self, numerator, denominator, vocab):
        return (numerator+0.1)*1.0/(denominator+vocab*0.1)

    # lamda = 0.3
    def interpolation_emission(self, numerator, denominator, N):
        return 0.3*self.laplace(numerator, denominator, 35388) + (1-0.3)*(1.0/N)
    # 0.4 , 0.2, 0.4
    def interpolation_transition(self, t2t1t_count, t2t1_count, t1t_count, t1_count, Pt):
        Ptt1t2 = self.laplace(t2t1t_count, t2t1_count, self.tag_vocab)
        Ptt1 = self.laplace(t1t_count, t1_count, self.tag_vocab)
        return 0.4*Ptt1t2 + 0.2*Ptt1 + 0.4*Pt

    #================== viterbi algorithm =================#

    def index_sentence(self, sentence):
        words = sentence.split(' ')
        word_id = {}
        i = 1
        for word in words:
            word_id[i] = word
            i+=1
        return word_id

    def get_possible_tag(self, word):
        tags_str = self.lexicon.get(self.uni.to_lower(word))
        if tags_str is None:
            return self.tag_set
        else:
            possible_tag_list = tags_str.split(' ')
        return possible_tag_list

    def viterbi(self, sentence):
        word_id = self.index_sentence(sentence)
        sentence_len = len(word_id.keys())

        best_score = {}
        back_trace = {}
        # initial step
        best_score[str(0) + "<s>"] = 0
        # compute best score for first word
        tag_list = self.get_possible_tag(word_id.get(1))
        for i in range(len(tag_list)):
            p = self.transition(tag_list[i], "<s>", "<s>") + self.emission(word_id.get(1), tag_list[i])
            best_score[str(1)+tag_list[i]] = p
            back_trace[str(1)+"\\"+tag_list[i]] = str(0)+"\\"+"<s>"
        # compute for sencond word
        if sentence_len >= 2:
            taglist_2 = self.get_possible_tag(word_id.get(2))
            taglist_1 = self.get_possible_tag(word_id.get(1))
            for i in range(len(taglist_2)):
                max = self.oo
                for j in range(len(taglist_1)):
                    p = best_score.get(str(1) + taglist_1[j]) + self.transition(taglist_2[i], taglist_1[j], "<s>") + self.emission(word_id.get(2), taglist_2[i])
                    if p > max:
                        max = p
                        index = j
                best_score[str(2) + taglist_2[i]] = max
                back_trace[str(2)+"\\"+taglist_2[i]] = str(1) + "\\" + taglist_1[index]
        # start with third word
        for i in range(3, len(word_id.keys())+1):
            taglist_i = self.get_possible_tag(word_id.get(i))
            taglist_i1 = self.get_possible_tag(word_id.get(i-1))
            for j in range(len(taglist_i)):
                max = self.oo
                for k in range(len(taglist_i1)):
                    trace = back_trace.get(str(i-1)+"\\"+taglist_i1[k])
                    pos = trace.index("\\")
                    tag_i2 = trace[pos+1:]
                    p = best_score.get(str(i-1) + taglist_i1[k]) + self.transition(taglist_i[j], taglist_i1[k], tag_i2) + self.emission(word_id.get(i), taglist_i[j])
                    if p > max:
                        max = p
                        index = k
                best_score[str(i)+taglist_i[j]] = max
                back_trace[str(i)+"\\"+taglist_i[j]] = str(i-1)+"\\"+taglist_i1[index]
        # end sentence
        taglist = self.get_possible_tag(word_id.get(len(word_id.keys())))
        max = self.oo
        for i in range(len(taglist)):
            trace = back_trace.get(str(sentence_len) + "\\" + taglist[i])
            pos = trace.index("\\")
            tag = trace[pos+1:]
            p = best_score.get(str(sentence_len)+taglist[i]) + self.transition("<e>", taglist[i], tag)
            if p > max:
                max = p
                index = i
        best_score[str(sentence_len+1), "<e>"] = max
        # backward step
        result = []
        result.append(word_id.get(sentence_len)+"\\"+taglist[index])
        s = back_trace.get(str(sentence_len)+"\\"+taglist[index])
        while s!= "0\<s>":
            pos = s.index("\\")
            result.append(word_id.get(int(s[0:pos])) + "\\" + s[pos+1:])
            s = back_trace.get(s)
        return result