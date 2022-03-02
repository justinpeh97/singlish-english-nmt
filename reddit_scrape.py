import praw
import time
import re
from helper_functions import clean_comments_reddit, custom_splitting, convert_to_sentences, filter_sentences
import argparse

# Model parameters



def scrape_subreddit(subreddit, num_threads):
    print("Scraping", subreddit)
    start = time.time()

    hot_posts = reddit.subreddit(subreddit).top(limit=num_threads)

    hot_posts_ids = []
    for post in hot_posts:
        hot_posts_ids.append(post.id)
        
    comments = []

    for hot_posts_id in hot_posts_ids:
        submission = reddit.submission(id=hot_posts_id)

        submission.comments.replace_more(limit=0)
        for comment in submission.comments.list():
            comments.append(comment.body)

    print(len(comments), "comments scraped")
    print(time.time() - start)
    
    return comments

def main():
    parser = argparse.ArgumentParser(description = "Arguments for Reddit scraping")
    parser.add_argument("--client_id", type = str, help = "client id")
    parser.add_argument("--client_secret", type = str, help = "client secret")
    parser.add_argument("--user_agent", type = str, help = "user agent")
    parser.add_argument("--posts_per_subreddit", type = int, default = 3000)
    parser.add_argument("--output", type = str, default = "datasets/raw/raw_reddit.txt")
    args = parser.parse_args()

    global reddit
    reddit = praw.Reddit(client_id= args.client_id, client_secret= args.client_secret, user_agent= args.user_agent)
    subreddits = open("data_generate/subreddits.txt").read().splitlines()
    file = open(args.output ,"w",encoding = "utf-8")
    num_sentences = 0
    for subreddit in subreddits:
        comments = scrape_subreddit(subreddit,args.posts_per_subreddit)
        cleaned_comments = []
        for comment in comments:
            comment = re.sub('[\n|\t]+',"",comment)
            cleaned_comments.append(comment)
        cleaned_comments = clean_comments_reddit(cleaned_comments)
        sentences = convert_to_sentences(cleaned_comments)
        filtered_sentences = filter_sentences(sentences)
        for sentence in filtered_sentences:
            file.write(sentence + "\n")
            num_sentences += 1
    print("Reddit: Total number of sentences collected:", num_sentences)

if __name__ == '__main__':
    main()


