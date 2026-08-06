# requests -> HTTP 요청 라이브러리(웹페이지 가져오기)
import requests
# BeautifulSoup -> HTML 파싱 라이브러리(데이터 추출)
from bs4 import BeautifulSoup

url = "https://weworkremotely.com/categories/remote-full-stack-programming-jobs"

# get() -> URL에 GET 요청 보내기, response -> 서버 응답 객체(status_code, content 등 포함)
response = requests.get(url)

# soup -> HTML을 탐색 가능한 객체로 변환
soup = BeautifulSoup(
    response.content, # 응답 HTML 바이트 데이터
    "html.parser", # Python 내장 HTML 파서 사용
    )

# find() -> 조건에 맞는 첫 번째 태그 반환
# find_all() -> 조건에 맞는 모든 태그 리스트 반환
# 메서드 체이닝으로 section 안의 li 전부 가져옴
jobs = soup.find( 
    "section",
      class_="jobs",
    ).find_all("li")

all_jobs = []

for job in jobs:
    title_tag = job.find("span", class_="new-listing__header__title__text")
    region_tag = job.find("p", class_="new-listing__company-headquarters")
    company_tag = job.find("p", class_="new-listing__company-name")
    url_tag = job.find("a", class_="listing-link--unlocked")

    if title_tag is None or region_tag is None or company_tag is None or url_tag is None:
        continue

    title = title_tag.text
    region = region_tag.text
    company = company_tag.text
    # 태그의 속성값 가져오기
    # tag["속성명"] 형태로 접근
    # tag.text는 태그 안 텍스트, tag["href"]는 태그 속성값
    url = url_tag["href"] 

    # 각 job 데이터를 딕셔너리로 구조화
    # all_jobs 리스트에 딕셔너리를 하나씩 추가
    job_data = {
        "title": title,
        "region": region,
        "company": company,
        "url": f"https://weworkremotely.com{url}",
    }
    all_jobs.append(job_data)

print(all_jobs)

# 딕셔너리 vs 리스트

# 리스트 [] - 순서 있는 데이터 모음, 인덱스(숫자)로 접근
# all_jobs = ["nico", "dean", "lynn"]
# all_jobs[0]  -> "nico"

# 딕셔너리 {} - 키:값 쌍으로 이루어진 데이터, 키(이름)로 접근
# job_data = {"title": "Developer", "region": "Seoul"}
# job_data["title"]  -> "Developer"


# # with : 리소스를 안전하게 사용하고 자동으로 닫아주는 키워드
# with open("jobs.txt", "w", encoding="utf-8") as f:  # jobs.txt 파일을 쓰기 모드로 열기, 파일 객체를 f로 사용 (블록 끝나면 자동 닫힘)
#     for job in jobs: #  jobs 리스트 순회
#         f.write(str(job) + "\n") #  job을 문자열로 변환 후 줄바꿈과 함께 파일에 작성
