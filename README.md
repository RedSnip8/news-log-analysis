# News Log Analyzer

Code written by [Frank Cipolone aka RedSnip8.](https://github.com/RedSnip8)

## Overview
This program is set up to function as a reporting tool for a PostgreSQL database. It will return data based on the following report questions:

  * __What are the *3 most popular* news articles (based on article views)?__
  * __Who are the *3 most popular* authors (based on total indiviual article views)?__
  * __Which days had *more than 1%* of requests lead to errors?__

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
```
CREATE VIEW articleviewcount AS
  SELECT articles.slug, articles.title, articles.author, view_count.count 
  FROM articles, (SELECT path, COUNT(path) FROM log group by path) AS view_count 
  WHERE view_count.path LIKE '%' || articles.slug;
```
> This selects slug, title, and author from the articles table and selects the total count of view from a subquery. The subquery is a match up of the slug from the articles table and the path from the log table, matching the last part of the path to the slug of each article. this does not account for misspelled paths on the user end and only accounts for the correct names. The subquery then counts the amount of request paths to the said articles by thier listed slug.

authorviewcount
```
CREATE VIEW authorviewcount AS
  SELECT authors.id, authors.name, SUM(articleviewcount.count) 
  FROM authors JOIN articleviewcount 
  ON authors.id = articleviewcount.author 
  GROUP BY authors.id;
```
> This selects the id and name of each author from the authors table, and the sum the of count column from previously created articleviewcount. In order to avoid a total count the authors table and the artileviewcount view are inner joinned and matched by the id for each author in the authors table and the author column in the articleviewcount view. The author column in the articleviewcount view has the same values found ub the articles table which is the coorsponding ID for each author.

dailystatuslog
```
CREATE VIEW dailystatuslog AS
    SELECT time::date AS day, COUNT(*) AS total_inqueries, 
    COUNT(case when status != '200 OK' then 1 end) AS errors, 
    ROUND((count(case when status != '200 OK' then 1 end) * 100.0)::numeric 
    / count(*),2) AS error_percent from log group by time::date;
```
>This selects the time from the log table and converts the timestamp timezone format into a date in order to group the status coeds by daily periods. The count of each row is then selected to track all requests even if they did not return a status code for some reason in lieu a count(status) as it is reasonable that a null would be considered an error for later use. Also selected is the rounded product of a count of all non "200 OK" status codes divided by the total logged rows. The return value is set to numerical format and up to 2 decimal places. The errors_percent is by 00.00% format.