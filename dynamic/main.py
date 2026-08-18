from playwright.sync_api import sync_playwright # Playwright - 브라우저 자동화 라이브러리
from bs4 import BeautifulSoup # HTML 파싱 라이브러리
from file import save_to_file
import time


p = sync_playwright().start() # Playwright 시작

browser = p.chromium.launch(headless=False) # headless=False -> 브라우저 화면 보이게 실행

page = browser.new_page() # 새 탭 열기

page.goto("https://www.wanted.co.kr/search?query=flutter&search_method=direct&tab=position") # URL 이동

time.sleep(3) # 페이지 로딩 대기

# 아래 주석 처리된 부분은 각각의 요소를 직접 찾아 동적으로 움직이는 것

# page.click("button.wds-1cqc7gt")

# time.sleep(3)

# page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")

# time.sleep(3)

# page.keyboard.down("Enter")

# time.sleep(3)

# page.click("a#search_tab_position")

# time.sleep(3)

# page.click("body")

# time.sleep(3)

# End 키 4번 눌러서 스크롤 내리기 (동적 로딩 데이터 가져오기 위함)
for _ in range(4): # _ -> 변수 사용 안할 때 관례적으로 사용
    page.keyboard.down("End")
    time.sleep(2)

content = page.content() # 현재 페이지 HTML 가져오기

p.stop() # Playwright 종료

soup = BeautifulSoup(content, "html.parser")

jobs = soup.find_all("div", class_="JobCard_container__zQcZs")

jobs_db = []

for job in jobs:
    link = f"https://www.wanted.co.kr{job.find('a')['href']}"
    title = job.find("strong", class_="JobCard_title___kfvj").text
    company_name = job.find("span", class_="CompanyNameWithLocationPeriod_CompanyNameWithLocationPeriod__company__ByVLu").text
    reward_tag = job.find("span", class_="JobCard_reward__oCSIQ")

    if reward_tag is None:
            continue

    job = {
        "title": title,
        "company_name": company_name,
        "reward": reward_tag.text,
        "link": link,
    }
    jobs_db.append(job)

save_to_file("python", jobs_db)




# Positional Arguments : 순서로 값 전달
# page.goto("https://google.com")
# "https://google.com" 이 첫 번째 인자 자리에 들어감

# Keyword Arguments : 이름으로 값 전달
# page.screenshot(path="screenshot.png")
# path 라는 이름으로 값 전달, 순서 상관없음