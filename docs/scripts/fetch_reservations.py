import os
import requests
from bs4 import BeautifulSoup
import argparse
import re
import json
from datetime import datetime

LOGIN_URL = "https://www.c-sqr.net/login"
SCHEDULE_URL = "https://www.c-sqr.net/events?date=today"

def fetch_ics_file(filename="docs/scripts/events.ics", debug=False):
    """iCalファイルを取得して保存する"""
    account = os.environ.get("CSQR_ACCOUNT")
    password = os.environ.get("CSQR_PASSWORD")
    if not account or not password:
        raise ValueError("環境変数 CSQR_ACCOUNT または CSQR_PASSWORD が設定されていません。")

    with requests.Session() as session:
        # 1. ログインページを取得してCSRFトークンを取得
        resp = session.get(LOGIN_URL)
        soup = BeautifulSoup(resp.text, "html.parser")
        token = soup.find("input", {"name": "_token"}).get("value")

        # 2. ログインフォーム送信
        payload = {
            "account": account,
            "password": password,
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
            if debug:
                with open("login_failed.html", "w", encoding="utf-8") as f:
                    f.write(login_resp.text)
                print("レスポンス内容を login_failed.html に保存しました。")
            return False
        else:
            print("ログイン成功")

            # スケジュールページへアクセス
            resp = session.get(SCHEDULE_URL)
            soup = BeautifulSoup(resp.text, "html.parser")

            # デバッグ用: スケジュールページのHTMLを保存
            if debug:
                with open("schedule_page.html", "w", encoding="utf-8") as f:
                    f.write(resp.text)
                print("スケジュールページのHTMLを schedule_page.html に保存しました。")

            # 「iCal出力」ページへ遷移
            ical_page_link = soup.find("a", href=lambda x: x and "/events/ics" in x)
            if not ical_page_link:
                print("iCal出力ページへのリンクが見つかりませんでした。")
                return False
            ical_page_url = ical_page_link["href"]
            if not ical_page_url.startswith("http"):
                ical_page_url = "https://www.c-sqr.net" + ical_page_url
            print("iCal出力ページURL:", ical_page_url)

            # iCal出力ページにアクセス
            ical_page_resp = session.get(ical_page_url)
            ical_page_resp.raise_for_status()
            if debug:
                with open("ical_page.html", "w", encoding="utf-8") as f:
                    f.write(ical_page_resp.text)
                print("iCal出力ページのHTMLを ical_page.html に保存しました。")

            ical_page_soup = BeautifulSoup(ical_page_resp.text, "html.parser")
            ics_input = ical_page_soup.find("input", {"id": "ics_url"})
            if not ics_input:
                print("icsファイルのURLが見つかりませんでした。")
                return False
            ics_url = ics_input.get("value")
            print("icsファイルURL:", ics_url)

            # icsファイルをダウンロード
            ical_resp = session.get(ics_url)
            ical_resp.raise_for_status()
            if not ical_resp.content.startswith(b"BEGIN:VCALENDAR"):
                print("警告: 取得したファイルはics形式ではありません。内容を確認してください。")
                if debug:
                    with open("invalid_ics_response.html", "wb") as f:
                        f.write(ical_resp.content)
                return False
            with open(filename, "wb") as f:
                f.write(ical_resp.content)
            print(f"iCalファイルを {filename} として保存しました。")
            return True

def ics_to_custom_json(ics_path="docs/scripts/events.ics", json_path="docs/scripts/calendar-reservations.json"):
    """iCalファイルをJSON形式に変換して保存する"""
    events_by_date = {}

    def parse_dt(dtstr):
        # 例: 20250126T093000 → "2025-01-26", "09:30"
        m = re.match(r"(\d{4})(\d{2})(\d{2})T?(\d{2})?(\d{2})?", dtstr)
        if m:
            y, mo, d, h, mi = m.groups()
            date = f"{y}-{mo}-{d}"
            time = f"{h}:{mi}" if h and mi else None
            return date, time
        return None, None

    with open(ics_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    event = {}
    for line in lines:
        line = line.strip()
        if line == "BEGIN:VEVENT":
            event = {}
        elif line == "END:VEVENT":
            # 必要な情報だけ抽出
            summary = event.get("SUMMARY", "")
            dtstart = event.get("DTSTART;TZID=Japan") or event.get("DTSTART;VALUE=DATE") or event.get("DTSTART")
            dtend = event.get("DTEND;TZID=Japan") or event.get("DTEND;VALUE=DATE") or event.get("DTEND")
            if dtstart and dtend and summary:
                date, start = parse_dt(dtstart)
                _, end = parse_dt(dtend)
                if date:
                    # 時間範囲がない場合（終日イベント）
                    time_range = f"{start} - {end}" if start and end else "終日"
                    if date not in events_by_date:
                        events_by_date[date] = {}
                    # 現在の形式に合わせて保存
                    events_by_date[date][time_range] = summary
        else:
            if ":" in line:
                key, value = line.split(":", 1)
                event[key] = value

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(events_by_date, f, ensure_ascii=False, indent=2)
    print(f"カレンダー用予約データを {json_path} に保存しました。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="iCal取得・変換スクリプト")
    parser.add_argument("--fetch", action="store_true", help="iCalファイルを取得する")
    parser.add_argument("--convert", action="store_true", help="icsファイルをJSONに変換する")
    args = parser.parse_args()

    if args.fetch:
        fetch_ics_file()
    if args.convert:
        ics_to_custom_json()
    if not args.fetch and not args.convert:
        # デフォルトは両方実行
        if fetch_ics_file():
            ics_to_custom_json()