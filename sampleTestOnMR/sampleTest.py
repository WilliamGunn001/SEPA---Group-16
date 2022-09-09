import pandas as pd
from transformers import pipeline
import csv
from functools import reduce

#Test push
def runWithModel(twitter_data, model, labelName):
    qty = 1000 

    sentiment_results = []

    #conduct sentiment analysis model
    sentiment_analysis = pipeline("sentiment-analysis",model=model)

    qty = int(qty)
    for i in range(0, qty):
        tweet = twitter_data[i]
        result = sentiment_analysis(tweet["Comments"])
        result[0]["twitter_id"] = tweet["TweetID"] # result is a type of list, result[0] is a type of dict
        sentiment_results.append(result[0])

    df = pd.DataFrame(sentiment_results)
    df.rename(columns= {"label" : labelName}, inplace=True) #rename the column name for different MRs label output
    return df 

def MR1(twitter_data, model):
    for i in twitter_data:
        i['Comments'] = i['Comments'] + " I like it."
    return runWithModel(twitter_data, model, "MR1_label") # return MR1 df
    
def MR2(twitter_data, model):
    for i in twitter_data:
        i['Comments'] = i['Comments'] + " I don't like it."
    return runWithModel(twitter_data, model, "MR2_label") # return MR2 df

def MR3(twitter_data, model):
    for i in twitter_data:
        i['Comments'] = i['Comments'] + " :)"
    return runWithModel(twitter_data, model, "MR3_label") # return MR3 df

def MR4(twitter_data, model):
    for i in twitter_data:
        i['Comments'] = i['Comments'] + " :("
    return runWithModel(twitter_data, model, "MR4_label") # return MR4 df

if __name__ == '__main__':
    column_name = ["Scale", "TweetID", "Date", "Query", "User", "Comments"]

    #read in csv file 
    df = pd.read_csv("data.csv", names=column_name, encoding='latin-1')

    twitter_data = df[['TweetID', 'Comments']].to_dict(orient='records')

    #Here are some choices for models
    #1. nlptown/bert-base-multilingual-uncased-sentiment
    #2. finiteautomata/bertweet-base-sentiment-analysis
    #3. cardiffnlp/twitter-roberta-base-sentiment-latest
    #4. Seethal/sentiment_analysis_generic_dataset
    model="Seethal/sentiment_analysis_generic_dataset"

    originalDF = runWithModel(twitter_data, model, "original_label")
    print(originalDF)
    mr1DF = MR1(twitter_data, model)
    print(mr1DF)
    mr2DF = MR2(twitter_data, model)
    print(mr2DF)
    mr3DF = MR3(twitter_data, model)
    print(mr3DF)
    mr4DF = MR4(twitter_data, model)
    print(mr4DF)
    data_frames = [originalDF, mr1DF, mr2DF, mr3DF, mr4DF]
    resultDF = reduce(lambda  left,right: pd.merge(left,right,on=['twitter_id'], how='left'), data_frames)
    print(resultDF)

    fileName = "./output_seethal.csv"
    resultDF.to_csv(fileName, encoding="utf-8")