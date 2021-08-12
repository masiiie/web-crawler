# Crawler


The crawler implemented is *specific-topic*, since it will collect the 1000 pages most similar to a default one, and all are expected to address the same topic or well-related topics. In this case, the url chosen is [Pintura](https://es.wikipedia.org/wiki/Pintura).

# Scrapy

The implementation in particular is a [**Scrapy**](https://scrapy.org/) project, a very popular **Python** framework in *web crawling*.
The most modified section was root \ spiders \ __ init__.py which contains the QuotesSpider class with the definition of the parse () method that defines the algorithm of crawling as such.


