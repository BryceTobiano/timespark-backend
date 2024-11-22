# example/views.py
from datetime import datetime

from django.http import HttpResponse

import os
from dotenv import load_dotenv
load_dotenv()

def index(request):
    now = os.getenv('DEBUG')
    html = f'''
    <html>
        <body>
            <h1>Hello from Vercel!</h1>
            <p>The current time is { now }.</p>
        </body>
    </html>
    '''
    return HttpResponse(html)