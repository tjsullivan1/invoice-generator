# import io
# import json
import os


#  Flask, render_template, request, send_file
import fastapi
from fastapi.staticfiles import StaticFiles
from api import invoice_api
from views import home
import uvicorn

# from weasyprint import HTML


PORT = 5000

app = fastapi.FastAPI()


def configure():
    configure_routing()


def configure_routing():
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(home.router)
    app.include_router(invoice_api.router)


# @app.route("/", methods=["GET", "POST"])
# def hello_world():
#     today = get_current_date()
#     posted_data = request.get_json() or {}
#     default_data = json.loads(
#         get_default_data_from_file(
#             os.path.join(os.path.dirname(__file__), "sample-data.json")
#         )
#     )

#     data = generate_data(posted_data, default_data)

#     rendered = render_template_from_data(data, today)

#     html = HTML(string=rendered)
#     rendered_pdf = html.write_pdf()
#     return send_file(io.BytesIO(rendered_pdf), attachment_filename="invoice.pdf")


# if __name__ == "__main__":
#     port = int(os.environ.get("Port", PORT))
#     app.run(host="0.0.0.0", port=port)  # nosec # re-evaluate this at a later date


if __name__ == "__main__":
    configure()
    port = int(os.environ.get("Port", PORT))
    uvicorn.run(app, port=port, host="127.0.0.1")
else:
    configure()
