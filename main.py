from flask import Flask, render_template, request, redirect, url_for
import yaml
import random

app = Flask(__name__)

with open('meme.yml', 'r', encoding='utf-8') as f:
    memes = yaml.safe_load(f)

meme_names = list(memes.keys())

@app.route('/')
def index():
    correct_meme = random.choice(meme_names)

    if len(meme_names) < 9:
        return "В файле meme.yml должно быть минимум 9 мемов!", 500

    other_memes = random.sample([m for m in meme_names if m != correct_meme], 8)
    options = [correct_meme] + other_memes
    random.shuffle(options)

    next_url = request.args.get('next')

    return render_template('index.html',
                           correct=correct_meme,
                           options=options,
                           memes=memes,
                           next_url=next_url)

@app.route('/check', methods=['POST'])
def check():
    selected = request.form.get('meme')
    correct = request.form.get('correct')
    next_url = request.form.get('next_url')

    if selected == correct:
        if next_url:
            return redirect(next_url)
        else:
            return render_template('success.html')
    else:
        return redirect(url_for('fail'))

@app.route('/fail')
def fail():
    cat_url = url_for('static', filename='cat.jpg')
    return render_template('fail.html', cat_url=cat_url)

if __name__ == '__main__':
    app.run(debug=True)
