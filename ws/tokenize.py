#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'thai'
from sets import Set
from uni_str import *
import re

class tokenizer:
    def __init__(self):
        return

    def split_sentence(self, paragraph):
        sentence_list = []
        sentences = paragraph.split(u'.')
        for sentence in sentences:
            ques_sents = sentence.split(u'?')
            for quest_sent in ques_sents:
                sentence_list.append(quest_sent)
            emot_sents = sentence.split(u'!')
            for emot_sent in emot_sents:
                sentence_list.append(emot_sent)
        return sentence_list

    def split_sign(self, s):
        specialReg = [
            'http://.+',
            '\d+\.\d+\.\d+',
            '\d+\,\d+\,\d+',
            '\d+\.\d+',
            '\d+\,\d+',
            '\d+\-\d+\-\d+',
            '\d+\-\d+',
            '\d+\/\d+\/\d+',
            '\d+\/\d+',
            '.+\.(com|vn|org|net)',
            '.+\.(com|vn|org|net)\.(com|vn|org|net)',
            # # emoticon
            # ':)', u':(', u':D', ':|', '=)', '=\)+'
        ]

        sign_list = [
            u"[", u"]", u",", u".", u"/", u";", u"\'", u"-", u"=", u"!", u"@", u"$", u"#", u"%",
            u"^", u"&", u"*", u"(", u")", u"\\", u"\"", u":", u"<", u">", u"?", u"{", u"}", u"“",
            u"”", u"…", u"..."
        ]
        for reg in specialReg:
            match = re.search(reg, s)
            if match is not None:
                s = s.replace(match.group(), ' ' + match.group() + ' ')
                return s
        if s in Set(sign_list):
            s = s
        for sign in sign_list:
            if sign in s:
              s = s.replace(sign, ' ' + sign + ' ')
        s = re.sub('\s+', ' ', s)
        return s.strip()

    def tokenize(self, tokens):
        tokenized_list = []
        for token in tokens:
            new_token = self.split_sign(token)
            __list = new_token.split(' ')
            for item in __list:
                tokenized_list.append(item)
        return tokenized_list

    def NER(self, tokens):
        common_vn_lastname = Set([
            u'Nguyễn', u'Trần', u'Lê', u'Phạm', u'Hoàng', u'Huỳnh', u'Phan', u'Vũ', u'Võ', u'Đặng', u'Bùi', u'Đỗ', u'Hồ', u'Ngô', u'Dương', u'Lý', u'Chu', u'Đàm', u'Nông', u'Trương', u'Quách',
            u'NGUYỄN', u'TRẦN', u'LÊ', u'PHẠM', u'HOÀNG', u'HUỲNH', u'PHAN', u'VŨ', u'VÕ', u'ĐẶNG', u'BÙI', u'ĐỖ', u'HỒ', u'NGÔ', u'DƯƠNG', u'LÝ', u'CHU', u'ĐÀM', u'NÔNG', u'TRƯƠNG', u'QUÁCH'
        ])
        common_organization_prefix = Set([
            u'Tỉnh', u'Huyện', u'Xã', u'Phường', u'Bộ', u'Cục', u'Ban', u'Ngành', u'Trường', u'Hội', u'Tp',
            u'TỈNH', u'HUYỆN', u'XÃ', u'PHƯỜNG', u'BỘ', u'CỤC', u'BAN', u'NGHÀNH', u'TRƯỜNG', u'HỘI', u'TP'
        ])
        uni = uniStr()
        result = []
        l = len(tokens)
        i = 0
        while i < l:
            if i == 0 and tokens[i] in common_vn_lastname:
                name = tokens[i]
                i += 1
                while uni.is_uni_upper(tokens[i][0:1]):
                    name += u'_' + tokens[i]
                    i += 1
                result.append(name)
            else:
                if tokens[i] in common_organization_prefix:
                    result.append(tokens[i])
                    i += 1
                elif i > 0 and uni.is_uni_upper(tokens[i][0:1]):
                    name = tokens[i]
                    i += 1
                    while i < l:
                        if uni.is_uni_upper(tokens[i][0:1]):
                            name += '_' + tokens[i]
                        else:
                            break
                        i += 1
                    result.append(name)
                else:
                    result.append(tokens[i])
                    i+=1

        return result

    def recognize_pattern(self, tokens):
        uni = uniStr()
        #tokens = sentence.split(' ')
        result = []
        suffix = Set([
            u'chục', u'trăm', u'nghìn', u'ngàn', u'vạn', u'triệu', u'tỉ', u'k', u'K'
        ])
        l = len(tokens)
        i = 0
        while i < l:
            if uni.is_number(tokens[i]):
                number = tokens[i]
                if i+1 < l and tokens[i+1] in suffix:
                    number += '_' + tokens[i+1]
                    result.append(number)
                    if i+2 < l:
                        i = i + 2
                    else:
                        break
                elif i+4 < l and tokens[i+1] == u':' and uni.is_number(tokens[i+2]) and tokens[i+3] == u':' and uni.is_number(tokens[i+4]):
                    number += '_' + tokens[i+1] + '_' + tokens[i+2] + '_' + tokens[i+3] + '_' + tokens[i+4]
                    result.append(number)
                    if i+5 < l:
                        i = i+5
                    else:
                        break
                elif i+4 < l and tokens[i+1] == u'/' and uni.is_number(tokens[i+2]) and tokens[i+3] == u'/' and uni.is_number(tokens[i+4]):
                    number += '_' + tokens[i+1] + '_' + tokens[i+2] + '_' + tokens[i+3] + '_' + tokens[i+4]
                    result.append(number)
                    if i+5 < l:
                        i = i+5
                    else:
                        break
                elif i+4 < l and tokens[i+1] == u'-' and uni.is_number(tokens[i+2]) and tokens[i+3] == u'-' and uni.is_number(tokens[i+4]):
                    number += '_' + tokens[i+1] + '_' + tokens[i+2] + '_' + tokens[i+3] + '_' + tokens[i+4]
                    result.append(number)
                    if i+5 < l:
                        i = i+5
                    else:
                        break
                else:
                    result.append(number)
                    i += 1
            else:
                result.append(tokens[i])
                i += 1
        return result

    def pre_processing(self, sentence):
        tokens = sentence.split(' ')
        tokens = self.tokenize(tokens)
        tokens = self.NER(tokens)
        tokens = self.recognize_pattern(tokens)
        s = u''
        for i in range(len(tokens)):
            s += tokens[i] + ' '
        s = re.sub('\s+', ' ', s)
        return s.strip()
