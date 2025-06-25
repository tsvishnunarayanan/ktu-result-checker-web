from flask import Flask, render_template, request, send_file
from bot import run_checker_web

app = Flask(__name__)  

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        semester = request.form['semester']
        status, pdf_path, img_path = run_checker_web(username, password, semester)
        return f"<h2>{status}</h2>"
    return '''
        <form method="post">
            <label>KTU ID:</label><input name="username"><br>
            <label>Password:</label><input name="password" type="password"><br>
            <label>Semester (S1-S8):</label><input name="semester"><br>
            <input type="submit" value="Check Result">
        </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
