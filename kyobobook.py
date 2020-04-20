import requests
from bs4 import BeautifulSoup
import csv
from csv import writer

class Crawler():

    def __init__(self):
        self.url = "https://search.kyobobook.co.kr/web/search?vPstrKeyWord=industrial%2520security&vPstrTab=PRODUCT&searchPcondition=1&currentPage=2&orderClick=LAG#container"

    def getHTML (self): 
        r = requests.get(self.url)
        if r.status_code != 200:
            print('request error:', r.status_code)
        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        return soup


    def getInfo (self, soup):
        bookCard = soup.find_all("tr")
        bookTitle=[]
        bookID=[]
        bookPrice=[]

        for j in bookCard:
            if (j.find('td', class_= "detail") == None) or (j.find("td", class_= "price").find("div", class_ = "sell_price") == None) :
                continue
            bookTitle.append(j.find('td', class_= "detail").find("div", class_="title").find("strong").text)
            bookID.append(j.find("td", class_= "detail").find("div", class_="title").find("a")['href'])
            bookPrice.append(j.find("td", class_= "price").find("div", class_ = "sell_price").find("strong").text.replace(',',"")) 
            
        self.write_CSV(bookTitle, bookPrice, bookID)

    def write_CSV(self, bookTitle, bookPrice, bookID):
        file = open("kyobo_book.csv", "a", newline='', encoding= 'utf-8-sig') 
        wr = csv.writer(file) 
        print(bookTitle[0])
        for i in range(len(bookTitle)):
            num = i+1
            wr.writerow([str(num), bookTitle[i], bookPrice[i], bookID[i]]) 
        file.close

    def playScrawler(self):            
        file = open("kyobo_book.csv", "w",newline='',encoding= 'utf-8-sig') 
        wr = csv.writer(file)
        wr.writerow(["No.", "Title", "Price", "Link"])
        file.close

        soupHTML = self.getHTML()
        self.getInfo(soupHTML) 


if __name__== "__main__":
    c = Crawler()
    c.playScrawler()
