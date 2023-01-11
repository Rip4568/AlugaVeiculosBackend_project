from django.test import TestCase
from django.utils import timezone
#from datetime import datetime, timedelta

from .models import Contrato
from Veiculo_app.models import Veiculo
from Proprietario_app.models import Proprietario
from Perfil_app.models import Perfil
from User_app.models import User

class ContratoTestCase(TestCase):
	def setUp(self):
		Contrato.objects.create(
			arquivo_contrato='contratos/contrato.pdf',
			#CONFIGURAR OS OUTROS CAMPOS
			veiculo=Veiculo.objects.create(
				proprietario=Perfil.objects.create(
					user=User.objects.create(
						username='proprietario_teste',
						password='123456',
					)
				),
				marca='Fiat',
				modelo='Uno',
				ano='2010',
				placa='ABC-1234',
				cor='Branco',
				alugado=False,
			),
			alugador=Perfil.objects.create(
				user=User.objects.create(
					username='alugador_teste',
					password='123456',
				)
			),
			data_inicio=timezone.now(),
			data_fim=timezone.now() + timezone.timedelta(days=1),#amanhã
			valor_diario=60.60,
			num_dias_aluguel=1,
			dias_atraso=0,
		)
	
	def test_contrato(self):
		contrato = Contrato.objects.get(arquivo_contrato='contratos/contrato.pdf')
		self.assertEqual(contrato.valor_total, 60.60)
		self.assertEqual(contrato.dias_atraso, 0)
		contrato.incrementar_dias_de_atraso_pos_vencimento()
		self.assertEqual(contrato.dias_atraso, 1)
		self.assertEqual(contrato.valor_total, 121.20)
	
	""" def test_contrato_valor_total(self):
		contrato = Contrato.objects.get(arquivo_contrato='contratos/contrato.pdf')
		self.assertEqual(contrato.valor_total, 60.60)
	
	def test_contrato_dias_atraso(self):
		contrato = Contrato.objects.get(arquivo_contrato='contratos/contrato.pdf')
		self.assertEqual(contrato.dias_atraso, 0)
		contrato.incrementar_dias_de_atraso_pos_vencimento()
		self.assertEqual(contrato.dias_atraso, 1)
		self.assertEqual(contrato.valor_total, 121.20) """