from flask import Flask, render_template, request
from resume_parser import extract_text_from_pdf
from skill_matcher import extract_skills, calculate_match
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    resume = request.files["resume"]
    job_description = request.form["job_description"]

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        resume.filename
    )

    resume.save(filepath)

    resume_text = extract_text_from_pdf(filepath)

    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    score = calculate_match(
        resume_text,
        job_description
    )

    # Category and Recommendation
    if score >= 80:
        category = "Excellent"
        recommendation = "Recommended for Interview"

    elif score >= 60:
        category = "Good"
        recommendation = "Consider for Interview"

    elif score >= 40:
        category = "Average"
        recommendation = "Needs Improvement"

    else:
        category = "Poor"
        recommendation = "Not Recommended"

    missing_skills = list(
        set(jd_skills) - set(resume_skills)
    )

    return render_template(
        "index.html",
        score=score,
        resume_skills=resume_skills,
        jd_skills=jd_skills,
        missing_skills=missing_skills,
        category=category,
        recommendation=recommendation
    )


if __name__ == "__main__":
    app.run(debug=True)