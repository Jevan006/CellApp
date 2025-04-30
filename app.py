import pyodbc
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

# Connect to the database
conn = pyodbc.connect(
    "DRIVER={SQL Server};SERVER=PF2WGETC\\SQLEXPRESS;DATABASE=CellApp;Trusted_Connection=yes;"
)

# Static leaders for dropdown based on zone selection
zone_leaders = {
    "Korle Bu": ["Michelle Peters", "Micheline Peters", "Destiny Manuel"],
    "Extension": ["Jaidee Ockhuis", "Venus Schroeder"],
}


@app.route("/get_leaders/<zone>")
def get_leaders(zone):
    cursor = conn.cursor()
    cursor.execute("SELECT LeaderName FROM Leaders WHERE Zone = ?", (zone,))
    leaders = [row.LeaderName for row in cursor.fetchall()]
    return jsonify(leaders)


@app.route("/")
def index():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Totals")
    totals = cursor.fetchall()

    cursor.execute("SELECT DISTINCT Zone FROM Leaders")
    zones = [row.Zone for row in cursor.fetchall()]

    return render_template("index.html", totals=totals, zones=zones)


@app.route("/submit", methods=["POST"])
def submit():
    # Get form data
    zone = request.form["zone"]
    grand_total = request.form["grand_total"]
    visitors = request.form["visitors"]
    decisions = request.form["decisions"]
    offering = request.form["offering"]
    leader_name = request.form["leader_name"]
    submission_date = request.form["submission_date"]  # Capture the submission date

    # Insert data into the Totals table
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Totals (Zone, GrandTotal, Visitors, Decisions, Offering, SubmissionDate, LeaderName)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
        (
            zone,
            grand_total,
            visitors,
            decisions,
            offering,
            submission_date,
            leader_name,
        ),
    )
    conn.commit()
    return redirect(url_for("index"))


@app.route("/update", methods=["POST"])
def update():
    # Get form data for update
    id = request.form["id"]
    grand_total = request.form["grand_total"]
    visitors = request.form["visitors"]
    decisions = request.form["decisions"]
    offering = request.form["offering"]
    submission_date = request.form["submission_date"]  # Capture the submission date

    # Update Totals table based on ID
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE Totals
        SET GrandTotal = ?, Visitors = ?, Decisions = ?, Offering = ?, SubmissionDate = ?
        WHERE ID = ?
    """,
        (
            grand_total,
            visitors,
            decisions,
            offering,
            submission_date,
            id,
        ),  # Pass the submission date for update
    )
    conn.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
