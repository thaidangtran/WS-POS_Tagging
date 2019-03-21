#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'thaidang'

from compute import *
from ws.uni_str import *
from count_ngram.io import *
import codecs
import timeit
from sets import Set
import glob
import sys


class POSTagger:

    def __init__(self, trigram_file, bigram_file, unigram_file, emission_file, lexicon_file, tagset_file):
        self.comp = compute(trigram_file, bigram_file, unigram_file, emission_file, lexicon_file, tagset_file)
        # define
        self.punctuation = Set(['.\CH', '!\CH', '?\CH', '"\CH', '...\CH', ':\CH', '”\CH', '“\CH'])
        self.currency = Set([u'USD', u'₫', u'$', u'VND', u'GBD', u'EUR', u'JPY', u'AUD', u'¥'])
        self.length_unit = Set(['mm', 'cm', 'dm','m','km', 'inch'])
        self.weight_unit = Set(['kg', 'g', 'gr',u'lạng', u'tấn', u'tạ', u'yến'])
        self.area_unit = Set([u"m²", "dm²", "cm²"])
        self.temprature = Set([u"ºC"])
        self.commmon_vn_lastname = Set([
            u"Nguyễn", u"Trần", u"Lê", u"Phạm", u"Hoàng", u"Huỳnh", u"Phan", u"Vũ", u"Võ", u"Đặng", u"Bùi", u"Đỗ", u"Hồ",
            u"Ngô", u"Dương", u"Lý", u"Chu", u"Đàm", u"Nông", u"Trương", u"Đồng", u"Đới", u"Quách"
        ])
        self.vn_organization_prefix = Set([
            u"Tỉnh", u"Huyện", u"Xã", u"Phường", u"Bộ", u"Cục", u"Ban", u"Ngành", u"Trường", u"Hội",
            u"Tp", u"Uỷ_ban", u"Tòa_án", u"Sở", u"Tổ_chức",u"Khu", u"Viện"
        ])
        self.sign_list = Set([
            u"[", u"]", u",", u".", u"/", u";", u"\'", u"-", u"=", u"!", u"@", u"$", u"#", u"%",
            u"^", u"&", u"*", u"(", u")", u"\\", u"\"", u":", u"<", u">", u"?", u"{", u"}", u"“",
            u"”", u"…", u"..."
        ])
        return
    
    def NER(self, input_list):
        uni = uniStr()
        for i in range(len(input_list)):
            input_list[i] = input_list[i] + u""
            pos = input_list[i].index("\\")
            token_list = input_list[i][0:pos].split("_")
            l = len(token_list)
            # recognize Name Entity that contains 2 syllables or more
            if len(token_list) >= 2:
                #if token_list[0][0:1].isupper() and token_list[l-1][0:1].isupper():
                if uni.is_uni_upper(token_list[0][0:1]) and uni.is_uni_upper(token_list[l-1][0:1]):
                    input_list[i] = input_list[i][:pos] + "\Np"
            if i == 0 and token_list[i] in self.commmon_vn_lastname:
                input_list[i] = input_list[i][:pos] + "\Np"
            # recognize organization name
            if i == 0 and token_list[i] in self.vn_organization_prefix:
                input_list[i] = input_list[i][:pos] + "\Np"
            # recognize NE contains 1 syllable. It contains recognize currency,length unit, weight unit, private name.
            if len(token_list) == 1:
                if (input_list[i][:pos]+u"") in self.currency:
                    input_list[i] = input_list[i][:pos] + "\Nu"
                elif i-1 >= 0 and input_list[i-1][0:1].isdigit():
                    if (input_list[i][:pos]+"u") in self.length_unit or (input_list[i][:pos]+"u") in self.weight_unit:
                        input_list[i] = input_list[i][:pos] + "\Nu"
                else:
                    if i-1 >= 0 and input_list[i-1] not in self.punctuation:
                        if input_list[i][0:1].isupper() and not input_list[i][1:2].isupper():
                            input_list[i] = input_list[i][:pos] + "\Np"
            # tag number
            if input_list[i][0:1].isdigit():
                input_list[i] = input_list[i][:pos] + '\M'
            # tag sign
            if input_list[i][:pos] in self.sign_list:
                input_list[i] = input_list[i][:pos] + '\CH'
            if re.search('\d+', input_list[i]) and len(re.search('\d+', input_list[i]).group()) < len(input_list[i][:pos]):
                input_list[i] = input_list[i][:pos] + '\Ny'


        return input_list

    def tagging_sentence(self, sentence):
        tagged = self.comp.viterbi(sentence)
        result = []
        # reorder the position of word in result
        for i in range(len(tagged)):
            result.append(tagged.pop())
            result = self.NER(result)
        return ' '.join(result).strip()
