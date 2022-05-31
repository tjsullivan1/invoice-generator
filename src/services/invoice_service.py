from datetime import datetime

from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")


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
def render_template_from_data(request, data, today=get_current_date()):
    return templates.TemplateResponse(
        "invoice.html",
        {
            "request": request,
            "date": today,
            "from_addr": data["from_addr"],
            "to_addr": data["to_addr"],
            "due_date": data["due_date"],
            "items": data["items"],
            "total": data["total"],
        },
    )
    # return render_template(
    #     "invoice.html",
    #     date=today,
    #     from_addr=data.get("from_addr"),
    #     to_addr=data.get("to_addr"),
    #     items=data.get("items"),
    #     total=data.get("total"),
    #     invoice_number=data.get("invoice_number"),
    #     due_date=data.get("due_date"),
    # )
