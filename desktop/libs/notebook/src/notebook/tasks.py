from __future__ import absolute_import, unicode_literals
from celery import Celery
import json
import logging
import os

from desktop.conf import ENABLE_DOWNLOAD, USE_NEW_EDITOR
from desktop.views import serve_403_error

from notebook.connectors.base import get_api, _get_snippet_name

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'desktop.settings')

app = Celery('tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')

LOG = logging.getLogger(__name__)

@app.task
def download(request):
    if not ENABLE_DOWNLOAD.get():
        return serve_403_error(request)

    notebook = json.loads(request.POST.get('notebook', '{}'))
    snippet = json.loads(request.POST.get('snippet', '{}'))
    file_format = request.POST.get('format', 'csv')

    response = get_api(request, snippet).download(notebook, snippet, file_format,
                                                  user_agent=request.META.get('HTTP_USER_AGENT'))

    if response:
        request.audit = {
            'operation': 'DOWNLOAD',
            'operationText': 'User %s downloaded results from %s as %s' % (
            request.user.username, _get_snippet_name(notebook), file_format),
            'allowed': True
        }

    f=open("/tmp/foo","w")
    f.write(response.content)
    f.close()
    return 0
