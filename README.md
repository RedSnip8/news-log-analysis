# News Log Analyzer

Code written by [Frank Cipolone aka RedSnip8.](https://github.com/RedSnip8)

### Index
* [Overview](#overview)
* [Desription of Code Function](#code-function)
* [Getting Started](#getting-started)
* [How to Use](#how-to)
* [Created Views](#views)


## <a name="overview"></a>Overview
This program is set up to function as a reporting tool for a PostgreSQL database. It will return data based on the following report questions:

  * __What are the *3 most popular* news articles (based on article views)?__
  * __Who are the *3 most popular* authors (based on total indiviual article views)?__
  * __Which days had *more than 1%* of requests lead to errors?__

The program is python based making use of the psycop2 DB-API and is meant to be connected to a premade news databased using PostgreSQL.

## <a name="code-function"></a>Description of Code Function

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


## <a name="getting-started"></a>Getting Started:

### System Requirements
This code is meant to run on either Ubuntu 16.04 with PostgreSQL and Python 3. If you already have these then feel free to continue on to the [Maunal setup for existing Linux System](#manual-set).

### Setting up a virtual system
For Windows, Mac, and non-Ubuntu machines you will need to run a [virtual box](https://www.virtualbox.org/) and use the tool [vagrant](https://www.vagrantup.com/). This will run a virtual Ubuntu 16.04 system on your exisitng hardware. You will be able to connect to the system locally. You will need to use a Unix-style terminal. On Non-windows based machines your built in terminal will do just fine. For windows users use the [Git-Bash](https://gitforwindows.org/) terminal. A download link for git bash can be found [here](https://git-scm.com/downloads).

#### Virtual  Box
To begin download [VirtualBox 5.1 here](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1) and look for you specific os in the list under the VirtualBox 5.1.38 list. After installation of VirtualBox you will not need to launch as Vagrant, which will be installed after, will take care of that for you! 
For linux users best results can be found by installing it via command line using:
> The following isntructions can be found [here](https://www.virtualbox.org/wiki/Linux_Downloads), below they where adjusted for VirtualBox-5.1

##### Oracle Linux
Users of Oracle Linux 6 and 7 can use the Oracle Linux yum  repository and enable the  ol6_developer channel for Oracle Linux 6 or the  ol7_developer channel for Oracle Linux 7. After that, do 
```
yum install VirtualBox-5.1
```

##### Debian-based Linux distributions
Add the following line to your /etc/apt/sources.list. According to your distribution, replace '<mydist>' with 'artful', 'zesty', 'yakkety', 'xenial', 'trusty', 'stretch', 'jessie', or 'wheezy' (older versions of VirtualBox supported different distributions): 
```
deb https://download.virtualbox.org/virtualbox/debian <mydist> contrib
```
The Oracle public key for apt-secure can be downloaded 
* [here](https://www.virtualbox.org/download/oracle_vbox_2016.asc)for Debian 8 ("Jessie") / Ubuntu 16.04 ("Xenial") and later 
* [here](https://www.virtualbox.org/download/oracle_vbox.asc) for older distributions. 

You can add these keys with 
```
sudo apt-key add oracle_vbox_2016.asc
sudo apt-key add oracle_vbox.asc
```

or combine downloading and registering: 
```
sudo apt-key add oracle_vbox_2016.asc
sudo apt-key add oracle_vbox.asc
```

The key fingerprint for oracle_vbox_2016.asc is 
```
B9F8 D658 297A F3EF C18D  5CDF A2F6 83C5 2980 AECF
Oracle Corporation (VirtualBox archive signing key) <info@virtualbox.org>
```

The key fingerprint for oracle_vbox.asc is 
```
7B0F AB3A 13B9 0743 5925  D9C9 5442 2A4B 98AB 5139
Oracle Corporation (VirtualBox archive signing key) <info@virtualbox.org>
```

 To install VirtualBox, do
```
sudo apt-get update
sudo apt-get install virtualbox-5.1
```

What to do when experiencing The following signatures were invalid: BADSIG ... when refreshing the packages from the repository? 
```
# sudo -s -H
# apt-get clean
# rm /var/lib/apt/lists/*
# rm /var/lib/apt/lists/partial/*
# apt-get clean
# apt-get update
```

##### RPM-based Linux distributions
Oracle provides a yum/dnf-style repository for Oracle Linux/Fedora/RHEL/openSUSE. All .rpm packages are signed. The Oracle public key for rpm can be downloaded here. You can add this key (not normally necessary, see below!) with 
```
sudo rpm --import oracle_vbox.asc
```

or combine downloading and registering: 
```
wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | rpm --import -
```

The key fingerprint is
```
7B0F AB3A 13B9 0743 5925  D9C9 5442 2A4B 98AB 5139
Oracle Corporation (VirtualBox archive signing key) <info@virtualbox.org>
```

After importing the public key, the package signature can be checked with 
```
rpm --checksig PACKAGE_NAME
```

Note that importing the key is not necessary for yum users (Oracle Linux/Fedora/RHEL/CentOS) when using one of the virtualbox.repo files from below as yum downloads and imports the public key automatically! Zypper users should run 
```
zypper refresh
```

#### Vagrant
Vagrant manages virtual enviorments. It will be used via the command line/git bash terminal to connect and transfer files. Click [here](https://en.wikipedia.org/wiki/Vagrant_(software) for more information on vagrant. You can [download Vagrant here](https://www.vagrantup.com/downloads.html). Once Installation is complete run the following in your terminal(git bash temrinal for windows)
```
vagrant --version
```
to ensure that vagrant is successfully installed on your computer.

### Configuring your Virtual Machine
The specific configuration for this program to run can be found in [This .zip file from Udacity](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip). If you are a windows user and time out [use Udacity's updated vagrant file](https://s3.amazonaws.com/video.udacity-data.com/topher/2019/March/5c7ebe7a_vagrant-configuration-windows/vagrant-configuration-windows.zip)

you can also fork and clone the Udacity repository (https://github.com/udacity/fullstack-nanodegree-vm). For information on forking and cloning [check out this](https://stackoverflow.com/questions/6286571/are-git-forks-actually-git-clones) awesome explination on Stack Overflow. For help cloning and forking [follow the instructions here](https://help.github.com/en/articles/fork-a-repo) on github.

After it is installed use the cd command to access the newly downloaded FSND-Virtual-Machine file. Once inside move to the vagrant file using cd and then type vagrant up:
```
cd <your-specific-path>/FSND-Virtual-Machine/vagrant
vagrant up
```

### <a name="manual-set"></a>Manual setup for existing Linux system
If you would prefer to use your personal installation of Ubunutu 16.04 or Ubuntu 18.04 then be sure to make sure the following prerequisites are met by running the following in your command line:
```
sudo apt-get -qqy install make zip unzip postgresql

sudo apt-get -qqy install python3 python3-pip

sudo pip3 install --upgrade pip

sudo pip3 install flask packaging oauth2client redis passlib flask-httpauth

sudo pip3 install sqlalchemy flask-sqlalchemy psycopg2-binary bleach requests

sudo apt-get -qqy install python python-pip

sudo pip2 install --upgrade pip

sudo pip2 install flask packaging oauth2client redis passlib flask-httpauth

sudo pip2 install sqlalchemy flask-sqlalchemy psycopg2-binary bleach requests

sudo postgres -c 'createuser -dRS <your-username>'
```
>These are based off of what can be found in [Udacity's FSND-Virutal-Machine/VagrantFile](https://github.com/udacity/fullstack-nanodegree-vm/blob/master/vagrant/Vagrantfile)


### Prep for first use

##### Virtual Route
If you took the virtualization route you will be able to use your virtual machine after vagrant has finished it's initial setup. By running
```
vagrant ssh
```
you will be able to SSH into your virtual machine. If you don't know what ssh is more information can be [found here](https://en.wikipedia.org/wiki/Secure_Shell). This specific ssh session will be handled by vagrant itself. You will see your command line prompt shift to display your new status as a Vagrant user on your virtual machine. 

After testing of your mahine connection is complete [download this Postgre database configuration](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) provided by Udacity. Unzip the file and place in you FSND-Virtual-Machine/vagrant directory. Once the unzipped file has be moved to the approriate folder, either via command line or using the system based file manager, return to your terminal and access the /FSND-Virtual-Machine/vagrant directory. From here run
```
psql -d news -f newsdata.sql
```
to create the database used for this program.

##### Manual Set-Up Route
If already run Ubuntu 16.04 or above and used the manual set up route then you will need to simply [download the database config](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) provided by Udacity. Once you unzip the file simple do the following
```
cd <your-path-to-the-zip>
psql -d news -f newsdata.sql
```
and your database will be created!

#### Making log-analysis.py executable
Besure to fork and clone news-log-analyis repository for this program if you haven't already. Make your way to the programs directory and run chmod -x to make the file executable:
```
cd <your-path-to>/news-log-analysis
chmod -x log-analysis.py
```


## <a name="how-to"></a>How to Use
Now that your preperations are complete you can start running the Log Analysis program. It will generate reports which can be found in the accompanying reports folder. To run the program open a new terminal shell and be sure to run the application while in the /news-log-analysis directory to function properly.
```
cd <your-path-to>/news-log-analysis
```

```
./log_analysis.py
```
All reports are sent to the reports folder. Check you reports folder to verify the the file has been generated by the application. They will be timestamped.
```
ls reports
```
To read files use your favorite editor below are some options.
```
code reports/newsReport_*YYYMonDD_HH.MM_ZCODE*.txt

subl reports/newsReport_*YYYMonDD_HH.MM_ZCODE*.txt

nano reports/newsReport_*YYYMonDD_HH.MM_ZCODE*.txt

vimtutor
vim reports/newsReport_*YYYMonDD_HH.MM_ZCODE*.txt
```


### <a name="views"></a>Created Views for use
The Python code relies heavily on the following views being created in order to save time on the applicaiton end. __Be sure to create each table in oreder shown.__
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