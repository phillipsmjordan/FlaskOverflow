import flask
from flask import Flask, request, render_template, jsonify
app = Flask(__name__)
app.debug = True

from httplib import HTTPException
from operator import attrgetter
from Models import Question, Answer
from Database import db
import QuestionMatcher as matcher


@app.route('/', methods=['GET'])
def index():
    questions = Question.query.all()
    questions = sorted(questions, key=attrgetter('timestamp'), reverse=True)

    top_answers = {}
    answer_count = {}
    for question in questions:
        answers = Answer.query.filter_by(question_id=question.id).all()
        answer_count[question.id] = len(answers)
        if len(answers) > 0:
            top_answer = max(answers, key=attrgetter('upvote_count'))
            top_answers[question.id] = top_answer
    return render_template('index.html', questions=questions, top_answers=top_answers, answer_count=answer_count)


@app.route('/question/<int:question_id>', methods=['GET'])
def question(question_id):
    question = Question.query.get(question_id)
    question.views += 1
    db.session.commit()
    answers = Answer.query.filter_by(question_id=question.id).all()
    answers = sorted(answers, key=attrgetter('upvote_count'), reverse=True)
    return render_template('question.html', question=question, answers=answers)


@app.route('/ask', methods=['GET', 'POST'])
def ask():
    if request.method == 'POST':
        subject = request.form['question_subject']
        body = request.form['question_body']
        question = Question(subject, body)
        db.session.add(question)
        db.session.commit()
        return flask.redirect('/')
    else:
        return render_template('ask.html')


@app.route('/answer/<int:question_id>', methods=['POST'])
def answer(question_id):
    question = Question.query.get(question_id)
    body = request.form['answer_body']
    answer = Answer(question.id, body)
    db.session.add(answer)
    db.session.commit()
    return flask.redirect('/question/' + str(question_id))


@app.route('/api/question/<int:question_id>', methods=['GET'])
def api_question(question_id):
    question = Question.query.get(question_id)
    return jsonify({"question_id":question.id, "subject":question.subject})


@app.route('/api/upvote/<int:answer_id>', methods=['GET', 'POST'])
def upvote(answer_id):
    answer = Answer.query.get(answer_id)
    if answer is None:
        return make_json_error(500)

    if request.method == 'POST':
        answer.upvote_count += 1
        db.session.commit()
        return jsonify({'success': True, 'new_total': answer.upvote_count}), 200, {'ContentType': 'application/json'}
    else:
        return jsonify(upvote_count=answer.upvote_count)


@app.route('/api/matchscore', methods=['GET'])
def get_match_score():
    subject = request.args.get('subject')
    match_score = matcher.get_match_scores(subject)
    return jsonify({"matchscore":match_score})


@app.route('/reset', methods=['GET'])
def reset():
    Question.query.delete()
    Answer.query.delete()
    db.session.commit()
    return flask.redirect('/')


def make_json_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code
                            if isinstance(ex, HTTPException)
                            else 500)
    return response


if __name__ == '__main__':
    app.run()
    # db.create_all()
