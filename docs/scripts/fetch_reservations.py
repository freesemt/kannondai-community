import os
import requests
from bs4 import BeautifulSoup

LOGIN_URL = "https://www.c-sqr.net/login"
SCHEDULE_URL = "https://www.c-sqr.net/events?date=today"

# ログイン情報を環境変数から取得
ACCOUNT = os.environ.get("CSQR_ACCOUNT")
PASSWORD = os.environ.get("CSQR_PASSWORD")

if not ACCOUNT or not PASSWORD:
    raise ValueError("環境変数 CSQR_ACCOUNT または CSQR_PASSWORD が設定されていません。")

with requests.Session() as session:
    # 1. ログインページを取得してCSRFトークンを取得
    resp = session.get(LOGIN_URL)
    soup = BeautifulSoup(resp.text, "html.parser")
    token = soup.find("input", {"name": "_token"}).get("value")

    # 2. ログインフォーム送信
    payload = {
        "account": ACCOUNT,
        "password": PASSWORD,
        "_token": token,
        "remember": "on"
    }
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": LOGIN_URL
    }
    login_resp = session.post(LOGIN_URL, data=payload, headers=headers)

    # 3. ログイン成功判定
    soup = BeautifulSoup(login_resp.text, "html.parser")
    title = soup.title.string if soup.title else ""
    if "ログイン" in title:
        print("ログイン失敗")
        # レスポンス内容をファイルに保存して確認
        with open("login_failed.html", "w", encoding="utf-8") as f:
            f.write(login_resp.text)
        print("レスポンス内容を login_failed.html に保存しました。")
    else:
        print("ログイン成功")

        # スケジュールページへアクセス
        resp = session.get(SCHEDULE_URL)
        soup = BeautifulSoup(resp.text, "html.parser")

        # hrefが"ics"で終わるaタグを探す
        ical_link = soup.find("a", href=lambda x: x and x.endswith("/ics"))
        if ical_link:
            ical_url = ical_link["href"]
            if not ical_url.startswith("http"):
                ical_url = "https://www.c-sqr.net" + ical_url
            print("iCal URL:", ical_url)

            ical_resp = session.get(ical_url)
            ical_resp.raise_for_status()
            with open("events.ics", "wb") as f:
                f.write(ical_resp.content)
            print("iCalファイルを events.ics として保存しました。")
        else:
            print("iCal出力リンクが見つかりませんでした。")