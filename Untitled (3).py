#!/usr/bin/env python
# coding: utf-8



import tweepy
import csv
import pandas as pd
import re
from textblob import TextBlob
import matplotlib.pyplot as plt
# Looooove can be shortend to love!
def remove_du(text):
    r = re.compile(r"([a-zA-Z])(\1+)")
    text = r.sub(r"\1",text)
    return text

# remove the url
def remove_url(text):
    text = re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", text)
    return " ".join(text.split())

# Use the TextBlob object to analysis the sentiment
def sentiment(text):
    return TextBlob(text)

# credentials of your account
key = '81mHRPVXsdoWTrFeOSgZxJiE1'
secret = '6hSCmsBVXeXalZPsnqCBp8sW0UdnEsgLhl3qGH6XoHxTxMyAgd'
token = '1236292513939537920-g19HMmiGo8dOKdYltatjXgnr1hXUGT'
token_secret = 'I6CG6vWoCMCZcPER5u9TwgGzuT5Iv8PtlUgL02j2VsaNG'
author = tweepy.OAuthHandler(key, secret)
author.set_access_token(token, token_secret)
api = tweepy.API(author,wait_on_rate_limit=True)
categories = ['Excitement', 'Happy', 'Pleasant', 'Surprise', ' Fear', ' Angry']
emoticons = ['•̀.̫•́✧', '(*´∀｀)', '(^_^.)', '(๑˃̵ᴗ˂̵)ﻭ', '( ﾟдﾟ) ', '(；･`д･´)']#emoticons
all_tweets = []
sen_val = []
tweets_for_crowd = []
for i in range(len(categories)):
        crowd = []
        with open(categories[i]+'.csv', 'w', encoding='utf-8', newline='',) as f:
            headers = ['Tweet id', 'Text', 'Create at', 'Class', 'Emoticons']
            f_csv = csv.writer(f)
            f_csv.writerow(headers)
            hashtag = "#" + categories[i] + " -filter:retweets"
            count = 0
            rows = []
            max_tweet = 200
            for twe in tweepy.Cursor(api.search,q=hashtag,
                                   lang="en",
                                   since="2019-04-03").items(max_tweet):
        
                text = twe.text
                text = remove_du(text)
                without_url = remove_url(text)
                polarity = sentiment(without_url).polarity
                rows.append([twe.user.id, without_url, twe.created_at, "#"+categories[i], emoticons[i]])
                all_tweets.append([twe.created_at, without_url, '#' + categories[i]])
                sen_val.append([polarity, without_url])
                crowd.append([without_url])
                f_csv.writerows(rows)
        tweets_for_crowd.append(crowd)
            
# make the crowd csv file        
for i in range(len(categories)):
    with open(categories[i]+'_crowd'+'.csv', 'w', encoding='utf-8', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(tweets_for_crowd[i])
senti = pd.DataFrame(sen_val, columns=["polarity", "Tweet"])
senti.head()
sen_df = pd.DataFrame(all_tweets, columns=["Create_at", "Tweet", "hashtag"])
date_time = sen_df["Create_at"][:,]
date_time = [i.to_pydatetime() for i in date_time]
date_time = [i.date() for i in date_time]
sen_df['Create_at'] = date_time
from collections import Counter #statistics of text
cnt = Counter(date_time)
date = []
count = []
for i in cnt.items():
    date.append(i[0])
    count.append(i[1])
c = Counter(sen_df[sen_df['Create_at']==date[0]]['hashtag'])
all_c = []
for d in range(len(date)):
    c = Counter(sen_df[sen_df['Create_at']==date[d]]['hashtag'])
    all_c.append(c)
data = []
for i,j in zip(date, all_c):
    for k in j.items():
        data.append([i,k[1],k[0]])
da = pd.DataFrame(data, columns=["Date", "Counts", "Hashtag"])
da.head()

