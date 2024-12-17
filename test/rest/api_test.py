import http.client
import os
import unittest
from urllib.request import urlopen
import time
import pytest
import socket

BASE_URL = "http://localhost:5000"
BASE_URL_MOCK = "http://localhost:9090"
DEFAULT_TIMEOUT = 2  # en segundos
PORT_CHECK_TIMEOUT = 15  # Tiempo máximo para esperar al puerto

def wait_for_port(host: str, port: int, timeout: int):
    """Espera hasta que el puerto esté disponible o expire el tiempo."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            if sock.connect_ex((host, port)) == 0:
                print(f"El puerto {port} está disponible.")
                return
        print(f"Esperando al puerto {port}...")
        time.sleep(1)
    raise TimeoutError(f"El puerto {port} no está disponible después de {timeout} segundos.")


@pytest.mark.api
class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        wait_for_port("localhost", 5000, PORT_CHECK_TIMEOUT)
        wait_for_port("localhost", 9090, PORT_CHECK_TIMEOUT)

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


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
