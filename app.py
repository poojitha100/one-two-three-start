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

    cursor = db.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        organization VARCHAR(255) NOT NULL,
        qualification VARCHAR(255) NOT NULL,
        age_limit VARCHAR(100) NOT NULL,
        last_date DATE NOT NULL,
        official_link VARCHAR(500) NOT NULL,
        notification_link VARCHAR(500) NOT NULL,
        description TEXT NOT NULL
    )
    """)

    db.commit()

    print("✅ Database connected successfully!")
    print("✅ Jobs table created successfully!")

except Exception as e:
    print("❌ Database connection failed!")
    print(e)


@app.route("/")
def index():

    cursor.execute("""
        SELECT id,title,organization,last_date
        FROM jobs
        ORDER BY last_date
    """)

    rows = cursor.fetchall()

    jobs = []

    for row in rows:
        jobs.append({
            "id": row[0],
            "title": row[1],
            "organization": row[2],
            "last_date": row[3]
        })

    return render_template("index.html", jobs=jobs)


@app.route("/job/<int:id>")
def job_details(id):

    cursor.execute("""
        SELECT *
        FROM jobs
        WHERE id=%s
    """, (id,))

    row = cursor.fetchone()

    job = {
        "id": row[0],
        "title": row[1],
        "organization": row[2],
        "qualification": row[3],
        "age_limit": row[4],
        "last_date": row[5],
        "official_link": row[6],
        "notification_link": row[7],
        "description": row[8]
    }

    return render_template("job_details.html", job=job)


@app.route("/api/jobs")
def api_jobs():

    cursor.execute("SELECT * FROM jobs")

    rows = cursor.fetchall()

    jobs = []

    for row in rows:
        jobs.append({
            "id": row[0],
            "title": row[1],
            "organization": row[2],
            "qualification": row[3],
            "age_limit": row[4],
            "last_date": str(row[5]),
            "official_link": row[6],
            "notification_link": row[7],
            "description": row[8]
        })

    return jsonify(jobs)


@app.route("/admin")
def admin():

    cursor.execute("SELECT * FROM jobs")

    rows = cursor.fetchall()

    jobs = []

    for row in rows:
        jobs.append({
            "id": row[0],
            "title": row[1],
            "organization": row[2],
            "qualification": row[3],
            "age_limit": row[4],
            "last_date": row[5],
            "official_link": row[6],
            "notification_link": row[7],
            "description": row[8]
        })

    return render_template("admin.html", jobs=jobs)


@app.route("/add-job", methods=["POST"])
def add_job():

    cursor.execute("""
        INSERT INTO jobs
        (title,organization,qualification,age_limit,last_date,
        official_link,notification_link,description)

        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (

        request.form["title"],
        request.form["organization"],
        request.form["qualification"],
        request.form["age_limit"],
        request.form["last_date"],
        request.form["official_link"],
        request.form["notification_link"],
        request.form["description"]

    ))

    db.commit()

    return redirect("/admin")


@app.route("/edit-job/<int:id>")
def edit_job(id):

    cursor.execute("SELECT * FROM jobs WHERE id=%s", (id,))

    row = cursor.fetchone()

    job = {
        "id": row[0],
        "title": row[1],
        "organization": row[2],
        "qualification": row[3],
        "age_limit": row[4],
        "last_date": row[5],
        "official_link": row[6],
        "notification_link": row[7],
        "description": row[8]
    }

    return render_template("edit_job.html", job=job)


@app.route("/update-job/<int:id>", methods=["POST"])
def update_job(id):

    cursor.execute("""
        UPDATE jobs
        SET
            title=%s,
            organization=%s,
            qualification=%s,
            age_limit=%s,
            last_date=%s,
            official_link=%s,
            notification_link=%s,
            description=%s
        WHERE id=%s
    """, (

        request.form["title"],
        request.form["organization"],
        request.form["qualification"],
        request.form["age_limit"],
        request.form["last_date"],
        request.form["official_link"],
        request.form["notification_link"],
        request.form["description"],
        id

    ))

    db.commit()

    return redirect("/admin")


@app.route("/delete-job/<int:id>")
def delete_job(id):

    cursor.execute("DELETE FROM jobs WHERE id=%s", (id,))

    db.commit()

    return redirect("/admin")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)