import logging

from playwright.sync_api import sync_playwright
from requests import post

from .bark import send_notice
from .config import SMBC

jsessionid = None
token = None
now_balance = None

def smbc_login():
    """SMBC 登录"""
    global jsessionid, token

    logging.info("[SMBC] 执行登录")
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
        token = page.query_selector_all('//input[@name="_TOKEN"]')[0].get_attribute("value")
        browser.close()


def smbc_balance():
    """SMBC 余额查询"""
    global now_balance

    if not jsessionid or not token: smbc_login()
    logging.info("[SMBC] 执行余额查询")
    data = post(
        "https://direct3.smbc.co.jp/ib/ajax/accountinquiry/AIFCDTLAjaxkikannshokai.smbc",
        headers={
            "Cookie": f"JSESSIONID={jsessionid}",
        },
        params={
            "_TOKEN": token,
            "_FORMID": "AIFCDTL",
        }
    ).json()
    if data["success"] == "false":
        logging.warning("[SMBC] 登录失效，重新登录")
        smbc_login()
        return smbc_balance()
    if data["response"]["meisai"][0]["torihikigobalance"] != now_balance:
        for m in data["response"]["meisai"]:
            if m["torihikigobalance"] == now_balance:
                break
            send_notice(
                "SMBC 余额变动",
               f"金额: {m['amount']} → {m['comment']}\n余额: {m['torihikigobalance']}", m["amount"].replace("円", "").replace(",", "").strip(),
                "SMBC", "https://article.biliimg.com/bfs/article/e5461b8a66674e57306a3f0be600a4eb14e59d6b.png"
            )
        now_balance = data["response"]["meisai"][0]["torihikigobalance"]
    logging.info(f"[SMBC] 余额: {now_balance}")
    return now_balance
