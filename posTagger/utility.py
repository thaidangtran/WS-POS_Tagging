#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'thaidang'

class Utility:

    def __init__(self):
        return

    def foreignTest(self, word):
        word = word.lower()
        if "w" in word:
            return True
        if "f" in word:
            return True
        if "j" in word:
            return True
        if "z" in word and word != "bazan":
            return True
        if "ar" in word:
            return True
        if "av" in word:
            return True
        if "as" in word:
            return True
        if "ag" in word:
            return True
        if "br" in word:
            return True
        if "ce" in word:
            return True
        if "ci" in word:
            return True
        if "ck" in word:
            return True
        if "ec" in word:
            return True
        if "er" in word:
            return True
        if "ev" in word:
            return True
        if "es" in word:
            return True
        if "ea" in word:
            return True
        if "et" in word:
            return True
        if "el" in word:
            return True
        if "ey" in word:
            return True
        if "gl" in word:
            return True
        if "ic" in word:
            return True
        if "ir" in word:
            return True
        if "is" in word:
            return True
        if "iv" in word:
            return True
        if "id" in word:
            return True
        if "il" in word:
            return True
        if "ka" in word:
            return True
        if "nn" in word:
            return True
        if "nd" in word:
            return True
        if "nc" in word:
            return True
        if "pp" in word:
            return True
        if "pl" in word:
            return True
        if "ov" in word:
            return True
        if "yl" in word:
            return True
        if "st" in word:
            return True
        if "ub" in word:
            return True
        if "ur" in word:
            return True
        if "us" in word:
            return True
        if "uv" in word:
            return True
        if "ud" in word:
            return True
        if "ion" in word:
            return True
        return False

#utility = Utility()
#print utility.foreignTest("hello")