import io
import json
import os
from datetime import datetime

from flask import Flask, render_template, request, send_file
from weasyprint import HTML

app = Flask(__name__)
PORT = 5000


# Get current date
def get_current_date():
    return datetime.now().strftime("%B %-d, %Y")


# Get default data from file
def get_default_data_from_file(filepath):
    with open(filepath, "r") as f:
        data = f.read()
    return data


# Generate data to submit to invoice based off of posted data or default data
def generate_data(posted_data, data):
    if posted_data:
        data["invoice_number"] = posted_data["invoice_number"]
        data["from_addr"] = posted_data["from_addr"]
        data["to_addr"] = posted_data["to_addr"]
        data["due_date"] = posted_data["due_date"]
        data["items"] = posted_data["items"]

    data["total"] = round(sum([i["charge"] for i in data["items"]]), 2)
    return data


# Render template from my data
def render_template_from_data(data, today):
    return render_template(
        "invoice.html",
        date=today,
        from_addr=data.get("from_addr"),
        to_addr=data.get("to_addr"),
        items=data.get("items"),
        total=data.get("total"),
        invoice_number=data.get("invoice_number"),
        due_date=data.get("due_date"),
    )


@app.route("/", methods=["GET", "POST"])
def hello_world():
    today = get_current_date()
    posted_data = request.get_json() or {}
    default_data = json.loads(
        get_default_data_from_file(
            os.path.join(os.path.dirname(__file__), "sample-data.json")
        )
    )

    data = generate_data(posted_data, default_data)

    rendered = render_template_from_data(data, today)

    html = HTML(string=rendered)
    rendered_pdf = html.write_pdf()
    return send_file(io.BytesIO(rendered_pdf), attachment_filename="invoice.pdf")


if __name__ == "__main__":
    port = int(os.environ.get("Port", PORT))
    app.run(host="0.0.0.0", port=port)  # nosec # re-evaluate this at a later date
