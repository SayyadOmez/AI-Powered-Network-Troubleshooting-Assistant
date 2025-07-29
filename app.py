from flask import Flask, render_template, request, send_file, session, redirect, url_for
from rag_retriever import analyze_with_rag, handle_follow_up
from markupsafe import Markup
import os

app = Flask(__name__)
app.secret_key = 'super_secret_key'

@app.route('/', methods=['GET', 'POST'])
def index():
    session['chat_history'] = []  # Reset on GET
    log_data = ''
    analysis_result = ''
    reference_docs = ''
    log_category = ''

    if request.method == 'POST':
        log_data = request.form['logs']
        with open("received_log.txt", "w") as f:
            f.write(log_data)

        analysis_result_raw, reference_docs, log_category = analyze_with_rag(log_data)
        analysis_result = format_to_bullets(analysis_result_raw)

        session['log_data'] = log_data
        session['analysis_result'] = analysis_result
        session['chat_history'] = [{'role': 'assistant', 'content': analysis_result}]

        with open("analysis_result.txt", "w") as f:
            f.write(analysis_result_raw)

    return render_template('index.html',
                           log_data=log_data,
                           analysis_result=analysis_result,
                           reference_docs=reference_docs,
                           log_category=log_category,
                           chat_history=session.get('chat_history', []))

@app.route('/followup', methods=['POST'])
def followup():
    follow_up_question = request.form['followup_question']
    log_data = session.get('log_data', '')
    initial_response = session.get('analysis_result', '')

    follow_up_answer_raw = handle_follow_up(log_data, initial_response, follow_up_question)
    follow_up_answer = format_to_bullets(follow_up_answer_raw)

    history = session.get('chat_history', [])
    history.append({'role': 'user', 'content': follow_up_question})
    history.append({'role': 'assistant', 'content': follow_up_answer})
    session['chat_history'] = history

    return render_template('index.html',
                           log_data=log_data,
                           analysis_result=initial_response,
                           reference_docs='',
                           log_category='',
                           chat_history=session.get('chat_history', []))

@app.route('/download', methods=['POST'])
def download():
    analysis_text = request.form['analysis_text']
    with open("analysis_result.txt", "w") as f:
        f.write(analysis_text)
    return send_file("analysis_result.txt", as_attachment=True)

@app.route('/clear')
def clear():
    session.clear()
    return redirect(url_for('index'))

def format_to_bullets(text):
    lines = text.strip().split('\n')
    bullets = []
    for line in lines:
        if line.strip():
            line = line.strip().lstrip("0123456789.:-•* ")
            bullets.append(f"<li>{line}</li>")
    return Markup("<ul>" + ''.join(bullets) + "</ul>")

if __name__ == "__main__":
    app.run(debug=True)
