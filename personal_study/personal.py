import requests
from bs4 import BeautifulSoup
import csv
from csv import writer

class Crawler():

    def __init__(self):
        self.url = "https://kr.indeed.com/jobs?q=python&limit=50"

    def getHTML (self, cnt): #여기는 requests.get(웹url) 빼고는 그대로 하면 됨
        r = requests.get(self.url + '&start='+ str(cnt*50))
        if r.status_code != 200:
            print('request error:', r.status_code)

        html = r.text
        soup = BeautifulSoup(html, "html.parser")
        return soup #웹에 있는 소스 가져오게 됨

    def pagesCount(self, soup): #여기에서 select 대신에 find_all()써도 무관?
        pages = soup. select('div.pagination > a') #select 사용법: https://blog.naver.com/kmongsil/221833371866
        return len(pages)

    def getInfo (self, soup, cnt):
        jobCards = soup.find_all('.jobsearch-SerpJobCard')
        jobID=[]
        jobTitle=[]
        jobLocation=[]

        for j in jobCards:
            jobID.append("https://kr.indeed.com/viewjob?jk=" + j["data-jk"]) #??j["data-jk"]의 의미는?
            jobTitle.append(j.find('a', class_='title').replace('\n',''))
            if j.find("span", class_="location") != None:
                jobLocation.append(j.find("span", class_="location").text)
            elif j.find("div", class_="location") != None:
                jobLocation.append(j.find("div", class_="location").text)
        
        self.write_CSV(jobID,jobTitle, jobLocation, cnt)

    def write_CSV(self, jobID, jobLocation, jobTitle, cnt):
        file = open("indeed_test.csv", mode= "w", newline='')
        writer = csv.writer(file)
        writer.writerow(["NO.","Link","Title", "location"])
        for i in range(len(jobID)):
            writer.writerow([str(i + 1 + (cnt * 50)), jobID[i], jobTitle[i], jobLocation[i]])
        file.close

    def playScrawler(self):
        soup_getHTML = self.getHTML(0)
        pages = self.pagesCount(soup_getHTML) #몇페이지인지 확인
        
        for i in range(pages):
            soupHTML = self.getHTML(i)
            self.getInfo(soupHTML, i) #getinfo 끝나면서 csv로 저장함
            print (i+1, "번째 page 끝")


if __name__== "__main__":
    c = Crawler()
    c.playScrawler()

'''
- 파일을 오픈할 수 있는 권한이 없을때.
- 파일이 아니라 폴더를 지정했을 때.
- 파일이 없을때
'''
