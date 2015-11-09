import jieba
import sqlite3
import lexicon

class searchEngine:
    cursor = sqlite3.Cursor
    conn = sqlite3.Connection
    path = ''
    def __init__(self, path_ = './/Index.db'):
        
        self.path = path_
        self.conn = sqlite3.connect(path_)
        self.cursor = self.conn.cursor()
    
    def getDocSet(self, word):
        if lexicon.inited() == False:
            lexicon.loadLexicon(self.path)
    
        wordID = lexicon.getWordID(word)
        
        if wordID < 0:
            return []
        else:
            self.cursor.execute('SELECT * FROM backwardTable where wordID = (?)', (wordID,))
            docID_range = self.cursor.fetchall()
            print docID_range
        #从这里开始写
        

    def search(self, query):
        seg_text = jieba.cut_for_search(query)
        query_list = list(seg_text)
        
        if ' ' in query_list:
            query_list.remove(' ')
            
        for item in query_list:
            self.getDocSet(item)
       
if __name__ == '__main__':
    se = searchEngine()
    while(True):
        query = raw_input('please: ')
        se.search(query)
    
    
    se.search()