# Crawler


The crawler implemented is *specific-topic*, since it will collect the 1000 pages most similar to a default one, and all are expected to address the same topic or well-related topics. 

# Scrapy

The implementation in particular is a [**Scrapy**](https://scrapy.org/) project, a very popular **Python** framework in *web crawling*.
The most modified section was [\_\_init\_\_.py](./spiders/\_\_init\_\_.py) file which contains the `QuotesSpider` class with the definition of the `parse()` method that defines the algorithm of crawling as such.

```python
def parse(self, response:HtmlResponse):
        texto = self.extract_text(response)
        vector = vectorice(texto,self.indexed)
        similarity = compute_cosine_similarity(vector,self.madre_vetor)

        print('url = {0}'.format(response.url))
        print('similarity = {0}'.format(similarity))
        input('look')

        if similarity < 0.2:
            return

        splited = response.url.split('/')
        splited = [x for x in splited if x != '']
        page_name = ''.join(splited[len(splited)-1])

        with open('web_pages/{0}.html'.format(page_name),'wb') as f:
            f.write(response.body)

        self.descargas += 1
        input('downloaded: {0}'.format(response.url))
        input('descargas = {0}'.format(self.descargas))
        if self.descargas == self.to_recolect:
            return

        extractor = LinkExtractor()
        links = extractor.extract_links(response)

        for link in links:
            if link is not None:
                requests
                yield Request(link.url)
```

# Choice of seed URLs

Since the task does not have to be shared with other crawlers, the seed URLs are a set of popular pages, chosen in this case with a query to [Google](https://www.google.com/) with the word "paint", those with the highest *PageRank*.

