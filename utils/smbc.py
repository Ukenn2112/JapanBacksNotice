import logging
import os.path
import re

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from playwright.sync_api import sync_playwright
from requests import post

from .bark import send_notice
from .config import SMBC
from .sqlitedb import sql

jsessionid = None
token = None
now_balance = None


def smbc_login():
    """SMBC 登录"""
    global jsessionid, token

    logging.info("[SMBC] 执行登录")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto("https://direct.smbc.co.jp/aib/aibgsjsw3k12.jsp")
            page.fill("input[name=branchNo]", str(SMBC["branchNo"]))
            page.fill("input[name=accountNo]", str(SMBC["accountNo"]))
            page.fill("input[name=cdPassword]", str(SMBC["password"]))
            page.click("a[class='btn-type01 -orange01 js-login-submit']")
            page.click("a[class='card-box01 -noPadding -overflow01 -shadow01']")
            cookies = page.context.cookies()
            jsessionid = [c for c in cookies if c["name"] == "JSESSIONID"][0]["value"]
            token = page.query_selector_all('//input[@name="_TOKEN"]')[0].get_attribute(
                "value"
            )
            browser.close()
    except Exception as e:
        logging.error(f"[SMBC] 登录失败: {e}")
        return None


def smbc_balance():
    """SMBC 余额查询"""
    if SMBC is None:
        return
    global now_balance

    if now_balance is None:
        now_balance = sql.select("SMBC")
    if not jsessionid or not token:
        smbc_login()
    logging.info("[SMBC] 执行余额查询")
    data = post(
        "https://direct3.smbc.co.jp/ib/ajax/accountinquiry/AIFCDTLAjaxkikannshokai.smbc",
        headers={
            "Cookie": f"JSESSIONID={jsessionid}",
        },
        params={
            "_TOKEN": token,
            "_FORMID": "AIFCDTL",
        },
    ).json()
    if data["success"] == "false":
        logging.warning("[SMBC] 登录失效，重新登录")
        smbc_login()
        return smbc_balance()
    if now_balance == "":
        sql.insert(
            "SMBC",
            data["response"]["meisai"][0]["amount"],
            data["response"]["meisai"][0]["torihikigobalance"],
            data["response"]["meisai"][0]["comment"],
        )
        now_balance = data["response"]["meisai"][0]["torihikigobalance"]
    elif data["response"]["meisai"][0]["torihikigobalance"] != now_balance:
        for m in data["response"]["meisai"]:
            if m["torihikigobalance"] == now_balance:
                break
            send_notice(
                "SMBC 余额变动",
                f"金额: {m['amount']} → {get_comment_to_mail(m['comment']) or m['comment']}\n余额: {m['torihikigobalance']}",
                m["amount"].replace("円", "").replace(",", "").strip(),
                "SMBC",
                "https://article.biliimg.com/bfs/article/e5461b8a66674e57306a3f0be600a4eb14e59d6b.png",
            )
            sql.insert("SMBC", m["amount"], m["torihikigobalance"], m["comment"])
        now_balance = data["response"]["meisai"][0]["torihikigobalance"]
    logging.info(f"[SMBC] 余额: {now_balance}")
    return now_balance


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_comment_to_mail(comment_id):
    creds = None

    if os.path.exists("data/token.json"):
        creds = Credentials.from_authorized_user_file("data/token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "data/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=8080)
        with open("data/token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    results = (
        service.users()
        .messages()
        .list(userId="me", labelIds=[SMBC["gmail_labelId"]], maxResults=10)
        .execute()
    )
    messages = results.get("messages", [])

    if not messages:
        return None
    else:
        for message in messages:
            msg = (
                service.users().messages().get(userId="me", id=message["id"]).execute()
            )
            match = re.search(
                r"利用先\s*：\s*(.*?)\s*◇.*?承認番号：\s*(\d+)", msg["snippet"]
            )
            if match:
                utilization_location: str = match.group(1)
                approval_number = "V" + match.group(2)
                if approval_number == comment_id:
                    return utilization_location
    return None