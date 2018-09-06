import json
import os.path


def store_rates(rates, path):
    date = rates["date"]  # TODO: handle the keyerror exception somewhere
    filename = "%s_fixer_rates.json" % date
    filepath = os.path.join(path, filename)

    with open(filepath, "w") as f:
        f.write(json.dumps(rates))


def retrieve_rates(date, path):
    filename = "%s_fixer_rates.json" % date
    filepath = os.path.join(path, filename)

    with open(filepath, "r") as f:
        rates = json.load(f)

    return rates
