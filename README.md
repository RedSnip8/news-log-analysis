# News Log Analyzer

Code written by [Frank Cipolone aka RedSnip8.](https://github.com/RedSnip8)

## Overview
This program is set up to function as a reporting tool for a PostgreSQL database. It will return data based on the following report questions:

  __* What are the *3 most popular* news articles (based on article views)?__
  __* Who are the *3 most popular* authors (based on total indiviual article views)?__
  __* Which days had *more than 1%* of requests lead to errors?__

The program is python based making use of the psycop2 DB-API and is meant to be connected to a premade news databased using PostgreSQL.

## Description of code function

In order to satisfy each report question the code does the following:

  _What are the 3 most popular articles?_
  * Create a view from the log table, grouping each request by their paths.
  * Get a count for each path request, excluding typo requests
  * Join correctly named paths with thier slugs in the articles table
  * Return back a count for each Article namde and it's total historical views

  _Who are the 3 most popular authors?_
  * Utilize the same view created for view_count
  * pair each view count the the articles table, via the slug
  * match each article to thier respective authors in the Authors table by their author number in the articles table and the ID number in authors table
  * return the 3  authors with the highest view counts by name and count

  _Which days had more than 1% of requests lead to errors?_
  * count each status code and group them by dates
  * count each status code that is not a 200 OK and group them by dates
  * divide the count of non 200 OK's by the total status codes for each day
  * return each date that has a product of 0.01 or more


## How to use



### Created Views for use
Views were created for the following:

articleviewcount
    CREATE VIEW articleviewcount AS
        SELECT 

authorviewcount
    CREATE VIEW authorviewcount AS
        SELECT 

dailystscodes
    CREAT VIEW dailystscodes AS
        SELECT