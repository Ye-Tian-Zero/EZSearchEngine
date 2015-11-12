import jieba
import sqlite3
import lexicon

class searchEngine:
    cursor_back_table = sqlite3.Cursor
    conn_back_table = sqlite3.Connection
    cursor_pages = sqlite3.Cursor
    conn_pages = sqlite3.Connection
    
    path = ''
    def __init__(self, path_ = './/Index.db'):
        
        self.path = path_
        self.conn_back_table = sqlite3.connect(path_)
        self.cursor_back_table = self.conn_back_table.cursor()
        self.conn_pages = sqlite3.connect("./Database/PAGES.db")
        self.cursor_pages = self.conn_pages.cursor()
    
    def getDocSet(self, word):
        if lexicon.inited() == False:
            lexicon.loadLexicon(self.path)
    
        wordID = lexicon.getWordID(word)
        
        if wordID < 0:
            return []
        else:
            self.cursor_back_table.execute('SELECT * FROM backwardTable where wordID = (?)', (wordID,))
            docID_range = self.cursor_back_table.fetchone()
            self.cursor_back_table.execute('select * from docIDTable where docID_index between (?) and (?)', (docID_range[1], docID_range[2] - 1))
            ret = self.cursor_back_table.fetchall() 
            return ret       
            #print docID_range
            
        
    

    def search(self, query):
        seg_text = jieba.cut_for_search(query)
        query_list = list(seg_text)
        
        query_list = [i for i in query_list if i != ' ']
        
        #print query_list
        
        title_hits_cnt = {}
        for item in query_list:
            doc_set = self.getDocSet(item)
            for doc_item in doc_set:
                #if doc_item[1] == 277:
                #  print doc_item[1], item, len(query_list)
                if doc_item[1] in title_hits_cnt:
                    title_hits_cnt[doc_item[1]] += 1
                else:
                    title_hits_cnt[doc_item[1]] = 1
        
        tmp = sorted(title_hits_cnt.items(), key=lambda x:x[1])
        
        for i in range(1,10):
            self.cursor_pages.execute('SELECT * FROM url_title where id = (?)', (tmp[-i][0],))
            url_title = self.cursor_pages.fetchone()
            print url_title[1]
            print url_title[2]
            print 
               
if __name__ == '__main__':
    se = searchEngine()
    while(True):
        query = raw_input('please: ')
        se.search(query)
    
    
    se.search()