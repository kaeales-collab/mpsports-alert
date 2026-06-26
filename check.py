import os
import re
import requests
from bs4 import BeautifulSoup

URL = "https://www.mpsports.or.kr/base/education/info/list?siteCode=&cat1=2&cat2=&cat3=&searchCategoryType=2&menuLevel=2&menuNo=11&searchStatus=&instructorNo=&target=%EC%84%B1%EC%9D%B8&searchStartDate=&searchEndDate=&educationStartTime=&educationEndTime=&searchType=total&searchWord=%EC%B4%88%EA%B8%89"

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers, timeout=20)
r.raise_for_status()

soup = BeautifulSoup(r.text, "html.parser")

tables = soup.find_all("table")

msg = []

for table in tables:

    data = {}

    for td in table.find_all("td"):
        key = td.get("data-th")
        if key:
            data[key] = td.get_text(strip=True)

    people = data.get("신청자/정원", "")

    if people and people != "20/20":

        msg.append(
            f"📌 {data.get('교육명','')}\n"
            f"🗓 {data.get('요일','')}\n"
            f"🕒 {data.get('강습시간','')}\n"
            f"👥 {people}"
        )

if msg:

    text = "🎉 빈자리가 생겼습니다.\n\n" + "\n\n-----------------\n\n".join(msg)

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=20
    )
