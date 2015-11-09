import sqlite3

class __lexicon:
    Dic = {}
    cur_wordID = 0
    inited = False

def inited():
    return __lexicon.inited

def getWordID(word):
    if __lexicon.inited == False:
        if word in __lexicon.Dic:
            return __lexicon.Dic[word]
        else:
            __lexicon.cur_wordID += 1
            __lexicon.Dic[word] = __lexicon.cur_wordID
            return __lexicon.cur_wordID
    else:
        if word in __lexicon.Dic:
            return __lexicon.Dic[word]
        else:        
            return -1
        
def getWord(ID):
    for key in __lexicon.Dic:
        if __lexicon.Dic[key] == ID:
            return key
    return ''

def buildLexicon(path):
    conn = sqlite3.connect(path)
    
    cur = conn.cursor()
    
    cur.execute("CREATE TABLE IF NOT EXISTS lexicon (word text primary key, wordID int)")
    
    for word, wordID in __lexicon.Dic.iteritems():
        cur.execute("INSERT INTO lexicon VALUES(?, ?)", (word, wordID))
        
    conn.commit()
    conn.close()
        
def loadLexicon(path):
    
    __lexicon.Dic={}
    
    conn = sqlite3.connect(path)
        
    #conn.text_factory=lambda x: unicode(x, 'gbk', 'ignore') 
    
    cur = conn.cursor()
    
    cur.execute('SELECT word, wordID FROM lexicon')

    word_list = cur.fetchall()

    for word_id_pair in word_list:
        __lexicon.Dic[word_id_pair[0]] = word_id_pair[1]
    
    __lexicon.cur_wordID = len(__lexicon.Dic)
    
    __lexicon.inited = True