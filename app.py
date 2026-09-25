from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Home / Incident Form
@app.route("/")
def incident_form():
    return render_template("incident.html")


# Client Script validation
@app.route("/validate_incident", methods=["POST"])
def validate_incident():
    data = request.get_json()

    short_description = data.get("short_description", "").strip()
    priority = data.get("priority", "")
    state = data.get("state", "")

    errors = []

    # Client Script: Short Description is mandatory
    if not short_description:
        errors.append("Short Description is mandatory.")

    # Client Script: High priority requires description
    if priority == "1" and len(short_description) < 10:
        errors.append(
            "For Critical priority, Short Description must contain at least 10 characters."
        )

    return jsonify({
        "success": len(errors) == 0,
        "errors": errors
    })


# UI Policy logic
@app.route("/ui_policy", methods=["POST"])
def ui_policy():
    data = request.get_json()

    priority = data.get("priority", "")
    state = data.get("state", "")

    policy = {
        "show_urgent_message": priority == "1",
        "make_resolution_required": state == "Resolved",
        "disable_priority": state == "Closed"
    }

    return jsonify(policy)


if __name__ == "__main__":
    app.run(debug=True)
