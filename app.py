from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = '  yomommasofatshebendslight'

@app.route('/')
def home():
    return render_template('home.html', name='MoonMan')

@app.route('/your_url', methods=['GET', 'POST'])
def your_url():
    if request.method == 'POST':
        urls = {}

        if os.path.exists('urls.json'):
            with open('urls.json') as urls_file:
                urls = json.load(urls_file)

        if request.form['code'] in urls.keys():
            flash('Short name is already in use. Please try another one.')
            return redirect(url_for('home'))
        
        if 'url' in request.form.keys():
           urls[request.form['code']] = {'url': request.form['url']}
        else: 
            f = request.files['file']
            full_name = request.form['code'] + secure_filename(f.filename)
            # print(os.cwd())
            f.save(os.path.join(f'{os.getcwd()}/files', full_name))
            urls[request.form['code']] = {'file': full_name}

        with open('urls.json', 'w') as url_file:
            json.dump(urls, url_file)
        return render_template('your_url.html', code=request.form['code'])
    else: return redirect(url_for('home'))


