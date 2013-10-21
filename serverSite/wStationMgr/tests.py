"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from wStationMgr.models import Server

class ServerActionMethodTests(TestCase):

    def test_server(self):
        """
        was_published_recently() should return False for polls whose
        pub_date is in the future
        """
        server = Server(name="Servidor")
        self.assertEqual(server.name, "Servidor")


