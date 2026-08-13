from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import csv

keywords = ["flutter", "react", "java"]

# Playwright, 브라우저를 전역에서 한 번만 생성 (함수 안에서 매번 만들면 오류 발생)
# 함수 안에서 매번 sync_playwright().start() 호출하면
# 이미 실행 중인 Playwright 위에 또 시작하려고 해서 충돌 발생
# 브라우저(Chrome 앱)는 한 번만 켜고, 탭(page)만 새로 여는 방식
p = sync_playwright().start()
browser = p.chromium.launch(headless=False)

def scrape_page(url, keyword):
    print(f"Scrapping {url}...")
    local_jobs = []

    page = browser.new_page()
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
        company_name = job.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__company__ByVLu").text
        link = f"https://www.wanted.co.kr{job.find('a')['href']}"
        reward_tag = job.find("span", class_="JobCard_reward__oCSIQ")

        if reward_tag is None:
            continue

        job = {
            "title": title,
            "company_name": company_name,
            "reward": reward_tag.text,
            "link": link,
        }

        local_jobs.append(job) # 로컬 리스트에 추가

    file = open(f"{keyword}.csv", "w", encoding="utf-8", newline="")
    writer = csv.writer(file)

    writer.writerow(["Title", "Company", "Reward", "Link"])

    for job in local_jobs:
        writer.writerow(job.values())

    file.close()

def scrape(keywords):
    for keyword in keywords: # 키워드별 URL 생성 후 스크랩
        url = f"https://www.wanted.co.kr/search?query={keyword}&search_method=direct&tab=position"
        scrape_page(url, keyword)
    
    p.stop() # Playwright 종료


scrape(keywords)