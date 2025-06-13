from flask import Flask, request, jsonify
from jobspy import scrape_jobs

app = Flask(__name__)

@app.route("/scrape", methods=["POST"])
def scrape():
    data = request.json

    # Default values from client filters
    search_term = data.get("search_query", '"graduate program" OR internship OR "early career"')
    location = data.get("location", "Netherlands")
    country_indeed = data.get("country", "Netherlands")

    job_type_map = {
        "Full-Time": "fulltime",
        "Part-Time": "parttime",
        "Contract": "contract",
        "Internship": "internship"
    }
    job_type = job_type_map.get(data.get("job_type", "All"), None)

    remote_pref = data.get("remote", "All")
    is_remote = True if remote_pref == "Remote" else False if remote_pref == "On-site" else None

    try:
        jobs = scrape_jobs(
            site_name=["linkedin", "indeed", "glassdoor"],
            search_term=search_term,
            location=location,
            job_type=job_type,
            is_remote=is_remote,
            results_wanted=30,
            hours_old=72,
            country_indeed=country_indeed,
            linkedin_fetch_description=False,
            verbose=0,
        )

        return jsonify(jobs.to_dict(orient="records"))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
