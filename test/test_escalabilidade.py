# # test/test_scalability.py
# import time
# import random
# import pytest
# from django.db import connection
# from locust import HttpUser, task, between
# from locust.env import Environment
# import os
# from terminate_after import start_terminator, stop_terminator
#
#
# # ------------------------------------------------------------------
# # 1. Definição das Tarefas do Locust
# # ------------------------------------------------------------------
# class OficinaUsuarioSimulado(HttpUser):
#     wait_time = between(0.1, 0.5)
#
#     @task(3)
#     @pytest.mark.django_db(transaction=True)
#     def test_escalabilidade_listagem_motoristas(self):
#         self.client.get("/api/motoristas/", name="[GET] /api/motoristas/")
#
#     @task(2)
#     @pytest.mark.django_db(transaction=True)
#     def test_escalabilidade_criacao_e_fluxo(self):
#         cpf_aleatorio = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-00"
#
#         payload_motorista = {
#             "nome": f"Cliente Carga {random.randint(1, 10000)}",
#             "cpf": cpf_aleatorio,
#             "telefone": "11999999999",
#             "endereco": "Rua da Carga, 100",
#             "email": f"carga_{random.randint(1, 10000)}@teste.com"
#         }
#         res_m = self.client.post("/api/motoristas/", json=payload_motorista, name="[POST] /api/motoristas/")
#
#         if res_m.status_code == 201:
#             motorista_id = res_m.json()["id"]
#
#             payload_auto = {
#                 "marca": "Fiat",
#                 "modelo": "Uno",
#                 "ano": 2020,
#                 "motorista": motorista_id
#             }
#             res_a = self.client.post("/api/automoveis/", json=payload_auto, name="[POST] /api/automoveis/")
#
#             if res_a.status_code == 201:
#                 auto_id = res_a.json()["id"]
#
#                 payload_conserto = {
#                     "automovel": auto_id,
#                     "problema_carro": "Teste de carga live server",
#                     "pecas_trocadas": "Óleo e Filtro",
#                     "data_entrada": "2026-07-30",
#                     "mecanico_responsavel": "Mecânico Carga",
#                     "valor_pecas": "100.00",
#                     "valor_servico": "150.00"
#                 }
#                 self.client.post("/api/consertos/", json=payload_conserto, name="[POST] /api/consertos/")
#
#     @task(1)
#     @pytest.mark.django_db(transaction=True)
#     def test_escalabilidade_consulta_consertos(self):
#         self.client.get("/api/consertos/", name="[GET] /api/consertos/")
#
#
# # ------------------------------------------------------------------
# # 2. Classe do Pytest com Habilitação Multi-Thread do Banco
# # ------------------------------------------------------------------
# @pytest.mark.django_db(transaction=True)
# class TestEscalabilidadeLiveServer:
#
#     def setup_method(self):
#         """Habilita o compartilhamento de conexões do banco de dados entre threads ativas"""
#         connection.inc_thread_sharing()
#
#     def teardown_method(self):
#         """Remove o compartilhamento ao finalizar o teste"""
#         connection.dec_thread_sharing()
#
#     @pytest.mark.django_db(transaction=True)
#     def test_executar_carga_locust_no_live_server(self, live_server):
#         # Configura o ambiente informando a URL do LiveServer
#         env = Environment(user_classes=[OficinaUsuarioSimulado], host=live_server.url)
#         env.create_local_runner()
#
#         # Start a background terminator so CI/pipeline won't hang.
#         # Timeout (seconds) can be set via PIPELINE_TIMEOUT env var. Default: 10s
#         timer = start_terminator()
#
#         # Inicia 15 usuários virtuais
#         try:
#             env.runner.start(user_count=15, spawn_rate=5)
#
#             # Executa a carga por um curto período (se desejar um tempo fixo local, ajuste abaixo)
#             # Se PIPELINE_TIMEOUT estiver definido, o processo será encerrado por start_terminator.
#             time.sleep(5)
#
#         except KeyboardInterrupt:
#             print("\n[TEST TERMINATOR] KeyboardInterrupt received; collecting stats and cleaning up...")
#         finally:
#             # Encerra o Locust (garantido)
#             try:
#                 env.runner.stop()
#             except Exception:
#                 pass
#
#         # Verificações dos resultados obtidos no servidor
#         stats = env.runner.stats.total
#         try:
#             stats = env.runner.stats.total
#             print(f"\n[LIVE SERVER LOCUST] Total de Requisições: {stats.num_requests} | Falhas: {stats.num_failures}")
#         except Exception as e:
#             print(f"\n[ERROR] Não foi possível obter estatísticas do runner: {e}")
#
#         # Cancel the terminator to prevent further interrupts
#         try:
#             stop_terminator(timer)
#         except Exception:
#             pass
#
#         # Assertions (if stats available)
#         try:
#             assert stats.num_requests > 0, "O LiveServer não processou requisições."
#             assert stats.num_failures == 0, f"Ocorreram {stats.num_failures} falhas no processamento multi-thread."
#         except NameError:
#             pytest.skip("Runner stats não disponíveis após interrupção.")