from weasyprint import HTML
from flask import Flask, render_template, send_file, request
import os
import io
from datetime import datetime, timedelta

app = Flask(__name__)
PORT = 5000


@app.route("/", methods=["GET", "POST"])
def hello_world():
    today = datetime.today().strftime("%B %-d, %Y")
    posted_data = request.get_json() or {}
    default_data = {
        "invoice_number": 123,
        "from_addr": {
            "company_name": "Sullivan Enterprises",
            "addr1": "2911 Anystreet",
            "addr2": "Roseville, MN  55113",
        },
        "to_addr": {
            "company_name": "Sullivan Group",
            "person_name": "Mr. Sullivan",
            "person_email": "mr@sullivanenterprises.org",
        },
        "items": [
            {"title": "website design", "charge": 300.00},
            {"title": "Hosting (3 months)", "charge": 75.00},
            {"title": "Domain name (1 year)", "charge": 10.00},
        ],
        "due_date": (datetime.today() + timedelta(30)).strftime("%B %-d, %Y"),
    }

    due_date = posted_data.get("duedate", default_data["due_date"])
    from_addr = posted_data.get("from_addr", default_data["from_addr"])
    to_addr = posted_data.get("to_addr", default_data["to_addr"])
    invoice_number = posted_data.get("invoice_number", default_data["invoice_number"])
    items = posted_data.get("items", default_data["items"])

    total = sum([i["charge"] for i in items])

    rendered = render_template(
        "invoice.html",
        date=today,
        from_addr=from_addr,
        to_addr=to_addr,
        items=items,
        total=total,
        invoice_number=invoice_number,
        due_date=due_date,
    )

    html = HTML(string=rendered)
    rendered_pdf = html.write_pdf()
    return send_file(io.BytesIO(rendered_pdf), attachment_filename="invoice.pdf")


if __name__ == "__main__":
    port = int(os.environ.get("Port", PORT))
    app.run(host="0.0.0.0", port=port)  # nosec # re-evaluate this at a later date
