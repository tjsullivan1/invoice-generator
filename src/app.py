# import io
# import json
import os
from datetime import datetime, timedelta

from flask import Flask, render_template, request, send_file
from weasyprint import HTML

app = Flask(__name__)


@app.route("/invoice", methods=["GET", "POST"])
def invoice():
    app.logger.debug("In the invoice function")
    today = datetime.today().strftime("%B %-d, %Y")
    posted_data = request.get_json()

    if posted_data is None:
        app.logger.debug(request)
        app.logger.debug(dir(request))
        app.logger.debug(request.data)
        app.logger.debug("posted_data is None")
        posted_data = {}

    app.logger.debug(f"posted_data: {posted_data}")
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

    due_date = posted_data.get("due_date", default_data["due_date"])
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
    rendered_pdf = html.write_pdf("invoice.pdf")  # noqa: F841
    return send_file(
        "invoice.pdf"
        # io.BytesIO(rendered_pdf),
        # attachment_filename='invoice.pdf'
    )


@app.route("/", methods=["GET", "POST"])
def index():
    app.logger.debug("In the index function")
    return '{"message": "Hello World"}'


if __name__ == "__main__":
    port = int(os.environ.get("Port", 5000))
    app.run(host="0.0.0.0", port=port)
