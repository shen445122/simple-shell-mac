#-*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests,time,json

D_file = "./list"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}

def get_detail(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
# url = "https://book.douban.com/subject/34869428/"
    web_data = requests.get(url,headers=headers)
    soup = BeautifulSoup(web_data.text,'lxml')
    rank = soup.select('#interest_sectl > div > div.rating_self.clearfix > strong')[0].get_text().strip()
# print(rank)
    return rank
def get_book(title):
    url = "https://book.douban.com/j/subject_suggest?q=%s"%title
    rsp = requests.get(url,headers=headers)
    rs_dict = json.loads(rsp.text)
# print(rs_dict)
    url_ = rs_dict[0]['url']
# print(url_)
    return url_,get_detail(url_)

if __name__ == '__main__':
    file = open(D_file, encoding = "utf-8")

    with open(D_file) as file:
        for item in file:
            url,rank = get_book(item)
            print(item,rank,url)