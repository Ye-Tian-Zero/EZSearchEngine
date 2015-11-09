# -*- coding:utf-8 -*-  
import backwardList as blist
import forwardList as flist
import lexicon
import sqlite3



DB_path = './Database/PAGES.db'
index_DB_path = './/Index.db'


read_step = 200000
conn_ut = sqlite3.connect(DB_path)

cur = conn_ut.cursor()

cur.execute("SELECT * from url_title")

data = cur.fetchmany(read_step)

print len(data)

while len(data) != 0:
    
    fwlist = flist.forwardIndexTable()
    for ut in data:
        fwlist.add_item(ut[0], unicode(ut[1]).lower().capitalize())
    
    print 'forward list ok'
    bwlist = blist.backwardList(fwlist)
    print 'bwlist ok'
    bwlist.buildBackwardListDB(index_DB_path)
    
    data = cur.fetchmany(read_step)
    
print 'bwlist done'
print 'saving lexicon'

lexicon.buildLexicon(index_DB_path)

print 'lexicon saved'
  



'''
fwlist.add_item(0, u"我爱吃米饭")
fwlist.add_item(1, u"3D打印机真好玩, 好喜欢玩3D打印机")
fwlist.add_item(2, u"我今天没有理发哈哈哈")
fwlist.add_item(3, u"我爱吃米饭吗？")
'''


'''for item in fwlist.forward_index_table:
    print item.docID, lexicon.getWord(item.wordID), item.word_hits'''



''''for item,val in bwlist.backward_index_table.iteritems():
    print lexicon.getWord(item),":"
    for sub_item in val:
        print '    docID: ', sub_item[0], '    hits: ', sub_item[1]   
a= 10'''
    