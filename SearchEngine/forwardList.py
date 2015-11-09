# -*- coding: utf-8 -*-
import jieba
import lexicon

def word_cut(text):
    seg_text = jieba.tokenize(text, mode = 'search')
    ret = list(seg_text)
    return ret

class forwardIndexTableItem:
    def __init__(self, docID_, wordID_, word_hits_):
        self.docID = docID_
        self.docID = docID_
        self.wordID = wordID_
        self.word_hits = word_hits_[:]
    
    wordID = 0
    docID = 0
    word_hits = []

class forwardIndexTable:
    forward_index_table = []
    
    def add_item(self, docID, title):
        words = word_cut(title)
        word_reduce = {}
        
        for item in words:
            if lexicon.getWordID(item[0]) in word_reduce:
                word_reduce[lexicon.getWordID(item[0])].append(item[1:])
            else:
                word_reduce[lexicon.getWordID(item[0])] = [item[1:]]
        
        for wordID in word_reduce:   
            self.forward_index_table.append(forwardIndexTableItem(docID, wordID, word_reduce[wordID]))
    
    def size(self):
        return len(self.forward_index_table)    
    
    def sortByWordID(self):
        print "sort"
        self.forward_index_table = sorted(self.forward_index_table, cmp=lambda x,y:cmp(x.wordID, y.wordID))
        print "end"