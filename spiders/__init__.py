# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

from nltk.corpus import stopwords 
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize 
from string import punctuation
import numpy as np

def compute_cosine_similarity(vector1, vector2):
    sum = 0
    square1 = 0
    square2 = 0

    for i,item in enumerate(vector1):
            sum += item*vector2[i]
            square1 += item**2
            square2 += vector2[i]**2

    if square1*square2 == 0: return 0

    return sum/(np.sqrt(square1)*np.sqrt(square2))

def vectorice(texto, indexeds):
    stop_words = set(stopwords.words('spanish'))
    token = word_tokenize(texto)
    ps = PorterStemmer()

    vector = {}
    for x in indexeds:
        vector[x] = 0

    for x in token:
        x = ps.stem(x.lower())
        if x in indexeds:
            if not x in vector:
                vector[x] = 0
            vector[x] += 1

    _max = max(vector.values()) 
    return [vector[x]/_max for x in indexeds]   


# Esta implementacion ahora mismo no garantiza q todos los terminos indexados
# sean sustantivos.
def indexed_terms(texto):
    stop_words = set(stopwords.words('spanish'))
    token = word_tokenize(texto)
    #input('token = {0}'.format(token))
    ps = PorterStemmer()

    vector = {}
    temp = []

    for x in token:
        x = ps.stem(x.lower())
        if x in temp or x in punctuation or x.isdigit():
            continue
        if x in stop_words:
            temp.append(x)
            continue
        if not x in vector:
            vector[x] = 0
        vector[x] += 1  

    _max = max(vector.values())

    indexados = sorted(vector.keys(), key=lambda x: vector[x],reverse=True)[:50]
    #input('indexados = {0}'.format(indexados))
        
    return (vector.keys(),[vector[x]/_max for x in vector])

# CODE

import scrapy
from scrapy.selector import Selector
from scrapy.http.response.html import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.link import Link
from scrapy.http import Request, Response
import requests

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    def __init__(self, category=None, *args, **kwargs):
        super(QuotesSpider, self).__init__(*args, **kwargs)
        self.descargas = 0
        # Profe aqui la url puede que se la devuelva mal xq hasta el momento 
        # estuve trabajando con el servidor de la aplicacion de Wikipedia
        # y no llegue a poner las mas populares de Google.
        self.madre_url = 'http://10.127.127.1:8001/wikipedia_es_all_2017-01/A/Pintura.html' #'https://es.wikipedia.org/wiki/Pintura'
        
        texto = self.extract_text_url(self.madre_url)
        with open('./madre.txt','wb') as f:
            f.write(texto.encode())
        
        self.indexed, self.madre_vetor = indexed_terms(texto)
        self.to_recolect = 5 #10 000

    # Profe a lo mejor estas urls dan error xq las puse a mano no se si estan bien escritas
    def start_requests(self):
        urls = [
            'http://10.127.127.1:8001/wikipedia_es_all_2017-01/A/Pintura.html',
            'http://10.127.127.1:8001/wikipedia_es_all_2017-01/A/Color.html',   #'https://es.wikipedia.org/wiki/Color',
            'http://10.127.127.1:8001/wikipedia_es_all_2017-01/A/Luz.html', #'https://es.wikipedia.org/wiki/Luz',
            'http://10.127.127.1:8001/wikipedia_es_all_2017-01/A/Dibujo.html'] 
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def extract_text(self,response):
        sel = Selector(response)
        e = sel.xpath('.//text()').getall() 
        style_text = sel.xpath('//style/text()').get()
        script_text = sel.xpath('//script/text()').get()
        texto = ''.join(e).replace(style_text,'').replace(script_text,'').replace('\n\n','')
        #input('texto = {0}'.format(texto))
        return texto 
    def extract_text_url(self,url):
        response = requests.get(url)
        return self.extract_text(response)
            

    # La cola inicial de parse es start_request
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