import pandas as pd

df = pd.read_excel("urls.xlsx")

# urls = [
#     "http://feeds.abcnews.com/abcnews/usheadlines",
#     "http://rss.cnn.com/rss/cnn_topstories.rss",
#     "http://www.cbsnews.com/latest/rss/main",
#     "https://feeds.nbcnews.com/nbcnews/public/world",
#     "https://www.theguardian.com/us-news/rss",
#     "http://feeds.harvardbusiness.org/harvardbusiness?format=xml",
#     "https://macleans.ca/author/inklesswells/feed/",
#     "https://www.oneindia.com/rss/news-sports-fb.xml",
#     "https://www.theguardian.com/us/film/rss",
#     "https://www.abc.net.au/news/feed/45924/rss.xml"
# ]
urls = list(df["urls"])
print(urls)
your_webite_url = ""
your_webite_Name = ""


use_paraphrase = False

title_summarise = True