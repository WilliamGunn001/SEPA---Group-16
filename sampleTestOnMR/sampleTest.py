import pandas as pd
from transformers import pipeline
import csv
import random
import re
from functools import reduce


# function to run sentiment model using passed data, model, and label name
def runWithModel(twitter_data, model, labelName):
    qty = 1000 # define the number of samples

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

# First MR, which adds a positive statement
# Add a positive sentiment to all samples, then all previously positive samples will be checked
def MR1(twitter_data, model):
    # Collect repository of statements that can be added randomly
    pos_df = twitter_data[twitter_data[""] == "p"]

    for i in twitter_data:
        r_int = random.randint(0, len(pos_df))
        i['Comments'] = i['Comments'] + pos_df["comments"].iloc[r_int] # add a random positive statement to each comment

        #i['Comments'] = i['Comments'] + " I like it."
    return runWithModel(twitter_data, model, "MR1_label") # return MR1 df

# Second MR, which adds a negative statement
def MR2(twitter_data, model):
    # Collect repository of statements that can be added randomly
    neg_df = twitter_data[twitter_data[""] == "n"]

    for i in twitter_data:
        r_int = random.randint(0, len(neg_df))
        i['Comments'] = i['Comments'] + neg_df["comments"].iloc[r_int] # add a random negative statement to each comment

        #i['Comments'] = i['Comments'] + " I don't like it."
    return runWithModel(twitter_data, model, "MR2_label") # return MR2 df

# Third MR, which adds a positive emoticon
def MR3(twitter_data, model):
    for i in twitter_data:
        i['Comments'] = i['Comments'] + " :)"
    return runWithModel(twitter_data, model, "MR3_label") # return MR3 df

# Fourth MR, which adds a negative emoticon
def MR4(twitter_data, model):
    for i in twitter_data:
        i['Comments'] = i['Comments'] + " :("
    return runWithModel(twitter_data, model, "MR4_label") # return MR4 df

# Fifth MR, which removes repeating characters after 2+ repeats
def MR5(twitter_data, model):
    for i in twitter_data:
        num_occur = 1
        str = i["Comments"]
        prev = ""
        new_s = ""
        for chr in str.lower():
            if chr == prev:  # if the character has repeated itself
                num_occur += 1  # add one to the number of repeats
                if num_occur > 2:  # if the character has repeated itself more than twice
                    continue
            else:
                num_occur = 1
            new_s += chr
            prev = chr
        i["Comments"] = new_s
    return runWithModel(twitter_data, model, "MR5_label")

# Sixth MR, which removes repetitions of exclamation marks
def MR6(twitter_data, model):
    for i in twitter_data:
        str = i["Comments"]
        prev = ""
        new_s = ""
        for chr in str.lower():
            if (chr == prev) and (chr == "!"):  # if the character has repeated itself
                continue
            new_s += chr
            prev = chr
        i["Comments"] = new_s
    return runWithModel(twitter_data, model, "MR6_label")

# Seventh MR, which replaces twitter usernames with a default tag
def MR7(twitter_data, model):
    for i in twitter_data:
        i["Comments"] = re.sub(r'\@\w+', '@twitteruser', i["Comments"])  # replace any word starting with @ with @twitteruser
    return runWithModel(twitter_data, model, "MR7_label")

# Eigth MR, which removes instances of "lol", "lmao", and "omg"
def MR8(twitter_data, model):
    for i in twitter_data:
        str = i["Comments"]
        new_s = str.replace('lol', '')  # replace all "lol" phrases wth empty space
        new_s = new_s.replace('lmao', '')  # replace all "lmao" phrases wth empty space
        new_s = new_s.replace('omg', '')  # replace all "omg" phrases wth empty space
        i["Comments"] = new_s
    return runWithModel(twitter_data, model, "MR8_label")

# Ninth MR, which randomly shuffles a string
def MR9(twitter_data, model):
    for i in twitter_data:
        str = i["Comments"]
        words = str.split()  # Split string into array of words
        random.shuffle(words)  # Randomly shuffle position of array words
        new_s = ' '.join(words)  # Re-join array into new string
        i["Comments"] = new_s
    return runWithModel(twitter_data, model, "MR9_label")



if __name__ == '__main__':
    column_name = ["Scale", "TweetID", "Date", "Query", "User", "Comments"]

    #read in csv file 
    df = pd.read_csv("data.csv", names=column_name, encoding='latin-1')

    # Convert data columns to dictionary
    twitter_data = df[['TweetID', 'Comments']].to_dict(orient='records')

    #Here are some choices for models
    #1. nlptown/bert-base-multilingual-uncased-sentiment
    #2. finiteautomata/bertweet-base-sentiment-analysis
    #3. cardiffnlp/twitter-roberta-base-sentiment-latest
    #4. Seethal/sentiment_analysis_generic_dataset
    model="Seethal/sentiment_analysis_generic_dataset"

    # Run original model against sentiment model
    originalDF = runWithModel(twitter_data, model, "original_label")
    print(originalDF)
    
    # Run sentiment model against MRs 
    mr1DF = MR1(twitter_data, model)
    print(mr1DF)
    mr2DF = MR2(twitter_data, model)
    print(mr2DF)
    mr3DF = MR3(twitter_data, model)
    print(mr3DF)
    mr4DF = MR4(twitter_data, model)
    print(mr4DF)
    mr5DF = MR5(twitter_data, model)
    print(mr5DF)
    mr6DF = MR6(twitter_data, model)
    print(mr6DF)
    mr7DF = MR7(twitter_data, model)
    print(mr7DF)
    mr8DF = MR8(twitter_data, model)
    print(mr8DF)
    mr9DF = MR9(twitter_data, model)
    print(mr9DF)

    # Merge all dataframes together
    data_frames = [originalDF, mr1DF, mr2DF, mr3DF, mr4DF, mr5DF, mr6DF, mr7DF, mr8DF, mr9DF]
    resultDF = reduce(lambda  left,right: pd.merge(left,right,on=['twitter_id'], how='left'), data_frames)
    print(resultDF)

    # Save file to csv
    fileName = "./output_seethal.csv"
    resultDF.to_csv(fileName, encoding="utf-8")