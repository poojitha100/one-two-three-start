from flask import Flask, render_template, jsonify

app = Flask(__name__)

JOBS = [
    {
        "title": "SSC CGL 2026",
        "Details": "Apply Now"
    },
    {
        "title": "IBPS PO 2026",
        "Details": "Apply Now"
    },
    {
        "title": "RRB NTPC 2026",
        "Details": "Apply Now"
    },
    {
        "title": "APPSC Group 2",
        "Details": "Apply Now"
    }
]


@app.route("/")
def index():
    return render_template("index.html",jobs=JOBS)

@app.route("/api/jobs")
def list_jobs():
    return jsonify(JOBS)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
