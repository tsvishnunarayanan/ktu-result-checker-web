from flask import Flask, render_template, request, send_file
from bot import run_checker_web

app = Flask(__name__)  

@app.route('/', methods=['GET', 'POST'])
@app.route('/')
def index():
    import os
    username = os.getenv("KTU_ID")
    password = os.getenv("KTU_PASS")
    semester = os.getenv("KTU_SEM", "S4")
    status, pdf_path, img_path = run_checker_web(username, password, semester)
    return f"<h2>{status}</h2>"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

