import mysql.connector
from flask import Flask, jsonify, redirect, render_template, request, url_for

app = Flask(__name__)

# 🔌 Connect to MySQL Workbench
conn = mysql.connector.connect(
    host="localhost",
    user="root",  # CHANGE THIS
    password="!St0107195090082",  # CHANGE THIS
    database="church_db",
)
cursor = conn.cursor(dictionary=True)


# 🏠 Home Page (Submission Form)
@app.route("/")
def index():
    return render_template("index.html")


# 🔽 Fetch Zone List for Dropdown
@app.route("/get_zones")
def get_zones():
    cursor.execute("SELECT ZoneName FROM Zones")
    zones = [row["ZoneName"] for row in cursor.fetchall()]
    return jsonify(zones)


# 🔽 Fetch Leaders for Selected Zone
@app.route("/get_leaders/<zone>")
def get_leaders(zone):
    cursor.execute("SELECT LeaderName FROM Leaders WHERE ZoneName = %s", (zone,))
    leaders = [row["LeaderName"] for row in cursor.fetchall()]
    return jsonify(leaders)


# ✅ Submit Totals
@app.route("/submit_totals", methods=["POST"])
def submit_totals():
    data = request.form
    query = """
        INSERT INTO Totals (ServiceDay, LeaderName, ZoneName, GrandTotal, Visitors, Decisions, Offering, SubmissionDate)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        data["service_day"],
        data["leader_name"],
        data["zone"],
        data["grand_total"],
        data["visitors"],
        data["decisions"],
        data["offering"],
        data["submission_date"],
    )
    cursor.execute(query, values)
    conn.commit()
    return redirect(url_for("index"))


# 📊 View Totals for a Specific Zone
@app.route("/zone_totals", methods=["GET", "POST"])
def zone_totals():
    if request.method == "POST":
        zone = request.form["zone"]
        cursor.execute(
            "SELECT * FROM Totals WHERE ZoneName = %s ORDER BY SubmissionDate DESC",
            (zone,),
        )
        totals = cursor.fetchall()
        return render_template("zone_totals.html", zone=zone, totals=totals)
    else:
        cursor.execute("SELECT ZoneName FROM Zones")
        zones = [row["ZoneName"] for row in cursor.fetchall()]
        return render_template("zone_totals.html", zones=zones, totals=None)


if __name__ == "__main__":
    app.run(debug=True)
