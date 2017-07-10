from secrets import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_SECRET

import logging, os, sys
import jinja2
import webapp2

sys.path.append(os.path.join(os.path.dirname(__file__)+"/lib/python2.7/site-packages"))
logging.info(sys.path)

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
    
import tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        logging.info("In MainHandler")
        vals={}
        vals['page_title']="wishing well"
        template = JINJA_ENVIRONMENT.get_template('homepage.html')
        self.response.write(template.render(vals))
   
def apiSearch(count=30,
              lang="en",
              q="-filter:retweets -filter:links -filter:replies",
              btn=""):
    """
    returns a list of tweets extracted from the JSON of each tweet matching
    the search query
    """
    q = '"%s" %s'%(btn,q)
    logging.info(q)
    matching_tweets_list = api.search(count=count,lang=lang,q=q) 
    tweet_list = [tweet._json["text"] for tweet in matching_tweets_list]
    return tweet_list

class ResponseHandler(webapp2.RequestHandler):
    def post(self):
        vals = {}
        
        wishes = self.request.get("wishbtn")
        hopes = self.request.get("hopebtn")
        dreams = self.request.get("dreambtn")
        
        if wishes:
            vals['page_title']="wishes from the wishing well"
            vals['header'] = "wishes"
            vals['results'] = apiSearch(btn="i wish")
        elif hopes:
            vals['page_title']="hopes from the wishing well"
            vals['header'] = "hopes"
            vals['results'] = apiSearch(btn="i hope")
        elif dreams:
            vals['page_title']="dreams from the wishing well"
            vals['header'] = "dreams"
            vals['results'] = apiSearch(btn="i dream")

        template = JINJA_ENVIRONMENT.get_template('response.html')
        self.response.write(template.render(vals))
    
application = webapp2.WSGIApplication([('/response',ResponseHandler),
                                       ('/.*',MainHandler)
                                       ],
                                       debug=True)