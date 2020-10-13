import re
import tweepy
from textblob import TextBlob
from wordcloud import WordCloud
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
CONSUMERKEY = "5Wittq9oSwEecQrKo67RoGnZv"
CONSUMERSECRET = "cS6eAjrdFhRCLTjitROrLeNni2QHZRYjjsNutauaxxLywf33a0"
ACCESSTOKEN = "221322633-AvWsANI3XXOqJP9hgI1TF6zgwWv6xU4uEXrBk2JL"
ACCESSTOKENSECRET = "ZfuCGRWvkVdkv6Vl4pngMf8u4zyByZuZwoQgOxOHt55M2"
authenticate = tweepy.OAuthHandler(CONSUMERKEY,CONSUMERSECRET)
authenticate.set_access_token(ACCESSTOKEN, ACCESSTOKENSECRET)
api = tweepy.API(authenticate, wait_on_rate_limit=True)
posts = api.user_timeline(screen_name="@Bill Gates", count=100, lang="en", tweet_mode="extended")
print("show the five and recent tweets: \n")
i=1
for tweet in posts[0:5]:
    print(str(i) + ')'+ tweet.full_text + '\n')
    i=i+1
# Stage 0- Importing Libraries and then setting keys for APIs
df=pd.DataFrame([tweet.full_text for tweet in posts],columns=['Tweets'])
df.head()
def clean_Txt(text):
    text=re.sub(r'@[A-Za-z0-9]+','',text)
    text=re.sub(r'#','',text)
    text=re.sub(r'RT[\s]+','',text)
    text=re.sub(r'https?:\/\/S+','',text)
    return text
df['Tweets']=df['Tweets'].apply(clean_Txt)
print(df)
def get_Subjectivity(text):
    return TextBlob(text).sentiment.subjectivity
def get_Polarity(text):
    return TextBlob(text).sentiment.polarity
df['Subjectivity']=df['Tweets'].apply(get_Subjectivity)
df['Polarity']=df['Tweets'].apply(get_Polarity)
print(df)
allWords=' '.join([twts for twts in df['Tweets']])
wordCloud=WordCloud(width=500,height=300,random_state=21,max_font_size=119).generate(allWords)
plt.imshow(wordCloud,interpolation='bilinear')
plt.axis('off')
plt.show()
def get_Analysis(score):
    if score<0:
        return 'Negative'
    elif score==0:
        return 'Neutral'
    else:
        return 'Positive'
df['Analysis']=df['Polarity'].apply(get_Analysis)
print(df)
#Stage 1: Cleaning data (Removing @,#,hyperlinks etc )
#print positive tweets
j=1
sortedDF=df.sort_values(by=['Polarity'])
for i in range(0,sortedDF.shape[0]):
    if sortedDF['Analysis'][i]=='Positive':
        print(str(j) + ')'+sortedDF['Tweets'][i])
        print()
        j=j+1
#print all negative tweets
j=1
sortedDF=df.sort_values(by=['Polarity'],ascending='False')
for i in range(0,sortedDF.shape[0]):
    if(sortedDF['Analysis'][i]=='Negative'):
        print(str(j) + ')'+sortedDF['Tweets'][i])
        print()
        j=j+1
#plot polarity and subjectivity
plt.figure(figsize=(8,6))  
for i in range(0,df.shape[0]):
    plt.scatter(df['Polarity'][i],df['Subjectivity'][i],color='green')      
plt.title('Sentiment Analysis')  
plt.xlabel('Polarity')
plt.ylabel('Subjectivity')
plt.show()   
 #get the percentage of positive tweets
ptweets=df[df.Analysis=='Positive']
ptweets=ptweets['Tweets']
print(round((ptweets.shape[0]/df.shape[0])*100,1))
   #get the percentage of negative tweets
ntweets=df[df.Analysis=='Negative']
ntweets=ntweets['Tweets']
print(round((ntweets.shape[0]/df.shape[0])*100,1))
#show the value counts iii8uyh
print(df['Analysis'].value_counts)
#plot and visualize counts
plt.title('Sentiment Analysis')
plt.xlabel('Sentiment')
plt.ylabel('counts')
df['Analysis'].value_counts().plot(kind='bar')
plt.show()
#stage2





