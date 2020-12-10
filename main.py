import datetime #to convert timestamp format to simple datetime formt.
import csv #to create CSV file.
import requests #to create a function to call the API when we need it.
import time #to handle time-related functions.
import pandas as pd #to read the csv file.
import matplotlib.pyplot as plt #to plot out data.

def str_to_timestamp(date):
    """
        string to timestamp date format
    """
    date = datetime.datetime.strptime(date,'%Y%m%d') #format
    date = date.timestamp()
    return str(int(date)) #delete float part and convert to string to use in base url

def make_next_date(date):
    """
        get date as timestamp format and add one day to this date   
    """
    next_date = datetime.datetime.utcfromtimestamp(int(date)) # to datetime format
    next_date += datetime.timedelta(days=1) # add one day
    next_date = next_date.timestamp() #convert to timestamp
    print( datetime.datetime.utcfromtimestamp(int(next_date)).strftime('%Y-%m-%d %H:%M:%S'))
    return str(int(next_date)) # don't need float part!

def save_to_csv(posts,subreddit):
    """
        save posts to csv file with subreddit name
    """
    with open(subreddit+".csv", 'w',encoding="utf-8",newline='') as csvfile: 
        #make column label based on one of post's fields
        writer = csv.DictWriter(csvfile, fieldnames = posts[0].keys() )
        writer.writeheader() 
        writer.writerows(posts)

def get_pushshift_posts(first_date,last_date,subreddit):
    """
        get reddit posts from pushshift api within given range and 
        with one day step using subreddit keyword 
    """

    three_month_posts = []
 
    #make the first & next_dates
    first_date = str_to_timestamp(first_date)
    last_date = str_to_timestamp(last_date)
    #make next 
    next_date = make_next_date(first_date)                                                    
    while True:
            #make the pushshift url with first_date and next_date with respect to our key field information that we wanna extract! 
            base_url = f"https://api.pushshift.io/reddit/submission/search/?before={next_date}&after={first_date}&fields=created_utc,author,title,num_comments,url,upvote,score&size=500&limit=100&sort=desc&subreddit={subreddit}"
            print(base_url)
            response = requests.get(base_url) #make a call to pushshift api
            if response.status_code == 200: #if request is successful
                re = response.json()# get json part of response
                posts = re['data'] # get the value part of data (api return dict object with key data and posts as value)                
                #append to all the posts one by one 
                [three_month_posts.append(i) for i in posts]
                print(len(three_month_posts))
                first_date = next_date #take the next day as start 
                if int(first_date) > int(last_date): 
                    break
                next_date = make_next_date(next_date) #make the next date
           
            else:
                #if request failed due to the large number of sent requests, wait for 1 sec then send new request! 
                time.sleep(1)
                #save the returned data into a csv file
    save_to_csv(three_month_posts,subreddit)
    return three_month_posts

vim=get_pushshift_posts("20200101","20200330","vim") #take posts data of vim subreddit of three months(2020/01/01--2020/03/30) 
emacs=get_pushshift_posts("20200101","20200330","emacs")#take posts data of emacs subreddit of three months(2020/01/01--2020/03/30)


df1 = pd.read_csv('vim.csv',encoding='utf8') #read the vim csv 
df2 = pd.read_csv('emacs.csv',encoding='utf8') #read the emacs csv 
df1['created_utc'] = pd.to_datetime(df1['created_utc'],unit='s').dt.date #vim convert to datetime!
df2['created_utc'] = pd.to_datetime(df2['created_utc'],unit='s').dt.date #emacs convert to datetime!


#plot the authors name and number of their proposed comments(num_comments) beneath of each posts in both vim+emacs subreddits! 
df1.plot(x='author', y='num_comments', legend=True, figsize=(100,10)) #vim
df2.plot(x='author', y='num_comments', legend=True, figsize=(100,10)) #emacs


#simotaniously comparison of #(number of comments) and (the scores) of vim and emacs subreddits with plot
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10,10))
axes[0].plot(df1['score']) #vim
axes[0].plot(df2['score']) #emacs
axes[1].plot(df1['num_comments']) #vim
axes[1].plot(df2['num_comments']) #emacs
