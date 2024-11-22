# example/views.py
from datetime import datetime

from django.http import HttpResponse

import os
from decouple import config

def index(request):
    now = config('DEBUG')
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)