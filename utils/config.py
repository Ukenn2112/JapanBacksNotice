import yaml

with open("data/config.yaml", "r") as f:
    config = yaml.safe_load(f)

SMBC: dict = config["SMBC"]

BARK: dict = config["BARK"]