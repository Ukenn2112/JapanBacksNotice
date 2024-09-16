import logging

# from apscheduler.schedulers.blocking import BlockingScheduler
import time

from utils.mufg import mufg_balance
from utils.smbc import smbc_balance
from utils.sqlitedb import sql

logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(
    format="[%(levelname)s] %(asctime)s: %(message)s",
    handlers=[
        logging.FileHandler("data/run.log", encoding="UTF-8"),
        logging.StreamHandler(),
    ],
)

def balance_inquiry():
    smbc_balance()
    mufg_balance()

def main():
    sql.create_db()
    while True:
        balance_inquiry()
        time.sleep(60)
    # scheduler = BlockingScheduler(timezone="Asia/Tokyo")
    # scheduler.add_job(
    #     func=balance_inquiry,
    #     trigger="interval",
    #     minutes=1
    # )
    # scheduler.start()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        exit()