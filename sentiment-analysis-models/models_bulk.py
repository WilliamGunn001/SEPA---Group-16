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

#set qty to 10 --- grab 10 data from csv file (set to "all" to model entire dataset)
qty = "all" 

#string is encoded in latin 1
#declare the header for each column in csv file
column_name = ["Scale", "TweetID", "Date", "Query", "User", "Comments"]

#read in csv file 
df = pd.read_csv("newoutput.csv", names=column_name, encoding='latin-1')


twitter_data = df[['TweetID', 'Comments']].to_dict(orient='records')
# print(twitter_data)

# Labels 
labels = {
    "negative": ["negative","1 star","2 stars","neg","label_0"],
    "neutral": ["neutral","3 stars","neu","label_1"],
    "positive": ["positive","4 stars","5 stars","pos","label_2"]
}

def convert_scale(result):
    label = result["label"].lower()
    score = result["score"]

    if "star" in label:
        scale = int(label[0])
        if scale <= 2:
            result["label"] = "Negative"
        elif scale >=4:
            result["label"] = "Positive"
        else:
            result["label"] = "Neutral"
        result["scale"] = scale
    elif label in labels["negative"]:
        result["label"] = "Negative"
        if(score >= 0.7):
            result["scale"] = 1
        else:
            result["scale"] = 2
    elif label in labels["neutral"]:
        result["label"] = "Neutral"
        result["scale"] = 3
    elif label in labels["positive"]:
        result["label"] = "Positive"
        if(score >= 0.7):
            result["scale"] = 5
        else:
            result["scale"] = 4

    return result

# Result array
sentiment_results = []

# run bulk models
models_list = ["nlptown/bert-base-multilingual-uncased-sentiment", "siebert/sentiment-roberta-large-english", "finiteautomata/bertweet-base-sentiment-analysis", "cardiffnlp/twitter-roberta-base-sentiment-latest", "Seethal/sentiment_analysis_generic_dataset", "DaNLP/da-bert-tone-sentiment-polarity"]

for model in models_list:

    sentiment_analysis = pipeline("sentiment-analysis",model=model)
    
    if qty == "all":
        for tweet in twitter_data:
            result = sentiment_analysis(tweet["Comments"])
            result[0]["twitter_id"] = tweet["TweetID"]
            new_result = convert_scale(result[0])
            print(new_result)
            sentiment_results.append(new_result)
    else:
        qty = int(qty)
        for i in range(0, qty):
            tweet = twitter_data[i]
            result = sentiment_analysis(tweet["Comments"])
            result[0]["twitter_id"] = tweet["TweetID"]
            new_result = convert_scale(result[0])
            print(new_result)
            sentiment_results.append(new_result)

print(sentiment_results) # print the sentiment result

with open("output.csv","w",newline="") as f:  # write to csv file
    title = "label,score,twitter_id,scale".split(",") # quick hack
    cw = csv.DictWriter(f,title,delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    cw.writeheader()
    cw.writerows(sentiment_results)

# # Record time of runs
# result = time.time() - start_time
# print("--- %s seconds ---" % result) 
# with open("result.csv", 'a') as fd:
#     fd.write(f"{model},{qty},{result}\n") # write to a csv file to analyse 