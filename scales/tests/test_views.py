import pytest

from django.urls import reverse
from django.test import TestCase
from django.test.client import Client

from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db

# Create your view tests here.
