import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from utils.smbc import smbc_balance

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


def main():
    balance_inquiry()
    scheduler = BlockingScheduler(timezone="Asia/Tokyo")
    scheduler.add_job(
        func=balance_inquiry,
        trigger="interval",
        minutes=1
    )
    scheduler.start()


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        exit()