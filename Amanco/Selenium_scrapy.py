# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from time import sleep



name = 'teste'
allowed_domains = ['http://amanco.com.br']
start_urls = ['http://amanco.com.br/produtos/predial/agua-quente']


driver = webdriver.Firefox(executable_path='/Users/Bruno.cunha/PycharmProjects/untitled/geckodriver')
driver.get(start_urls[0])
page = driver.page_source
search_button = True
while search_button:
    try:
        button = driver.find_element_by_xpath('/html/body/main/article[3]/div/div/div[3]/div')
        button.click()
        print('clickei no botão')
    except:
        search_button = False
        print('nao encontrei')
page = driver.page_source
resp = HtmlResponse(url=start_urls[0], body=page,encoding = 'utf-8')
url_products = resp.css('div.row article.product a ::attr(href)').getall()
print('links de produtos',url_products)
        
#categorias = driver.find_element_by_xpath('/html/body/header/nav/ul/li[1]/ul/li/a').get_attribute('href')



####NAO APAGUE MESSI!!!!!

driver.close()