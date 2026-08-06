from selenium import webdriver
from bs4 import BeautifulSoup
import time

keywords = ["flutter", "python", "golang"]
all_jobs = []

driver = webdriver.Chrome()

def scape_page(url):
    print(f"Scrapping {url} ...")
    driver.get(url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")

    tbody = soup.find("tbody")
    if tbody is None:
        print(f"tbody 없음 : {url}")
        return

    jobs = tbody.find_all("tr", attrs={"data-offset": True})

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
        all_jobs.append(job_data)

for keyword in keywords:
    url = f"https://remoteok.com/remote-{keyword}-jobs"
    scape_page(url)

driver.quit()
print(len(all_jobs))
