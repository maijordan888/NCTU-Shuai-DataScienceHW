# NCTU-Shuai-DataScienceHW
## Main purpose
Web scrawler for ptt beauty.
## Function
### --crawl
Get article and popular article title in 2018 year.    
**You should Always execute this first.**
### --push start_date end_date
Get accounts who have top 10 push&boo times.
### --popular start_date end_date
Get picture url in popular article between start_date and end_date.
### --keword start_date end_date
Get picture url which belongs to the article exist the keyword between start_date and end_date.
## Version describe
scrawler.py is the original one which doesn't care about the hint assistant gave.
Hint: In test, it will be first to try the "crawl", so you could (or should) use the output from the crawl.

version2.0.0 came out after scrawler.py. It also forgot the hint but use the function to shorten the code.

version3.0.0 is the version which use the hint, and seems to be the final version.
