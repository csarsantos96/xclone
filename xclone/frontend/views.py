# frontend/views.py

from django.views.generic import View
from django.http import HttpResponse
import os

class FrontendAppView(View):
    def get(self, request):
        try:
            file_path = os.path.join(os.path.dirname(__file__), 'build', 'index.html')
            with open(file_path, 'r') as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponse("index.html não encontrado. Rode 'npm run build'!", status=501)
