from datetime import datetime,timedelta
from pymongo import MongoClient,errors

class MogoQueue():
    OUTSTANDING = 1 ##初始状态
    PROCESSING = 2  ##正在下载状态
    COMPLETE = 3  ##下载完成状态

    def __init__(self,db,collection,timeout=300):#初始mongodb链接
        self.client = MongoClient()
        self.Client = self.client[db]
        self.db = self.Client[collection]
        self.timeout = timeout

    def __bool__(self):
        '''该函数的意思是，如果下面的表达为真，则整个类为真 $ne的意思是不匹配'''
        record = self.db.find_one(
            {'status':{'$ne':self.COMPLETE}}
        )
        return  True if record else False

    def push(self,url,title):#这个函数用来添加新的URL进队列
        try:
            self.db.insert({'_id':url,'status':self.OUTSTANDING,'主题':title})
            print(url,'插入队列成功')
        except errors.DuplicateKeyError as e:#报错则代表已经存在于队列之中了
            print(url,'已经存在于队列之中了')
            pass

    def push_imgurl(self,title,url):
        try:
            self.db.insert({'_id':title,'status':self.OUTSTANDING,'url':url})
            print('图片地址插入成功')
        except errors.DuplicateKeyError as e:
            print('地址已经存在了')
            pass

    def pop(self):
        '''该函数会查询队列中所有状态为OUTSTANDING的值，更改状态'''
        record = self.db.find_and_modify(
            query={'status':self.OUTSTANDING}
            update={'$set':{'status':self.PROCESSING,'timestamp':datetime.now()}}
        )
        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError


    def pop_title(self,url):
        record = self.db.find_one({'_id':url})
        return record['主题']

    def peek(self):
        '''这个函数是取出状态为OUTSTANDING的文档并返回_id(URL)'''
        record = self.db.find_one({'status':self.OUTSTANDING})
        if record:
            return record['_id']

    def complete(self,url):
        '''这个函数是更新已完成的URL完成'''
        self.db.update({'_id':url},{'$set':{'status':self.COMPLETE}})

    def repair(self):
        '''该函数是重置状态 $lt是比较的意思'''
        record = self.db.find_and_modify(
            query={
                'timestamp':{'$lt':datetime,now()-timedelta(seconds=self.timeout)},
                'status':{'$ne':self.COMPLETE}
            },
            update={'$set':{'status':self.OUTSTANDING}}
        )
        if record:
            print('重置URL状态',record['_id'])

    def clear(self):
        '''该函数只有第一次才调用，后续不要调用，因为这是删库'''
        self.db.drop()










