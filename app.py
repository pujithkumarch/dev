from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
import boto3, os

app = Flask(__name__)

# MongoDB
client = MongoClient("mongodb://mongo-service:27017")
db = client["snist_expo"]
collection = db["faculty_feedback"]

# S3
S3_BUCKET = "snist-expo-feedback"
S3_KEY = "feedback-report.html"
s3 = boto3.client("s3", region_name="ap-south-1")

def generate_html_report(entries):
    rows = ""
    for i, e in enumerate(entries, 1):
        r = e.get("ratings", {})
        rows += f"""
        <tr>
            <td>{i}</td>
            <td>{e.get('faculty_name','')}</td>
            <td>{e.get('department','')}</td>
            <td>{e.get('designation','')}</td>
            <td>{r.get('technical_complexity','')}</td>
            <td>{r.get('cicd_understanding','')}</td>
            <td>{r.get('presentation','')}</td>
            <td>{r.get('overall_quality','')}</td>
            <td>{e.get('comments','')}</td>
            <td><b>{e.get('grade_recommendation','')}</b></td>
            <td>{str(e.get('submitted_at',''))[:19]}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>SNIST Expo Feedback Report</title>
<style>
  body {{ font-family: Arial, sans-serif; padding: 30px; background: #f5f5f5; }}
  h1 {{ color: #1a1d2e; }}
  h2 {{ color: #5b6cf9; font-size: 15px; margin-bottom: 20px; }}
  table {{ border-collapse: collapse; width: 100%; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
  th {{ background: #5b6cf9; color: white; padding: 12px 10px; text-align: left; font-size: 13px; }}
  td {{ padding: 10px; border-bottom: 1px solid #eee; font-size: 13px; color: #333; }}
  tr:last-child td {{ border-bottom: none; }}
  tr:hover td {{ background: #f0f1ff; }}
  .footer {{ margin-top: 16px; font-size: 12px; color: #999; }}
</style>
</head>
<body>
<h1>DevOps Project Expo — SNIST</h1>
<h2>Faculty Feedback Report &nbsp;|&nbsp; Total submissions: {len(entries)}</h2>
<table>
<thead>
  <tr>
    <th>#</th><th>Faculty Name</th><th>Department</th><th>Designation</th>
    <th>Technical</th><th>CI/CD</th><th>Presentation</th><th>Overall</th>
    <th>Comments</th><th>Grade</th><th>Submitted At</th>
  </tr>
</thead>
<tbody>{rows}</tbody>
</table>
<p class="footer">Generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
</body>
</html>"""

def upload_to_s3():
    entries = list(collection.find({}, {"_id": 0}))
    html = generate_html_report(entries)
    s3.put_object(
        Bucket=S3_BUCKET,
        Key=S3_KEY,
        Body=html.encode("utf-8"),
        ContentType="text/html"
    )

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/feedback", methods=["POST"])
def submit_feedback():
    data = request.get_json()
    data["submitted_at"] = datetime.utcnow().isoformat()
    collection.insert_one(data)
    upload_to_s3()
    return jsonify({"message": "Feedback saved"}), 201

@app.route("/api/feedbacks", methods=["GET"])
def get_feedbacks():
    entries = list(collection.find({}, {"_id": 0}))
    return jsonify(entries)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
