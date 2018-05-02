
import praw
import config
import time
import os
import re

def bot_login():
    r = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "Bamboozle Insurance Bot v0.1")
    print("Logged in!")
    return r

def run_bot(r, comments_replied_to):
	print("Obtaining 100 comments...")

	for comment in r.subreddit('all').comments(limit=100):
		if "bamboozle" in comment.body and comment.id not in comments_replied_to and comment.author != r.user.me():
			print("String with \"bamboozle\" found " + comment.id)
			comment.reply("""Worried about being bamboozled? Fear not! Get your bamboozle insurance for the simple cost of 1 upvote. Upvote this comment for your FREE BAMBOOZLE INSURANCE!""")
			print("Replied to comment " + comment.id)

			comments_replied_to.append(comment.id)

			with open("comments_replied_to.txt", "a") as f:
				f.write(comment.id + "\n")

	print("Sleeping for 10 seconds")
	#Sleep for 10 seconds
	time.sleep(10)

def get_saved_comments():
	if not os.path.isfile("comments_replied_to.txt"):
		comments_replied_to = []
	else:
		with open("comments_replied_to.txt", "r") as f:
			comments_replied_to = f.read()
			comments_replied_to = comments_replied_to.split("\n")
			comments_replied_to = list(filter(None, comments_replied_to))

	return comments_replied_to

r = bot_login()
comments_replied_to = get_saved_comments()
print(comments_replied_to)

while True:
	run_bot(r, comments_replied_to)