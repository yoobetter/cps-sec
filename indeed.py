'''
    1. 웹사이트 접속
    2. 웹사이트 html 받아오기
    3.  html에서 원하는 정보 찾기
    4. 수집 
'''
import requests 
from bs4 import BeautifulSoup
import csv


class Scraper(): #아래에서 jobTitle, jobLocation, jobId를 뽑는 과정을 페이지 수만큼 반복해야 해서 그냥 함수를 선언함
    def __init__(self): #클래스 내부에 함수를 정의할 때 첫번째 매개변수로 self를 준다
        self.url = "https://kr.indeed.com/jobs?q=python&limit=50" #변수 추가하고 싶을 때 함수.변수명(init에 선언된 변수는 클래스내 전역변수)
    
    def getHTML(self, cnt): 
        res = requests.get(self.url + "&start=" + str(cnt*50)) #각 페이지별로 접근하는 것
        if res.status_code != 200: #status_code 함수는 특정 url의 상태코드를 알려줌
            print('request error:', res.status_code)

        html = res.text #html 소스 받아오기
        soup = BeautifulSoup(html, "html.parser")#html 태그 정보 가져올 준비과정. 원하는 정보 수집위해 beautifulsoup을 쓸 수 있는 형태로 전환
        return soup

    def getPages(self, soup): #페이지수 세기
        pages = soup.select('div.pagination > a')
        return len(pages)#page 수 출력함 #그냥 pages를 출력하면 <a data-pp="gQJYAAAAAAAAAAAAAAABgBY5WAAHAQAA5jQdwAADAgAB" 이런식으로 나오므로 length 사용

    def getCards(self, soup, cnt): #페이지 내에서 내가 원하는 특정 정보만 수집
        jobCards = soup.find_all("div", class_ = "jobsearch-SerpJobCard")
        #find_all("태그유형", 요소이름)
        jobID = []
        jobTitle = []
        jobLocation = []   
        
        for j in jobCards: #위에서 받아온 페이지의 수만큼 for문을 돌려줘야함
            jobID.append("https://kr.indeed.com/viewjob?jk=" + j["data-jk"])
            jobTitle.append(j.find("a").text.replace("\n","")) #\n이 들어간 계행문자를 없앤다
            if j.find("div", class_ = "location") != None:
                jobLocation.append(j.find("div", class_ = "location").text)
            elif j.find("span", class_ = "location") != None:
                jobLocation.append(j.find("span", class_ = "location").text)
            
        self.writeCSV(jobID, jobTitle,jobLocation, cnt)

    def writeCSV(self, jobID, jobTitle, jobLocation, cnt): 
        file = open("indeed.csv", "a", newline='', encoding= 'utf-8-sig') #a모듈: 기존에 있던 csv파일의 마지막 행에 데이터 추가
        wr = csv.writer(file) #csv파일로 저장하는 코드
        for i in range(len(jobID)):
             wr.writerow([str(i + 1 + (cnt * 50)), jobID[i], jobTitle[i], jobLocation[i]])        
        file.close

    def scrap(self): #파이썬 파일을 한 번 돌린다는 의미- 스크랩퍼가 실행되며 indeedcsv파일을 초기화함
        soupPage = self.getHTML(0)
        pages = self.getPages(soupPage)

        file = open("indeed.csv", "w",newline='',encoding= 'utf-8-sig') #encoding add part .... #, newline=''
        wr = csv.writer(file)
        wr.writerow(["No.", "Link", "Title", "Location"])
        file.close
              
        for i in range(pages):
            soupCard = self.getHTML(i)
            self.getCards(soupCard, i)
            print(i+1, "번째 페이지 Done")
        

if __name__== "__main__": #이걸 사용하면 다른 파일이나 대화형 인터프리터에서 이 모듈을 불러 사용하면 if문 다음이 수행이 안 됨. 즉 이 모듈이 들어있는 창을 실행할 때만 그 밑에 적혀있는 것들이 실행되는 것
    s = Scraper()
    s.scrap()

'''
- 파일을 오픈할 수 있는 권한이 없을때.
- 파일이 아니라 폴더를 지정했을 때.
- 파일이 없을때
'''