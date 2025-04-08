import os
import json
import unittest
from firebase_admin import credentials, initialize_app, firebase_admin

class TestFirebaseKey(unittest.TestCase):

    def test_firebase_key(self):
        # Carregar a chave do Firebase a partir da variável de ambiente
        firebase_key = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')

        # Verificar se a chave existe
        self.assertIsNotNone(firebase_key, "FIREBASE_SERVICE_ACCOUNT_KEY não foi configurado corretamente.")

        # Tentar carregar a chave JSON
        try:
            firebase_key_dict = json.loads(firebase_key)
            cred = credentials.Certificate(firebase_key_dict)
            initialize_app(cred)
        except json.JSONDecodeError:
            self.fail("Falha ao decodificar a chave JSON do Firebase.")
        except firebase_admin.exceptions.FirebaseError as e:
            self.fail(f"Falha ao inicializar o Firebase: {str(e)}")

if __name__ == "__main__":
    unittest.main()
