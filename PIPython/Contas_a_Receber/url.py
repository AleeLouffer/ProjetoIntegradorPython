from django.contrib import admin
from django.urls import path
from Contas_a_Receber import views

app_name = "Contas_a_Receber"

urlpatterns = [
    path('contas_a_receber/', views.tela_contas_a_receber, name="tela_contas_a_receber"),
    path('adicionar_conta/', views.adicionar_conta, name="adicionar_conta"),
    path('editar_conta/', views.editar_conta, name="editar_conta"),
    path('adicionar_conta_agentamento/', views.adicionar_conta_agendamento, name="adicionar_conta_agendamento"),
    path('verifica_botoes_conta_agendamento/', views.verifica_botoes_conta_agendamento, name="verifica_botoes_conta_agendamento")
]
