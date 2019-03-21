#!/usr/bin/env python3

import psycopg2
import time
import os

# Declare variable for Database Name
DBNAME = "news"

#variable for database queries for:

# -top artiles using established view
artilces_query = """select title, count from articleviewcount
        order by count desc limit 3;"""

# -top authors using estblished view
authors_query =  """select name, sum from authorviewcount
        order by sum desc limit 3;"""

# -days with returned data errors over 1%
errorPerc_query = """select day, error_percent from dailystatuslog
        where error_percent > 1 order by day;"""

# variable for time and date stamp
timestmp = time.strftime("%Y%b%d_%H.%M_%Z")
# Get CWD as variable
cwd = os.getcwd()
# Create a new file with time stamp in log folder
report = open(cwd + "/reports/newsReport_" + timestmp + ".txt", "w+")


def execute_query(sql_code):
    conn = psycopg2.connect(dbname=DBNAME)
    cur = conn.cursor()
    cur.execute(sql_code)
    data = cur.fetchall()
    conn.close()
    return data

# Write data to a txt file

# Variables for gets
toparticles = execute_query(artilces_query)
topauthors = execute_query(authors_query)
errors = execute_query(errorPerc_query)

# write each chunk of data with two new lines between them
report.write("Top Articles and View Count\r\n")
for article in toparticles:
    report.write(
        "Article: " + article[0] +
        "\n  Views: " + str(article[1]) + "\r\n"
            )

report.write("\n\nTop Authors and View Count\r\n")

for author in topauthors:
    report.write(
        "Author: " + author[0] +
        "\n Views: " + str(author[1]) + "\r\n"
            )

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
