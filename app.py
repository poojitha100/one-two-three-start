from flask import Flask, render_template, jsonify, request, redirect
import mysql.connector

app = Flask(__name__)

try:
    db = mysql.connector.connect(
        host="sql.freedb.tech",
        user="u_F67wYN",
        password="WkeQ6maN0ZhC",
        database="freedb_Q7U3nO3c",
        port=3306
    )

    print("✅ Database connected successfully!")
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        details VARCHAR(255) NOT NULL
    )
    """)

    db.commit()

    print("✅ Jobs table created successfully!")

except Exception as e:
    print("❌ Database connection failed!")
    print(e)

@app.route("/")
def index():
    cursor.execute("SELECT title, details FROM jobs")
    rows = cursor.fetchall()

    jobs = []

    for row in rows:
        jobs.append({
            "title": row[0],
            "Details": row[1]
        })

    return render_template("index.html", jobs=jobs)

@app.route("/api/jobs")
def list_jobs():
    cursor.execute("SELECT title, details FROM jobs")
    rows = cursor.fetchall()

    jobs = []

    for row in rows:
        jobs.append({
            "title": row[0],
            "Details": row[1]
        })

    return jsonify(jobs)

@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/add-job", methods=["POST"])
def add_job():

    title = request.form["title"]
    details = request.form["details"]

    cursor.execute(
        "INSERT INTO jobs (title, details) VALUES (%s, %s)",
        (title, details)
    )

    db.commit()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
