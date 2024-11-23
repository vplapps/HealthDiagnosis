import unittest
from app import app

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_diagnose_route(self):
        # Відправка коректного JSON-запиту
        response = self.app.post('/diagnose', json={
            'name': 'John Doe',
            'age': 30,
            'temperature': 37.5,
            'pulse': 80,
            'pressure': 90,
            'spo2': 90
        })

        # Перевірка статус-коду
        self.assertEqual(response.status_code, 200)

        # Перевірка наявності рівня ризику
        self.assertIn('risk_level', response.get_json())
