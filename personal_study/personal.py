import requests
from bs4 import BeautifulSoup
import csv
from csv import writer

class Crawler():

    def __init__(self):
        self.url = "https://search.kyobobook.co.kr/web/search?vPstrKeyWord=industrial%2520security&vPstrTab=PRODUCT&searchPcondition=1&currentPage="

    def getHTML (self, cnt): #여기는 requests.get(웹url) 빼고는 그대로 하면 됨
        r = requests.get(self.url + str(cnt+1) + '&orderClick=LAG#container')
        if r.status_code != 200:
            print('request error:', r.status_code)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        return soup #웹에 있는 소스 가져오게 됨

    def pagesCount(self, soup): #여기에서 select 대신에 find_all()써도 무관?
        pages = soup. select('div > li > a') #select 사용법: https://blog.naver.com/kmongsil/221833371866
        return len(pages)

    def getInfo (self, soup, cnt):
        bookCard = soup.find_all('tr')
        bookTitle=[]
        bookID=[]
        bookPrice=[]

        for j in bookCard: 
            bookTitle.append(j.find('td', class_= "detail").find("div", class_="title").find('strong')) 
            bookID.append(j.find('td', class_= "detail").find("div", class_="title").find('a').text)
            bookPrice.append(j.find('td', class_ = 'price').find('div', class_ = 'sell_price').find('strong'))
            cnt = cnt + 1 
        
        self.write_CSV(bookTitle, bookPrice, bookID, cnt)

    def write_CSV(self, bookTitle, bookPrice, bookID, cnt):
        file = open("kyobo_book.csv", "a", newline='', encoding= 'utf-8-sig') 
        wr = csv.writer(file) #csv파일로 저장하는 코드
        for i in range(len(bookTitle)):
             wr.writerow([str(i+1+(cnt*20)), bookTitle[i], bookPrice[i], bookID[i]]) 
        file.close

    def playScrawler(self):
        soup_getHTML = self.getHTML(0)
        pages = self.pagesCount(soup_getHTML) #몇페이지인지 확인
        
        file = open("kyobo_book.csv", "w",newline='',encoding= 'utf-8-sig') 
        wr = csv.writer(file)
        wr.writerow(["No.", "TItle", "Price", "Link"])
        file.close

        for i in range(pages):
            soupHTML = self.getHTML(i)
            self.getInfo(soupHTML, i) 
            print (i+1, "번째 page 끝")


if __name__== "__main__":
    c = Crawler()
    c.playScrawler()