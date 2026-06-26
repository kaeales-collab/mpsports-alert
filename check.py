import requests
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.getenv("BOT_TOKEN") or "여기에_봇토큰"
CHAT_ID = os.getenv("CHAT_ID") or "여기에_채팅ID"

URL = "https://www.mpsports.or.kr/base/education/info/list?siteCode=&cat1=2&cat2=&cat3=&searchCategoryType=2&menuLevel=2&menuNo=11&searchStatus=&instructorNo=&target=%EC%84%B1%EC%9D%B8&searchStartDate=&searchEndDate=&educationStartTime=&educationEndTime=&searchType=total&searchWord=%EC%B4%88%EA%B8%89"

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(URL, headers=headers, timeout=20).text
soup = BeautifulSoup(html, "html.parser")

msg = []

for table in soup.find_all("table"):

    data = {}

    for td in table.find_all("td"):
        key = td.get("data-th")
        if key:
            data[key] = td.get_text(" ", strip=True)

    people = data.get("신청자/정원", "")

    if not people:
        continue

    if people.strip() != "20/20":

        day = data.get("요일", "")
        time = data.get("강습시간", "")

        msg.append(
            f"🟢 자리 발생\n"
            f"요일 : {day}\n"
            f"시간 : {time}\n"
            f"현재 : {people}"
        )

if msg:

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": "\n\n----------------------\n\n".join(msg)
        },
        timeout=20
    )

else:
    print("빈자리 없음")
