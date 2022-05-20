from tkinter import N
from numpy import dtype
from transformers import pipeline
import csv
from pandas import *
import pandas as pd
from ast import literal_eval
import time
import json
from datetime import datetime

#Converted to object but dont need to
class models(object):
	def __init__(self):
		#start time - program runtime testing
		start_time = time.time()

		#set qty to 100 --- grab 100 data from csv file (set to "all" to model entire dataset)
		self.qty = "all" 

		# Labels 
		self.labels = {
			"negative": ["negative","1 star","2 stars","neg","label_0"],
			"neutral": ["neutral","3 stars","neu","label_1"],
			"positive": ["positive","4 stars","5 stars","pos","label_2"]
		}

	def convert_scale(self, result):
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
		elif label in self.labels["negative"]:
			result["label"] = "Negative"
			if(score >= 0.7):
				result["scale"] = 1
			else:
				result["scale"] = 2
		elif label in self.labels["neutral"]:
			result["label"] = "Neutral"
			result["scale"] = 3
		elif label in self.labels["positive"]:
			result["label"] = "Positive"
			if(score >= 0.7):
				result["scale"] = 5
			else:
				result["scale"] = 4

		return result

	def run(self, nlpModel, fileDeets, fromDate, endDate, include, exclude, filter):
		print("Working", nlpModel)
		#Here are some choices for models
		#1. nlptown/bert-base-multilingual-uncased-sentiment
		#2. siebert/sentiment-roberta-large-english
		#3. finiteautomata/bertweet-base-sentiment-analysis
		#4. cardiffnlp/twitter-roberta-base-sentiment-latest
		#5. Seethal/sentiment_analysis_generic_dataset
		#6. DaNLP/da-bert-tone-sentiment-polarity

		#Check which model is needed
		if nlpModel == "Nlptown":
			model = "nlptown/bert-base-multilingual-uncased-sentiment"
		elif nlpModel == "Siebert":
			model = ""
		elif nlpModel == "Finiteautomata":
			model = "finiteautomata/bertweet-base-sentiment-analysis"
		elif nlpModel == "Cardiffnlp":
			model = "cardiffnlp/twitter-roberta-base-sentiment-latest"
		elif nlpModel == "Seethal":
			model = "Seethal/sentiment_analysis_generic_dataset"
		elif nlpModel == "DaNLP":
			model = "DaNLP/da-bert-tone-sentiment-polarity"

		#conduct sentiment analysis model
		sentiment_analysis = pipeline("sentiment-analysis",model=model)

		#string is encoded in latin 1
		#declare the header for each column in csv file
		column_name = ["Scale", "TweetID", "Date", "Query", "User", "Comments"]

		df = pd.read_csv(fileDeets[0], names=column_name, encoding='latin-1')
		# tweet = df.Comments.to_list() #make the column to a list of string

		#Added date
		twitter_data = df[['TweetID', 'Comments', 'Date']].to_dict(orient='records')
		# print(twitter_data)

		# Accuracy testing
		sentiment_results = []
		

		if self.qty == "all":
			#Does filter need to be applied?
			filterEnabled = False
			if filter != "":
				wordProcessing = filter.split(",")
				filterWords = []
				#Makes list 'whole words' (surrounded by whitespace) case sensitive?
				for w in wordProcessing:
					filterWords.append(" " + w.strip() + " ")
				filterEnabled = True
			for tweet in twitter_data:
				#Converts tweet date to date object for comparison
				#This will need to be changed to be more robust but works with current tweet time formatting
				date = datetime.strptime(tweet["Date"], "%a %b %d %H:%M:%S PDT %Y").date()

				#Checks if tweet is in date range
				#could potentially make this more efficient if data was sorted by time/date
				if date < fromDate or date > endDate:
					print (tweet["TweetID"], " out of date")
					continue

				#Filters tweets by words
				if filterEnabled:
					if exclude:
						if any(word in tweet["Comments"] for word in filterWords):
							print (tweet["TweetID"],tweet["Comments"], " filtered")
							continue
					elif include:
						#Possible sub selection - Must include all words or any words?
						if not any(word in tweet["Comments"] for word in filterWords):
							print (tweet["TweetID"],tweet["Comments"], " filtered")
							continue
				#print (tweet["TweetID"],tweet["Comments"], " not filtered")

				result = sentiment_analysis(tweet["Comments"])
				result[0]["twitter_id"] = tweet["TweetID"]
				result[0]["date"] = tweet["Date"]
				new_result = self.convert_scale(result[0])
				print(new_result)
				sentiment_results.append(new_result)
		else:
			qty = int(qty)
			for i in range(0, qty):
				tweet = twitter_data[i]
				result = sentiment_analysis(tweet["Comments"])
				result[0]["twitter_id"] = tweet["TweetID"]
				result[0]["date"] = tweet["Date"]
				new_result = self.convert_scale(result[0])
				print(new_result)
				sentiment_results.append(new_result)

		print(sentiment_results) # print the sentiment result

		with open("output.csv","w",newline="") as f:  # write to csv file
			title = "label,score,twitter_id, date, scale".split(",") # quick hack
			cw = csv.DictWriter(f,title,delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			cw.writeheader()
			cw.writerows(sentiment_results)

		# # Record time of runs
		# result = time.time() - start_time
		# print("--- %s seconds ---" % result) 
		# with open("result.csv", 'a') as fd:
		#     fd.write(f"{model},{qty},{result}\n") # write to a csv file to analyse 
