This software is created to crawl the twitter information by twitter api, 
which used hash tags to crawl 'Excitement', 'Happy', 'Pleasant', 'Surprise', 'fear' and' Angry' user data, respectively.
 Each class has 150 items, totally have 900 tweets. We extract out the text to analysis the sentiment of user’s, 
and labeled it with the real hash tag. All the data will be saved to csv format file with columns 'Tweet id', 'Text', 'Create at', 'Class', 'Emoticons'.
Programming language: python 3.6
Package: textblob 0.15.3, tweepy 3.8.0.