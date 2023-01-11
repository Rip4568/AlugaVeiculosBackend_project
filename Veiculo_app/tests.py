from django.test import TestCase

from .models import Veiculo
class VeiculoTestCase(TestCase):
    def setUp(self):
        Veiculo.objects.create(placa="ABC-1234", marca="Fiat", modelo="Uno", cor="Branco", ano="2010")
        Veiculo.objects.create(placa="DEF-5678", marca="Ford", modelo="Fiesta", cor="Preto", ano="2015")

    def test_veiculo_placa(self):
        """Veiculos que começam com ABC tem placa ABC-1234"""
        veiculo_abc = Veiculo.objects.get(placa="ABC-1234")
        veiculo_def = Veiculo.objects.get(placa="DEF-5678")
        self.assertEqual(veiculo_abc.placa, 'ABC-1234')
        self.assertEqual(veiculo_def.placa, 'DEF-5678')

    def test_veiculo_marca(self):
        """Veiculos que começam com ABC tem marca Fiat"""
        veiculo_abc = Veiculo.objects.get(placa="ABC-1234")
        veiculo_def = Veiculo.objects.get(placa="DEF-5678")
        self.assertEqual(veiculo_abc.marca, 'Fiat')
        self.assertEqual(veiculo_def.marca, 'Ford')

    def test_veiculo_modelo(self):
        """Veiculos que começam com ABC tem modelo Uno"""
        veiculo_abc = Veiculo.objects.get(placa="ABC-1234")
        veiculo_def = Veiculo.objects.get(placa="DEF-5678")
        self.assertEqual(veiculo_abc.modelo, 'Uno')
        self.assertEqual(veiculo_def.modelo, 'Fiesta')

    def test_veiculo_cor(self):
        """Veiculos que começam com ABC tem cor Branco"""
        veiculo_abc = Veiculo.objects.get(placa="ABC-1234")
        veiculo_def = Veiculo.objects.get(placa="DEF-5678")
        self.assertEqual(veiculo_abc.cor, 'Branco')
        self.assertEqual(veiculo_def.cor, 'Preto')

    def test_veiculo_ano(self):
        """Veiculos que começam com ABC tem ano 2010"""
        veiculo_abc = Veiculo.objects.get(placa="ABC-1234")
        veiculo_def = Veiculo.objects.get(placa="DEF-5678")
        self.assertEqual(veiculo_abc.ano, '2010')
        self.assertEqual(veiculo_def.ano, '2015')
