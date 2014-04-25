import tweepy, json, time

class CountException(Exception):
  pass

matt_consumer_key='QIpWk7AGgwtNc9v04KbZg'
matt_consumer_secret='f2voSvlOHKwGO240dOGTCNs3pFDbveX4GL1bKq2Zek'
matt_access_token_key='336838314-c70cW7XaN3DwDdHvGU5Q5Y5JFFSJR4tvNakBPrq3'
matt_access_token_secret='Uk0qjVIpJBzxkHQwpR4bBjFO2GtQWj4an9pNKG8Ps5zkZ'

auth = tweepy.OAuthHandler(matt_consumer_key, matt_consumer_secret)
auth.set_access_token(matt_access_token_key, matt_access_token_secret)
api = tweepy.API(auth)

TWEETS_PER_FILE = 2000
DELAY = 60
jsonTweets = dict()
textTweets = list()


################output directories for collected tweets################
# must end with a /
outDir_full = 'TwitterData/Chicago/full_tweet/'
outDir_text = 'TwitterData/Chicago/text_only/'

class CustonStreamListener(tweepy.StreamListener):
  def __init__(self, api=None):
    self.api = api


  def on_data(self, tweet):
    try:
      print len(jsonTweets)
      tweet = unicode(tweet)
      j = json.loads(tweet)

      try:
        jsonText = j[u'text']
      except:
        jsonText = None
      try:
        jsonCreatedAt = j[u'created_at']
      except:
        jsonCreatedAt = None
      try:
        jsonCoordinates = j[u'coordinates'][u'coordinates']
      except:
        jsonCoordinates = None

      jsonTweets[j[u'id']] = {'created_at' : jsonCreatedAt, 'text' : jsonText, 'coordinates' : jsonCoordinates}
      textTweets.append(jsonText)
    except:
      print 'Error: skipping tweet'

    if len(jsonTweets) >= TWEETS_PER_FILE:
      raise CountException

  def on_error(self, status_code):
    return True

  def on_timeout(self):
    return True


def main():
  while True:
    listen = CustonStreamListener(api)
    stream = tweepy.Stream(auth, listen)

    global jsonTweets
    global textTweets
    timestr = time.strftime('%Y%m%d-%H%M%S')
    outFile = open(outDir_full + timestr + '.txt', 'w+')
    textOutfile = open(outDir_text + timestr + '.txt', 'w+')

    noError = True
    while noError:
      try:
        print "Streaming started..."
        stream.filter(locations=[-87.94011, 41.64454, -87.52413,42.02303]) # chicago
      except CountException:
        print 'Saved results to file'
        outFile.write(json.dumps(jsonTweets, indent=2))
        outFile.write('\n')
        outFile.close()
        for text in textTweets:
          textOutfile.write( (text + '\n').encode('utf-8') )
        textOutfile.close()

        # reset
        time.sleep(DELAY / 3)
        jsonTweets = dict()
        textTweets = list()
        timestr = time.strftime('%Y%m%d-%H%M%S')
        outFile = open(outDir_full + timestr + '.txt', 'w+')
        textOutfile = open(outDir_text + timestr + '.txt', 'w+')

      except:
        print 'error: '
        print 'Saved results to file'
        outFile.write(json.dumps(jsonTweets, indent=2))
        outFile.write('\n')
        outFile.close()
        for text in textTweets:
          textOutfile.write( (text + '\n').encode('utf-8') )
        textOutfile.close()
        noError = False
        jsonTweets = dict()
        textTweets = list()
        stream.disconnect()
        time.sleep(DELAY * 10)  # wait 10 mins before restarting


if __name__ == '__main__':
    main()
