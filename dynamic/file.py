import csv

def save_to_file(file_name, jobs_db):
    file = open(
        f"{file_name}.csv",         # 파일명 (경로 지정 안하면 현재 실행 파일 위치에 생성)
        "w",                # 모드: w(쓰기), r(읽기), a(이어쓰기)
        encoding="utf-8",   # 인코딩: utf-8 지정 안하면 한글 깨질 수 있음
        newline=""          # csv 저장 시 행마다 빈 줄 생기는 것 방지 (Windows 전용 이슈)
    )

    writer = csv.writer(file) # csv writer 객체 생성

    writer.writerow(["Title", "Company", "Reward", "Link",]) # 헤더(컬럼명) 작성

    for job in jobs_db:
        writer.writerow(job.values()) # 딕셔너리의 값만 추출해서 한 행씩 작성
        # job.values() -> dict_values(['title값', 'company값', 'reward값', 'link값'])
    file.close()