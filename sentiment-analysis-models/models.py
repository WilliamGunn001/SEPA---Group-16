from tkinter import N
from numpy import dtype
from transformers import pipeline
import csv
from pandas import *
import pandas as pd
from ast import literal_eval
import time
import json

#start time - program runtime testing
start_time = time.time()

#set qty to 100 --- grab 100 data from csv file (set to "all" to model entire dataset)
qty = "all" 

#Here are some choices for models
#1. nlptown/bert-base-multilingual-uncased-sentiment
#2. siebert/sentiment-roberta-large-english
#3. finiteautomata/bertweet-base-sentiment-analysis
#4. cardiffnlp/twitter-roberta-base-sentiment-latest
#5. Seethal/sentiment_analysis_generic_dataset
#6. DaNLP/da-bert-tone-sentiment-polarity
model="DaNLP/da-bert-tone-sentiment-polarity"

#conduct sentiment analysis model
sentiment_analysis = pipeline("sentiment-analysis",model=model)

#string is encoded in latin 1
#declare the header for each column in csv file
column_name = ["Scale", "TweetID", "Date", "Query", "User", "Comments"]
df = pd.read_csv("twitterdata.csv", names=column_name, encoding='latin-1')
# tweet = df.Comments.to_list() #make the column to a list of string

twitter_data = df[['TweetID', 'Comments']].to_dict(orient='records')
# print(twitter_data)

# Accuracy testing
sentiment_results = []

if qty == "all":
    for tweet in twitter_data:
        result = sentiment_analysis(tweet["Comments"])
        result[0]["twitter_id"] = tweet["TweetID"]
        print(result[0])
        sentiment_results.append(result[0])
else:
    qty = int(qty)
    for i in range(0, qty):
        tweet = twitter_data[i]
        result = sentiment_analysis(tweet["Comments"])
        result[0]["twitter_id"] = tweet["TweetID"]
        print(result[0])
        sentiment_results.append(result[0])

print(sentiment_results) # print the sentiment result

with open("output.csv","w",newline="") as f:  # write to csv file
    title = "label,score,twitter_id".split(",") # quick hack
    cw = csv.DictWriter(f,title,delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    cw.writeheader()
    cw.writerows(sentiment_results)

# # Record time of runs
# result = time.time() - start_time
# print("--- %s seconds ---" % result) 
# with open("result.csv", 'a') as fd:
#     fd.write(f"{model},{qty},{result}\n") # write to a csv file to analyse 
