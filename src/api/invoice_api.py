import logging

import os
import json

from weasyprint import HTML

from fastapi import Request, APIRouter
from fastapi.responses import Response
from services import invoice_service


router = APIRouter()


def convert_to_pdf(html_string):
    html = HTML(string=html_string)
    pdf_bytes = html.write_pdf()
    return pdf_bytes


@router.post("/api/invoice", name="generate_invoice", status_code=201)
async def invoice_post(request: Request):
    logging.info("In invoice_post")

    posted_data = await request.json()
    default_data = json.loads(
        invoice_service.get_default_data_from_file(
            os.path.join(os.path.dirname(__file__), "sample-data.json")
        )
    )

    data = invoice_service.generate_data(posted_data, default_data)

    rendered = invoice_service.render_template_from_data(request, data)

    rendered_string = rendered.body.decode("utf-8")

    pdf_bytes = convert_to_pdf(rendered_string)

    headers = {"Content-Disposition": 'attachment; filename="out.pdf"'}
    return Response(pdf_bytes, headers=headers, media_type="application/pdf")
