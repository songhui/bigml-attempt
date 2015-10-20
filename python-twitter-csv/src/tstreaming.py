#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import tquery
import csvwriter


class CsvWriter:
    def __init__(self, filename, headers):
        self.filename = filename
        self.headers = headers
        self.add_line(self.headers)
    
    def add_line(self, line):
        f = open(self.filename, 'a')
        l = ', '.join([str(x) for x in line])
        print l
        f.write(l)
        f.write('\n')
        f.close()

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def __init__(self, writer):
        self.writer = writer

    def on_data(self, data):
        print data
        #print type(data)
        d = json.loads(data)
        line = csvwriter.process_twitter_message(d)
        print line
        self.writer.add_line(line)
        return True

    def on_error(self, status):
        print status



if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    writer = CsvWriter('output.csv', csvwriter.header)
    l = StdOutListener(writer)
    auth = OAuthHandler(tquery.consumer_key, tquery.consumer_secret)
    auth.set_access_token(tquery.access_token, tquery.access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    tquery.query(stream)
    #stream.filter(track=['python', 'javascript', 'ruby'])
