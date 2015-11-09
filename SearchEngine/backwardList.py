# -*- coding:utf-8 -*-  
import sqlite3
import lexicon

class backwardList:
    def __init__(self, fw_list):
        fw_list.sortByWordID()
        for item in fw_list.forward_index_table:
            if item.wordID not in self.backward_index_table:
                self.backward_index_table[item.wordID] = [[item.docID, item.word_hits]]
            else:
                self.backward_index_table[item.wordID].append([item.docID, item.word_hits])
                
    def buildBackwardListDB(self, path):
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        
        cur.execute("CREATE TABLE IF NOT EXISTS backwardTable (wordID INT PRIMARY KEY, off_start INT, off_end INT)")
        cur.execute("CREATE TABLE IF NOT EXISTS docIDTable (docID_index INTEGER PRIMARY KEY AUTOINCREMENT, docID INT, hits TEXT)")
        
        off_start = 1
        off_end = 1
        
        for item, val in self.backward_index_table.iteritems():
            for sub_item in val:
                hits = ""
                for offset_item in sub_item[1]:
                    hits += ('%d' % offset_item[0] + ' ' + '%d' % offset_item[1] + ' ') 
                cur.execute("INSERT INTO docIDTable (docID, hits) VALUES(?, ?)", (sub_item[0], hits))
                off_end += 1
            cur.execute("INSERT INTO backwardTable VALUES(?, ?, ?)", (item, off_start, off_end))
            
            off_start = off_end
            
        conn.commit()
        conn.close()
        
    backward_index_table = {}
