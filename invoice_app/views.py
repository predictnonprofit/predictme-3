from django.views.generic import TemplateView
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa
from weasyprint import HTML, CSS




class InvoiceDetailsView(TemplateView):
    template_name = "invoice_app/detail.html"


class InvliceListView(TemplateView):
    template_name = "invoice_app/list.html"


class InvCreateView(TemplateView):
    template_name = "invoice_app/create.html"



# def generate_printable_pdf(template_src, invoice_context_data={}):
#     template = get_template(template_src)
#     html = template.render(invoice_context_data)
#     result = BytesIO()
#     pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
#     if not pdf.err:
#         return HttpResponse(result.getvalue(), content_type="application/pdf")
#
#     return None

def pdf_generation(request):
    html_template = get_template('templates/home_page.html')
    pdf_file = HTML(string=html_template).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="home_page.pdf"'
    return response


class InvoicePrintView(View):

    def get(self, request, *args, **kwargs):
        html_template = get_template('invoice_app/inc/invoice_template.html')
        pdf_file = HTML(string=html_template).write_pdf()
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="INVOICE #25.pdf"'
        return response
