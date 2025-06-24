from flask import Flask, render_template, request, send_file
from bot import run_checker_web
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None
    result_file = None
    screenshot_file = None

    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']
        semester = request.form['semester'].upper()

        if semester not in ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8"]:
            message = "Invalid semester. Use S1 to S8."
        else:
            message, result_file, screenshot_file = run_checker_web(user_id, password, semester)

    return render_template('index.html', message=message, result_file=result_file, screenshot_file=screenshot_file)

@app.route('/download/<path:filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)