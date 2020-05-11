'''This is the main flask python file'''
from flask import Flask, Response,request, render_template,redirect,url_for
from werkzeug.utils import secure_filename
import os
from predict import Predictor
import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
import string
import datetime
import _pickle as cPickle
import joblib
app = Flask(__name__)

def process_text(text):
    '''
    Yapılacaklar:
    1. Noktalama işaretleri silinecek.
    2. Stopword'ler silinecek.
    3. Temizlenmiş kelimeler clean_words döndürülecek.
    '''

    # 1
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)

    # 2
    clean_words = [word for word in nopunc.split() if word.lower() not in stopwords.words('turkish')]

    # 3
    return clean_words



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/completed')
def complete():
    return render_template('complete.html')


@app.route('/progress')
def progress():
    return Response(FPB.progress(example_generator()), mimetype='text/event-stream')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join("./static/files", secure_filename(f.filename)))
        pred = Predictor(os.path.join("./static/files", secure_filename(f.filename)),os.path.join("./static/output", secure_filename(f.filename))).predictor_func()
        return render_template('complete.html',location=os.path.join("./static/output", secure_filename(f.filename)))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
