
from unittest import TestCase


from gestionAlmuerzos import helpers


class uuid_test(TestCase):

    def uuid_test_f(self):
        uuid = helpers.generar_uuid()

        self.assertIsNotNone(uuid)   # Si no es None el valor uuid, ya que se me caeria la url

        self.assertTrue((uuid.hex).__len__())  # Verifica la integridad del numero generado