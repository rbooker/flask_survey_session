from flask import Flask, request, render_template, redirect, flash, session
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'


@app.route('/')
def welcome_page():
    return render_template('start_page.html', survey=satisfaction_survey)

@app.route('/start', methods=["POST"])
def start_survey():
    session["responses"] = []
    return redirect('/questions/0')

@app.route("/questions/<int:qid>")
def display_question(qid):

    responses = session.get("responses")

    #if there are no responses yet, send them back to the start of the survey
    if (responses is None):
        return redirect("/")
    #if the length of the responses variable is the same as that of the number of
    #questions, they've finished the survey and should be redirected to the 'complete'
    #page
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/done")

    #if they're trying to questions out of order, flash a message and redirect them
    #to the correct page
    if (len(responses) != qid):
        flash("I can't let you do that, Dave. You must answer the questions in order")
        return redirect(f"/questions/{len(responses)}")

    #otherwise, render the question
    next_question = satisfaction_survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=next_question)

@app.route("/answer", methods=["POST"])
def get_response():

    #get the answer
    user_response = request.form['answer']

    #add the answer to the response list
    responses = session["responses"]
    responses.append(user_response)
    session["responses"] = responses

    #if the length of the responses variable is the same as that of the number of
    #questions, they've finished the survey and should be redirected to the 'complete'
    #page
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/done")

    else:
        return redirect(f"/questions/{len(responses)}")

@app.route("/done")
def complete():
    return render_template("thanks.html", survey=satisfaction_survey)