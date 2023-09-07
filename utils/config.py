import yaml

with open("data/config.yaml", "r") as f:
    config = yaml.safe_load(f)

SMBC: dict = config["SMBC"] if "SMBC" in config else None

MUFG: dict = config["MUFG"] if "MUFG" in config else None

BARK: dict = config["BARK"]