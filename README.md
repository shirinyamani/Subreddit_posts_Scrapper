# Subreddit_Submissions_Sccraper
# 1.Using Pushshift Module for Reddit Submissions Data extraction with Python
When we want to grab data for a specific date range in the past, we need to use Pushshift API. This is because the Reddit API does not allow us to have a time-based search on both endpoints(i.e. /reddit/search/submission or /comments). Therefore, we need to use Pushshift API, which basically is a copy of all reddit objects, right at the time they were posted (i.e. comments & posts). In the following code, I went for extracting (2020/01/01--2020/03/30) submissions data from /emacs and /vim subreddits
# 2.Convert to timestamp format
The format of the returned data in every call from pusshift api is JSON. So, we need timestamp format which is readable for api in base url.
# 3.Get all three-months (2020/01/01--2020/03/30) posts data.
our general purpose has set to extract all data whithin the mentioend three-months. Since a year ago, pushshift api allows us to get only 1000 results per return. This means, we have 2 ways to be able to grab all the posts data in subreddits. 1) to categorize the search period to too many small periods, and from each period we get 1000 data which would be pretty time-consuming, Or 2)extracting the data day by day (on a daily-basis limit size=1000). I found the second solution much better! So, I went for it in the following!
# 4.Save to CSV file
Till here, we scrape the data from both subreddits(emacs & vim). So now we need to save them in an excel file.
# 5.Get the posts from Pushshift API
We can access the Pushshift API through building an URL with the relevant parameters. In this regard, generally speaking, in order to search for submissions, we use the endpoint https://api.pushshift.io/reddit/search/submission/ . However, since our search has some other parameters such as the auther, sort_type, after, before, subreddit, size, so we need to first build our url based on wanted parameters.
### Parameters for our Pushshift URL:

• size — limit of returned entries

• after — where to start the search

• before — where to end the search

• title — to search only within the submission’s title

• subreddit — to narrow it down to a particular subreddit

### Key information for our Submissions subreddits(vim+emacs) data extraction:
• author name —(author)

• title of the post —(title)

• score —(score)

• URL —(url)

• creation time of post —(created_utc)

• number of comments of the posts —(num_comments)

Created URL based on the key imformation that we want to extract from the posts:  

https://api.pushshift.io/reddit/submission/search/?before={next_date}&after={first_date}&fields=created_utc,author,title,num_comments,url,upvote,score&size=500&limit=100&sort=desc&subreddit={subreddit}"

• after — 20200101

• before — 20200330

• subreddit — emacs and vim
# 6.Get the submissions data from pushshift + update the search date + then save the result into a CSV
In this step we update our data gatheration function to get the next day posts. (please refer to the explanation file for better understanding)
# 7.Used pandas mondule to read the CSV then convert timestamp format to datetime format to be shown in datetime format in the CSV *(explanation file)*
# 8.used matplotlib for plotting both subreddits(emacs + vim) to have comparison of the key chosen fields *(explanation file)*
