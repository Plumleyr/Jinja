from flask import Flask, request, render_template

from stories import Story

app = Flask(__name__)

app.config['SECRET_KEY'] = "zzz"

Stories = {'On_the_road' : Story(["adjective", "noun"],"I hate {adjective} {noun} drivers"), 'Slay_the_dragon' : Story(["noun", "action_verb","adjective"], '{noun} {action_verb} to slay a {adjective} dragon')}

ans = {}

# selected_story = ''

@app.route('/')
def show_select_story():
    return render_template('select.html', Stories = Stories)

@app.route('/form', methods=["GET", "POST"])
def show_form():
    global selected_story

    if request.method == 'POST':
        selected_story = request.form["selected_story"]
    return render_template("form.html", prompts = Stories[selected_story].prompts)

def get_answers(selected_story):
    for prompt in Stories[selected_story].prompts:
        ans[prompt] = request.args.get(prompt)

@app.route('/story', methods=["POST"])
def show_story():
    get_answers(selected_story)
    generated = Stories[selected_story].generate(request.form)
    return render_template("madlibs.html", generated = generated)