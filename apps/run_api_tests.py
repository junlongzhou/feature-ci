#!/usr/bin/env python
from os import environ
import sys

import django
from django.conf import settings
from django.test.utils import get_runner

# for local tests running
LOCAL_DEVELOPMENT = environ.get('LOCAL_DEVELOPMENT', 'true') == 'true'

if __name__ == "__main__": 
    if LOCAL_DEVELOPMENT:
        environ["DJANGO_SETTINGS_MODULE"] = "apiserver.settings.test"
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['features.tests'])
    sys.exit(bool(failures))
