from flask import Flask, render_template, request # Flask 웹 프레임워크 import
from wanted_scaper import WantedScraper # 같은 폴더의 wanted_scaper.py에서 클래스 import

app = Flask("JobScrapper") # Flask 앱 생성

# @app.route() -> URL과 함수를 연결하는 데코레이터
@app.route("/") # http://127.0.0.1:5000/ 접속 시 실행
def home():
    return render_template("home.html") # templates/home.html 렌더링

@app.route("/search")  # http://127.0.0.1:5000/search 접속 시 실행
def search():
    # request.args.get() -> URL 쿼리스트링에서 값 가져오기
    # /search?keyword=python -> keyword = "python"
    keyword = request.args.get("keyword")
    scraper = WantedScraper([keyword])  # 키워드를 리스트로 감싸서 스크래퍼 생성
    jobs = scraper.scrape() # 스크랩 실행 후 결과 반환
    # render_template() -> HTML 파일에 변수 전달하며 렌더링
    return render_template("search.html", keyword=keyword, jobs=jobs)

app.run(debug=True) # debug=True -> 코드 수정 시 서버 자동 재시작