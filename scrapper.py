import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from slugify import slugify

URL = "https://www.detik.com/tag/hukum/?sortby=time&page=10"
html = requests.get(URL).text
page = BeautifulSoup(html, "html.parser")
post_list = page.find("div", class_="list-berita")
post_item = post_list.find_all("article")

post_dict = {
    'title' : [],
    'seo_title' : [],
    'author_id' : [],
    'category_id' : [],
    'slug': [],
    'excerpt': [],
    'body': [],
    'image': [],
    'status': [],
    'created_at': [],
    'updated_at': [],
    'meta_description': [],
    'meta_keywords': [],
    'featured': [],
    'source': [],
}

for p in post_item:
    post_url = requests.get(p.find("a")['href']).text
    post_page = BeautifulSoup(post_url, "html.parser")

    title = post_page.title.string
    source = "<a href='{}' target='_blank'>{}</a>".format(p.find("a")['href'], 'detikJabar')

    post_dict['title'].append(title)
    post_dict['author_id'].append(3)
    post_dict['category_id'].append(1)
    post_dict['slug'].append(slugify(title))
    post_dict['seo_title'].append(title)
    post_dict['excerpt'].append(p.find("p").text)
    post_dict['body'].append(post_page.find("div", class_="detail__body-text").text)
    post_dict['image'].append(p.find("img")['src'])
    post_dict['status'].append('PUBLISHED')
    post_dict['created_at'].append(datetime.date.today())
    post_dict['updated_at'].append(datetime.date.today())
    post_dict['meta_description'].append(post_page.find('meta',attrs={'name':'description'})['content'])
    post_dict['meta_keywords'].append(post_page.find('meta',attrs={'name':'keywords'})['content'])
    post_dict['featured'].append(0)
    post_dict['source'].append(source)



engine = create_engine('mysql+pymysql://{db_user}:{db_pass}@{db_host}/{db_name}')
df = pd.DataFrame.from_dict(post_dict)
df.to_sql(con=engine, name='posts', if_exists='append', index=False)
df.head(5)
