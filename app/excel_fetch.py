import pandas
from flask import jsonify

def test():
    data = pandas.read_excel("app\labels.xlsx")
    data_json = data.to_json(orient="records")
    return jsonify(data_json)
