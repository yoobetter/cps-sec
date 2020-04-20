import requests 
from bs4 import BeautifulSoup
import csv


class Scraper(): 
    def __init__(self): 
        self.url = "http://hince.co.kr/category/lipstick/48?page=" 
    
    def getHTML(self, cnt): 
        res = requests.get(self.url + str(cnt)) 
        if res.status_code != 200: 
            print('request error:', res.status_code)

        html = res.text 
        soup = BeautifulSoup(html, "html.parser")
        return soup

#    def getPages(self, soup): 
#        pages = soup.find("div", class_ = "xans-element- xans-product xans-product-normalpaging pagination").find("li")
#        return len(pages)

    def getCards(self, soup, cnt): 
        lipCards = soup.find_all("div", class_ = "product-info")
        lipID = []
        lipTitle = []
        lipPrice = []   
        
        for j in lipCards: 
            if (j.find("div", class_ = "name") == None) or (j.find("div", class_ = "name").find("span", class_= "price-now xans-record-") == None) :
                continue
            lipID.append(j.find("div", class_ = "name").find("a")['href'])
            lipTitle.append(j.find("div", class_ = "name").find("span")) 
            lipPrice.append(j.fing("span", class_= "price-now xans-record-").find("span"))
            
        self.writeCSV(lipID, lipTitle, lipPrice, cnt)

    def writeCSV(self, lipID, lipTitle, lipPrice, cnt): 
        file = open("hince.csv", "a", newline='', encoding= 'utf-8-sig') 
        wr = csv.writer(file)
        for i in range(len(lipID)):
             wr.writerow([str(i + 1 + (cnt * 24)), lipTitle[i], lipPrice[i], lipID[i]])        
        file.close

    def scrap(self): 
        # soupPage = self.getHTML(0)
        # pages = self.getPages(soupPage)

        file = open("hince.csv", "w",newline='',encoding= 'utf-8-sig') 
        wr = csv.writer(file)
        wr.writerow(["No.", "Title", "Price", "Link"])
        file.close
              
        for i in range(2):
            soupCard = self.getHTML(i)
            self.getCards(soupCard, i)
            print(i+1, "번째 페이지 Done")
        

if __name__== "__main__": 
    s = Scraper()
    s.scrap()
