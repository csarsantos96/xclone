import os
import unittest
import firebase_admin
from firebase_admin import credentials

class TestFirebaseKey(unittest.TestCase):
    def test_firebase_key_file_exists_and_valid(self):
        path = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY_PATH')
        self.assertTrue(path and os.path.exists(path), "Arquivo da chave do Firebase não encontrado.")

        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(path)
                firebase_admin.initialize_app(cred)
        except Exception as e:
            self.fail(f"Erro ao inicializar o Firebase com o arquivo: {e}")

if __name__ == "__main__":
    unittest.main()
