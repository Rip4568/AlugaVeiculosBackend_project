#CotratoAluguel_app/tasks/tasks.py
from __future__ import absolute_import, unicode_literals
from celery import shared_task
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.formats import currency
import asyncio

from ..models import Contrato

@shared_task
def update_contrato():
    # Obtém a data atual
	data_atual = datetime.now().date()

	# Obtém a data de amanhã
	data_amanha = (data_atual + timedelta(days=1)).date()

	# Obtém a lista de contratos que vencem amanhã
	contratos_a_vencer_amanha = Contrato.objects.filter(data_fim=data_amanha)

	# Obtém a lista de contratos que vencem hoje
	contratos_a_vencer_hoje = Contrato.objects.filter(data_fim=data_atual)

	# Obtém a lista de contratos vencidos (cuja data de término é anterior à data atual)
	contratos_vencidos = Contrato.objects.filter(data_fim__lt=data_atual)
	
	# Obtém a lista de contratos vencidos (cuja data de término é anterior à data atual)
	contratos_vencidos = Contrato.objects.filter(data_fim__lt=data_atual)

	de_email:str = settings.EMAIL_HOST_USER
	for contrato in contratos_vencidos:
		para_email:str = contrato.alugador.user.email
		contrato.incrementar_dias_de_atraso_pos_vencimento()
		valor_total = contrato.valor_total
		valor_total_formatado = currency(val=valor_total,symbol=True)
		assunto = f'O carro de {contrato.proprietario.nome}, esta em atraso!'
		mensagem = f'O veiculo cujo modelo: {contrato.veiculo.modelo}, marca: {contrato.veiculo.marca}, placa: {contrato.veiculo.placa} está em atraso! devolva o mais rapido possivel por favor. valor total atual:R$ {valor_total_formatado}'
		asyncio.run(contrato.enviar_email_alerta(
			assunto=assunto,
			mensagem=mensagem,
			de_email=de_email,
			para_email=[para_email,]
		))

	for contrato_vence_hoje in contratos_a_vencer_hoje:
		para_email:str = contrato_vence_hoje.alugador.user.email
		assunto = f'O carro de {contrato_vence_hoje.proprietario.nome}, deve ser devolvido hoje!'
		mensagem = f'O veiculo cujo modelo: {contrato_vence_hoje.veiculo.modelo}, marca: {contrato_vence_hoje.veiculo.marca}, placa: {contrato_vence_hoje.veiculo.placa} deve ser devolvido hoje, para cada dia de atraso começando amanhã vai ser cobrado mais 1 (um) dia de aluguel.'
		asyncio.run(contrato_vence_hoje.enviar_email_alerta(assunto=assunto,mensagem=mensagem,de_email=de_email,para_email=[para_email,]))
	
	for contrato_vence_amanha in contratos_a_vencer_amanha:
		para_email:str = contrato_vence_amanha.alugador.user.email
		assunto = f'O prazo para devolver o veiculo de {contrato_vence_amanha.proprietario.nome} é amanhã!'
		mensagem = f'O veiculo cujo modelo: {contrato_vence_amanha.veiculo.modelo}, marca: {contrato_vence_amanha.veiculo.marca}, placa: {contrato_vence_amanha.veiculo.placa} tem prazo para ser devolvido amanhã, programe-se para devolver, pois a cada dia de atraso será acrescido mais 1 (um) dia de aluguel.'
		#adicionei o asyncio.run para rodar o envio de email em segundo plano
		asyncio.run(contrato_vence_amanha.enviar_email_alerta(assunto=assunto,mensagem=mensagem,de_email=de_email,para_email=[para_email,]))