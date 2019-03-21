#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'thai'

from sets import Set
import re
class uniStr:
    def __init__(self):
        self.upperChar = [
            u'A', u'Á', u'À', u'Ả', u'Ã', u'Ạ',
            u'Ă', u'Ắ', u'Ằ', u'Ẳ', u'Ẵ', u'Ặ',
            u'Â', u'Ấ', u'Ầ', u'Ẩ', u'Ẫ', u'Ậ',
            u'E', u'É', u'È', u'Ẻ', u'Ẽ', u'Ẹ',
            u'Ê', u'Ế', u'Ề', u'Ể', u'Ễ', u'Ệ',
            u'I', u'Í', u'Ì', u'Ỉ', u'Ĩ', u'Ị',
            u'Y', u'Ý', u'Ỳ', u'Ỷ', u'Ỹ', u'Ỵ',
            u'O', u'Ó', u'Ò', u'Ỏ', u'Õ', u'Ọ',
            u'Ô', u'Ố', u'Ồ', u'Ổ', u'Ỗ', u'Ộ',
            u'Ơ', u'Ớ', u'Ờ', u'Ở', u'Ỡ', u'Ợ',
            u'U', u'Ú', u'Ù', u'Ủ', u'Ũ', u'Ụ',
            u'Ư', u'Ứ', u'Ừ', u'Ử', u'Ữ', u'Ự',
            u'B', u'C', u'D', u'Đ', u'G', u'H', u'K', u'L', u'M', u'N', u'P', u'Q', u'R', u'S', u'T', u'V', u'X', u'F', u'J', u'W', u'Z'
        ]

        self.lowerChar = [
            u'a',u'á', u'à', u'ả', u'ã', u'ạ',
            u'ă', u'ắ', u'ằ', u'ẳ', u'ẵ', u'ặ',
            u'â', u'ấ', u'ầ', u'ẩ', u'ẫ', u'ậ',
            u'e', u'é', u'è', u'ẻ', u'ẽ', u'ẹ',
            u'ê', u'ế', u'ề', u'ể', u'ễ', u'ệ',
            u'i', u'í', u'ì', u'ỉ', u'ĩ', u'ị',
            u'y', u'ý', u'ỳ', u'ỷ', u'ỹ', u'ỵ',
            u'o', u'ó', u'ò', u'ỏ', u'õ', u'ọ',
            u'ô', u'ố', u'ồ', u'ổ', u'ỗ', u'ộ',
            u'ơ', u'ớ', u'ờ', u'ở', u'ỡ', u'ợ',
            u'u', u'ú', u'ù', u'ủ', u'ũ', u'ụ',
            u'ư', u'ứ', u'ừ', u'ử', u'ữ', u'ự',
            u'b', u'c', u'd', u'đ', u'g', u'h', u'k', u'l', u'm', u'n', u'p', u'q', u'r', u's', u't', u'v', u'x', u'f', u'j', u'w', u'z'
        ]
        return

    def is_uni_lower(self, inStr):
        count = 0
        for i in range(len(inStr)):
            if inStr[i] in Set(self.lowerChar):
                count+=1
        if count == len(inStr):
            return True
        else:
            return False

    def is_uni_upper(self, inStr):
        count = 0
        for i in range(len(inStr)):
            if inStr[i] in Set(self.upperChar):
                count+= 1
        if count == len(inStr):
            return True
        else:
            return False


    def to_lower(self, inStr):
        newStr = ''
        for i in range(len(inStr)):
            if inStr[i] in self.upperChar:
                newStr += self.lowerChar[self.upperChar.index(inStr[i])]
            else:
                newStr += inStr[i]
        return newStr

    def to_upper(self, inStr):
        newStr = ''
        for i in range(len(inStr)):
            if inStr[i] in self.lowerChar:
                newStr += self.upperChar[self.lowerChar.index(inStr[i])]
            else:
                newStr += inStr[i]
        return newStr

    def is_number(self, inStr):
        if re.search('\d+', inStr) or re.search('\d+\.\d+', inStr) or re.search('\d+\,\d+', inStr):
            return True
        return False

# testing
#uni = uniStr()
# s = u'TÔI'
# print uni.is_uni_lower(s)
# print uni.is_uni_upper(s)
# print uni.is_number(u'123.0')
#print uni.to_lower(u'J ')


