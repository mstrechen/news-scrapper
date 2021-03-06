import requests
from datetime import datetime 
from lxml import html
import resizeimage

from ..article import Article


from .IArticleScraper import IArticleScraper


class Scraper(IArticleScraper):
    def __init__(self):
        self.url = "tsn.ua"

    def update_article(self, article: Article):
        src = requests.get(article.url).content
        tree = html.fromstring(src)
        
        try:
            text = tree.xpath('//*[@id="main-content"]//' +
                              'article[contains(@class, "u-content-read") or ' +
                              'contains(@class, "c-main")]')[0]
        except IndexError:
            return

        text = self.elem_to_str(text)

        article.text = self.get_pure_text(text)
        article.richtext = text
        img = tree.xpath("/html/body/div[5]/div[3]/div/div[3]/div/div[1]/img/@src")
        if not img:
            img = tree.xpath('//*[@id="main-content"]/' +
                             'div/div[1]/div/div[2]/header/div[1]/div/div[1]/div[1]/img/@src')
        try:
            dt = tree.xpath('//*[@id="main-content"]//header//time/@datetime')[0]
        except IndexError:
            dt = tree.xpath('//*[@id="main-content"]//time/@datetime')[0]
        dt = str(dt)
        
        article.datetime = datetime.strptime(dt[:19], "%Y-%m-%dT%H:%M:%S")

        if img:
            img = img[0]
            img = str(img)
            try:
                article.img = "/storage/" +\
                self.process_image("http://" + article.get_source(), img, height=100)
            except resizeimage.imageexceptions.ImageSizeError:
                article.img = ""
