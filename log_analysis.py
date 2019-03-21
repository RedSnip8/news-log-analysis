#!/usr/bin/env python3

import psycopg2
import time
import os

# Declare variable for Database Name
DBNAME = "news"


def get_top_articles():
    # Get the 3 most popular posts
    conn = psycopg2.connect(dbname=DBNAME)
    cur = conn.cursor()
    cur.execute(
        "select title, count from articleviewcount order by count desc limit 3;"
        )
    top_posts = cur.fetchall()
    conn.close()
    return top_posts


def get_top_authors():
    # Get the 3 most popular authors
    conn = psycopg2.connect(dbname=DBNAME)
    cur = conn.cursor()
    cur.execute(
        "select name, sum from authorviewcount order by sum desc limit 3;"
        )
    top_authors = cur.fetchall()
    conn.close()
    return top_authors


def get_high_error_day():
    # Get days with >1% error codes
    conn = psycopg2.connect(dbname=DBNAME)
    cur = conn.cursor()
    cur.execute(
        "select day, error_percent from dailystatuslog where error_percent > 1 order by day;"
        )
    error_log = cur.fetchall()
    conn.close()
    return error_log


# Write data to a txt file

# Variables for gets
toparticles = get_top_articles()
topauthors = get_top_authors()
errors = get_high_error_day()

# variable for time and date stamp
timestmp = time.strftime("%Y%b%d_%H.%M_%Z")
# Get CWD as variable
cwd = os.getcwd()
# Create a new file with time stamp in log folder
report = open(cwd + "/reports/newsReport_" + timestmp + ".txt", "w+")
# write each chunk of data with two new lines between them
report.write("Top Articles and View Count\r\n")
for article in toparticles:
    report.write("Article: " + article[0] + "\n  Views: " + str(article[1]) + "\r\n")

report.write("\n\nTop Authors and View Count\r\n")

for author in topauthors:
    report.write("Author: " + author[0] + "\n Views: " + str(author[1]) + "\r\n")

report.write("\n\nDays With Page Request Errors over 1%\r\n")
for day in errors:
    report.write(
        "Day: " + str(day[0]) +
        "\n Error Percentage: " +
        str(day[1])
        + "%\r\n"
        )
# save the new report file
report.seek
report.close()
