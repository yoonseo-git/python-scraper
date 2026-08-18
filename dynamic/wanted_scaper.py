from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import csv

class WantedScraper:

    def __init__(self, keywords):
        self.keywords = keywords
        self.p = sync_playwright().start()
        self.browser = self.p.chromium.launch(headless=False)

    def scrape_page(self, url, keyword):
        print(f"Scrapping {url}...")

        local_jobs = []
            
        page = self.browser.new_page()
        page.goto(url)

        time.sleep(2)

        for _ in range(4):
            page.keyboard.down("End")
            time.sleep(2)

        content = page.content()
        soup = BeautifulSoup(content, "html.parser")

        jobs = soup.find_all("div", class_="JobCard_container__zQcZs")

        for job in jobs:
            title = job.find("strong", class_="JobCard_title___kfvj").text
            company_name = job.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__company__ByVLu wds-nkj4w6").text
            reward_tag = job.find("span", class_="JobCard_reward__oCSIQ")
            if reward_tag is None:
                continue
            link = f"https://www.wanted.co.kr/{job.find('a')['href']}"

            job_data = {
                "title": title,
                "company": company_name,
                "reward": reward_tag.text,
                "link": link,
            }

            local_jobs.append(job_data)

        file = open(f"{keyword}.csv", "w", encoding="utf-8", newline="")
        writer = csv.writer(file)

        writer.writerow(["Title", "Company", "Reward", "Link"])

        for job in local_jobs:
            writer.writerow(job.values())

        file.close()

        return local_jobs


    def scrape(self):
        for keyword in self.keywords:
            url = f"https://www.wanted.co.kr/search?query={keyword}&search_method=direct&tab=position"
            jobs = self.scrape_page(url, keyword)
        self.p.stop()
        return jobs


# scraper = WantedScraper(["flutter", "react", "java"])
# scraper.scrape()