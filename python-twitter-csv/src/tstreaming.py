#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import tquery
import script
from pymongo import MongoClient

class CsvWriter:
    def __init__(self, filename, headers):
        self.filename = filename
        self.headers = headers
        f = open(self.filename, 'w')
        f.write('')
        f.close()
        self.add_line(self.headers)

    def add_line(self, line):
        self.append(line)

    def append(self, line):
        f = open(self.filename, 'a')
        l = ', '.join([str(x) for x in line])
        print l
        f.write(l)
        f.write('\n')
        f.close()

class MongoWriter:
    def __init__(self, host, port, db, collection):
        client = MongoClient(host, port)
        db = client[db]
        self.collection = db[collection]
        
    def append(self, item):
        self.collection.insert_one(item)
        print 'Mongo count: %d' % self.collection.count()

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def __init__(self, writers):
        self.writers = writers

    def on_data(self, data):
        #print data
        #print type(data)
        d = json.loads(data)
        print d['text'].encode('utf-8')
        line = script.process(d, self.writers)
        return True

    def on_error(self, status):
        print status

def resolve_writer(spec):
    if spec['type'] == 'file/csv':
      return CsvWriter('output.csv', spec['header'])
    if spec['type'] == 'mongo':
      return MongoWriter(spec['host'], int(spec['port']), spec['db'], spec['collection'])


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    writers = dict()
    for w in script.writers:
        spec = script.writers[w]
        writers[w]= resolve_writer(spec)

    l = StdOutListener(writers)
    auth = OAuthHandler(tquery.consumer_key, tquery.consumer_secret)
    auth.set_access_token(tquery.access_token, tquery.access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    tquery.query(stream)
    #stream.filter(track=['python', 'javascript', 'ruby'])
