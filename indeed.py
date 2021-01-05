import requests
from bs4 import BeautifulSoup
LIMIT = 50
URL = f"https://www.indeed.com/jobs?q=Python&limit={LIMIT}"

def extract_indeed_pages():
  result = requests.get(URL)
  soup=BeautifulSoup(result.text,"html.parser")
  pagination = soup.find("div",{"class":"pagination"})
  links = pagination.find_all('a')
  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))
  max_page = pages[-1]
  return max_page

def extract_job(h):
  title = h.find("h2",{"class":"title"}).find("a")["title"]
  company = h.find("span", {"class": "company"})
  if company.find("a") is not None :
    com = str(company.find("a").string)
  else :
    com = str(company.string)
  com = com.strip()
  location = h.find("div", {"class" : "recJobLoc"})["data-rc-loc"]
  job_id = h["data-jk"]
  return {'title':title, 'company': com, 'location': location, 
  "link": f"https://www.indeed.com/viewjob?jk={job_id}"}

def extract_indeed_jobs(last_page):
  jobs = []
  for page in range(last_page) :
    print(f"Scrapping page {page}")
    result = requests.get(f"{URL}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text,"html.parser")
    results=soup.find_all("div",{"data-tn-component": "organicJob"})
    for result in results:
      job = extract_job(result)
      jobs.append(job)
  return jobs