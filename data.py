#! /usr/bin/python

import dateutil.parser as parser
import datetime
import requests
import os
import facebook

class date:

  def __init__(self,year,month,day):
    self.__year = year
    self.__month = month
    self.__day = day

  def __last_feed(self,feeds):
    return feeds[len(feeds) - 1]

  def __created_date(self,feed):
    return parser.parse(feed['created_time']).date()
  
  def __last_feed_created_date(self,feeds):
    return self.__created_date(self.__last_feed(feeds))

  def __birthdate(self):
    return datetime.date(self.__year,self.__month,self.__day)

  def __is_posted_on_birthday(self,feed):
    if self.__created_date(feed) == self.__birthdate():
      return True
  
  def __get_feeds_by_pagination(self,feeds):
    all_feeds = []
    all_feeds = all_feeds + feeds['data']

    while parser.parse(all_feeds[len(all_feeds) - 1]['created_time']).date() == self.__birthdate():
      feeds = requests.get(feeds['paging']['next']).json()
      all_feeds = all_feeds + feeds['data']

    return all_feeds

  def __exclude_already_thanked_posts(self,feed):
    commenters = []
    if 'comments' in feed.keys():
      for comment in feed['comments']['data']:
        commenters.append(comment['from']['name'])

    if os.environ['birthday_boy_name'] not in commenters:
      return True

  def feeds(self):
    graph = facebook.GraphAPI(os.environ['oauth_access_token'])
    feeds = graph.get_object("me/feed")
    all_feeds = self.__get_feeds_by_pagination(feeds)
    return filter(self.__exclude_already_thanked_posts,filter(self.__is_posted_on_birthday,all_feeds))
