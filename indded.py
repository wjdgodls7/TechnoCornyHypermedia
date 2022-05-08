import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&limit={LIMIT}"


def get_last_pages():
  result = requests.get(URL)
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("div",{"class":"pagination"})
  links = pagination.find_all('a')
  pages = []

  for link in links[:-1] :
    pages.append(int(link.string))

  max_page = pages[-1]
  return max_page

def extract_job(html):
  title = html.find("h2",{"class":"jobTitle"}).find("span",title=True).string
# title.find("span" ,title=True ) 은 title 이 있는 span 을 찾아라 입니다.
  company = html.find("span",{"class":"companyName"}).string
  location = html.find("div",{"class":"companyLocation"}).string
  job_id = html["data-jk"]
  
  return {"title":title,"company":company,"location":location,"link":f"https://kr.indeed.com/jobs?q=python&l&vjk={job_id}&from=web&vjs=3"}

def extract_jobs(last_page):
  jobs = []
  for page in range(last_page):
    print(f"Scrapping Indeed page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("a",{"class":"tapItem"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs

def get_jobs():
  last_page = get_last_pages()
  jobs = extract_jobs(last_page)
  return jobs