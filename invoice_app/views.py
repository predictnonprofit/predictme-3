from django.views.generic import (TemplateView, View)
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from weasyprint import HTML, CSS
from django.shortcuts import (reverse, redirect, render)
from django.contrib.auth.mixins import (LoginRequiredMixin, UserPassesTestMixin)


class InvoiceDetailsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "invoice_app/detail.html"
    login_url = "login"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse('profile-overview'))


class InvoiceListView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "invoice_app/list.html"
    login_url = "login"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse('profile-overview'))


class InvCreateView(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = "login"

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False

    def handle_no_permission(self):
        return redirect(reverse('profile-overview'))

    def get(self, request):
        return render(request, "invoice_app/create.html")

    def post(self, request):
        print(request.POST)
        return render(request, "invoice_app/create.html")


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
