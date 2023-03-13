import yaml

with open("data/config.yaml", "r") as f:
    config = yaml.safe_load(f)

SMBC: dict = config["SMBC"]

MUFG: dict = config["MUFG"]

BARK: dict = config["BARK"]