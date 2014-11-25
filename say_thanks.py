import dateutil.parser as parser
import datetime
import sys
import facebook
import os

class Thanks:
  def __init__(self,feeds,thanks_message):
    self.__feeds = feeds
    self.__thanks_message = thanks_message

  def __get_input(self, prompt):
    return raw_input(prompt).rstrip(' \n')

  def __get_message(self,well_wisher_name):
    if self.__get_input('Comment with default message? ') == 'y':
      return "@" + well_wisher_name + " " + self.__thanks_message + " :-D !!!"
    else:
      return self.__get_input("Your personalized message: ")

  def __post_comment(self,feed,well_wisher_name):
    comment_message = self.__get_message(well_wisher_name)
    graph = facebook.GraphAPI(os.environ['oauth_access_token'])
    post = graph.put_comment(feed['id'], message = comment_message)
    if post.get('id'):
      print 'Your comment: ',comment_message
    else:
      print 'Default comment Added'

  def __feed_message(self,feed):
    return feed['message']
  
  def __well_wisher_full_name(self,feed):
    return feed['from']['name'].encode('utf-8')

  def __well_wisher_first_name(self,feed):
    return self.__well_wisher_full_name(feed).rsplit(' ')[0]

  def __say_thanks_to_well_wisher(self, feed):
    well_wisher_first_name = self.__well_wisher_first_name(feed)
    
    print 'message: "{0}"'.format(self.__feed_message(feed))
    print 'from: {0}'.format(self.__well_wisher_full_name(feed))

    if self.__get_input('Do you wish to say Thanks? ') == 'y':
      self.__post_comment(feed,well_wisher_first_name)

  def wish_all(self):
    for feed in self.__feeds:
      self.__say_thanks_to_well_wisher(feed)
      print '\n'
