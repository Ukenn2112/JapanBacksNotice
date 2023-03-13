from requests import post

from .config import BARK


def send_notice(title: str, content: str, amount: str, bank: str, bank_icon: str):
    """baka推送
    title: 标题
    content: 内容
    amount: 金额
    bank: 银行
    bank_icon: 银行图标"""
    json= {
        "title": title,
        "body": content,
        "group": bank,
        "sound": "bell",
        "level": "timeSensitive",
        "icon": bank_icon,
        "url": f"shortcuts://run-shortcut?name=%E5%BF%AB%E6%8D%B7%E8%AE%B0%E8%B4%A6&input={amount}"
    }
    return post(BARK["server"], json=json)
