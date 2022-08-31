# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd


def print_hi():
    # Use a breakpoint in the code line below to debug your script.
    column_name = ["Scale", "TweetID", "Date", "Query", "User", "Comments"]

    df = pd.read_csv("input.csv", names=column_name, encoding='latin-1')
    df['Comments'] = 'str: '+df['Comments']
    df.to_csv('str.csv')
def new():
    column_name = ["Scale", "TweetID", "Date", "Query", "User", "Comments"]
    df = pd.read_csv("data.csv", names=column_name, encoding='latin-1')
    df['Comments']=df['Comments'].str.replace("omg|lol|lmao|OMG|LOL|LMAO","").str.strip()
    df.to_csv('MR1.csv')

def new1():
    column_name = ["Scale", "TweetID", "Date", "Query", "User", "Comments"]
    df = pd.read_csv("data.csv", names=column_name, encoding='latin-1')
    df['Comments'] = df["Comments"].str.replace(r'.*(\w)\1', "").str.strip()
    df.to_csv('MR2.csv')

def test():
    df = pd.read_csv("test cardif.csv", encoding='latin-1')
    df['str violation'] = df['label_str']==df['label']
    df['upper violation'] = df['label_upper']==df['label']
    print(df['str violation'].value_counts())
    print(df['upper violation'].value_counts())

    df.to_csv('test_output_cardif.csv')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('mmm')
  #  print_hi()
    #   test()
    new()
    new1()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
