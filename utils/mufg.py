import logging

from lxml.etree import HTML
from playwright.sync_api import sync_playwright
from requests import post

from .bark import send_notice
from .config import MUFG
from .sqlitedb import sql

iwInfo = None
now_balance = None

def mufg_login():
    """MUFG 银行登录"""
    global iwInfo

    logging.info("[MUFG] 执行登录")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://entry11.bk.mufg.jp/ibg/dfw/APLIN/loginib/login?_TRANID=AG004_001")
        page.fill("input[name=TENBAN]", str(MUFG["branchNo"]))
        page.fill("input[name=KOUZA_NO]", str(MUFG["accountNo"]))
        page.fill("input[name=PASSWORD]", str(MUFG["password"]))
        page.click("button[onclick='gotoPageFromAA011(); return false;']")
        cookies = page.context.cookies()
        iwInfo = [c for c in cookies if c["name"] == "IW_INFO"][0]["value"]
        browser.close()


def mufg_balance():
    """MUFG 银行余额查询"""
    if MUFG is None: return
    global now_balance

    if now_balance is None:
        now_balance = sql.select("MUFG")
    if not iwInfo: mufg_login()
    r = post(
        "https://direct11.bk.mufg.jp/ib/dfw/APL/bnkib/banking",
        headers={
            "Cookie": f"IW_INFO={iwInfo}",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "_TRANID": "AZ091_999",
        }
    )
    html = HTML(r.text)
    error = html.xpath("//section[@class='page-error']")
    if error:
        logging.warning("[MUFG] 登录失效，重新登录")
        mufg_login()
        return mufg_balance()
    cookies = r.headers["Set-Cookie"]
    balance = html.xpath("//span[@class='total-amount-unmask hide']/text()")[0]
    sendts = html.xpath("//input[@name='_SENDTS']/@value")[0]

    if balance != now_balance:
        b = post(
            "https://direct11.bk.mufg.jp/ib/dfw/APL/bnkib/banking",
            headers={
                "Cookie": f"{cookies}; IW_INFO={iwInfo}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={
                "_PAGEID": "AD001",
                "_SENDTS": sendts,
                "_TRANID": "AD001_066",
                "_SUBINDEX": -1,
                "_WINID": "root",
                "SEEOTHERS": "false",
            }
        )
        b_html = HTML(b.text)
        error = b_html.xpath("//section[@class='page-error']")
        if error: return

        meisai_data = b_html.xpath("//table[@class='data yen_nyushutsukin_001']/tbody/tr")[-1]
        if manage_to := meisai_data.xpath("./td[@class='manage number'][1]/strong/text()"):
            manage_num = "-" + manage_to[0]
        elif manage_from := meisai_data.xpath("./td[@class='manage number'][2]/strong/text()"):
            manage_num = manage_from[0]
        transaction = meisai_data.xpath("./td[@class='transaction']/text()")[0]

        send_notice(
            "MUFG 余额变动",
           f"金额: {manage_num}円 → {transaction}\n余额: {balance}", manage_num.replace(",", "").strip(),
           "MUFG", "https://article.biliimg.com/bfs/article/2db82e3d8bae1b9d1cf2cca3a437b02dcf5564d4.png"
        )
        sql.insert("MUFG", manage_num, balance, transaction)
        now_balance = balance
    logging.info(f"[MUFG] 余额: {now_balance}")
    return now_balance
