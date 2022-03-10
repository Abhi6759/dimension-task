import datetime
import pymongo

import pandas as pd
from flask import render_template, request, redirect, url_for,flash

from main import app, mongo

db = mongo.db.dimensions

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("home.html")

# to convert date string to a date
def datecovertor(string_date):
    date = string_date.split('-')
    final_date = datetime.datetime(year=int(date[0]), month=int(date[1]), day=int(date[2]))
    return final_date

# to create a model for the database
def create_dict(i, data):
    dict1 = {
        'image_name': data['image_name'][i],
        'objects_detected': (data['objects_detected'][i]).split(','),
        'timestamp': datecovertor((data['timestamp'][i]))
    }
    return dict1

# to validate if the data exists  if it exists it just updates
@app.route('/upload2', methods=['GET', 'POST'])
def upload2():
    if request.method == 'POST':
        csv_file = request.files['file']
        data = pd.read_csv(csv_file)
        for i in range(len(data)):
            single_data = create_dict(i, data)
            db.update_one({'image_name': single_data['image_name']},
                          {"$set": {'objects_detected': single_data['objects_detected'],
                                    'timestamp': single_data['timestamp']}}
                          , upsert=True)

        return redirect(url_for('home'))

# to view to scan images
@app.route('/view', methods=['GET', 'POST'])
def view():
    if request.method == 'POST':
        start = datecovertor(request.form.get('start'))
        end = datecovertor(request.form.get('end'))
        data2 = db.find
        data = list(db.find({"timestamp": {"$gte": start, "$lte": end}}, {'_id': 0, 'timestamp': 0}))
        if len(data) == 0:
            flash('Sorry NO scans found in these dates')
            data = None
        return render_template("home.html", data=data)


