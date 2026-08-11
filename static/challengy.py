from selenium import webdriver
from bs4 import BeautifulSoup
import time

class RemoteOKScrapper:

    def __init__(self, keywords):
        self.keywords = keywords
        self.all_jobs = []
        self.driver = webdriver.Chrome()
        
    def scrape_page(self, url):
        print(f"Scrapping {url} ...")
        self.driver.get(url)
        time.sleep(3)

        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        jobs = soup.find("tbody").find_all("tr", attrs={"data-offset": True})
        
        for job in jobs:
            title_tag = job.find("h2", itemprop="title")
            company_tag = job.find("h3", itemprop="name")
            location_tag = job.find("div", class_="location")
        
            if title_tag is None or company_tag is None or location_tag is None:
                continue
        
            job_data = {
                    "title": title_tag.text.strip(),
                    "company": company_tag.text.strip(),
                    "location": location_tag.text.strip(),
                }
            self.all_jobs.append(job_data)


    def scrape(self):
        for keyword in self.keywords:
            url = f"https://remoteok.com/remote-{keyword}-jobs"
            self.scrape_page(url)
        self.driver.quit()
        print(len(self.all_jobs))

# __init__ 실행 → keywords, all_jobs, driver 초기화
scraper = RemoteOKScrapper(["flutter", "python", "golang"])
# scrape() 실행 → keywords 순회 → scrape_page() 3번 호출 → driver.quit() → 결과 출력
scraper.scrape()
