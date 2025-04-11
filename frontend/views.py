# frontend/views.py
from django.views.generic import View
from django.http import HttpResponse
import os

class FrontendAppView(View):
    def get(self, request):
        try:
            with open(os.path.join(os.path.dirname(__file__), '../frontend/build/index.html')) as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponse("React app não encontrado. Rode 'npm run build'!", status=501)
