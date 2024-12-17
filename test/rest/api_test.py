import http.client
import os
import unittest
from urllib.request import urlopen

import pytest

BASE_URL = "http://localhost:5000"
BASE_URL_MOCK = "http://localhost:9090"
DEFAULT_TIMEOUT = 2  # in secs

@pytest.mark.api
class TestApi(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(BASE_URL, "URL no configurada")
        self.assertTrue(len(BASE_URL) > 8, "URL no configurada")

    def test_api_add(self):
        url = f"{BASE_URL}/calc/add/1/2"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "3", "ERROR ADD"
        )

    def test_api_sqrt(self):
        url = f"{BASE_URL_MOCK}/calc/sqrt/64"
        response = urlopen(url, timeout=DEFAULT_TIMEOUT)
        self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
        )
        self.assertEqual(
            response.read().decode(), "8", "ERROR SQRT"
        )

# NUEVO

    def test_api_power(self):
    	base = 2
    	exponent = 3
    	url = f"{BASE_URL_MOCK}/calc/power/2/3"
    	response = urlopen(url, timeout=DEFAULT_TIMEOUT)
    	self.assertEqual(
            response.status, http.client.OK, f"Error en la petición API a {url}"
    	)
    	self.assertEqual(
            response.read().decode(), "8", "ERROR POWER"
    	)

if __name__ == "__main__":  # pragma: no cover
    unittest.main()
