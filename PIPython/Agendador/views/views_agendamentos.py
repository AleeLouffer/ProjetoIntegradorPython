from django.shortcuts import render, redirect
from datetime import date, datetime
from Agendador.repo import *
from Contas_a_Receber.repo import *
from Login.repo import *

def tela_agenda(requisicao):
    id_empresa = requisicao.session['id_empresa']
    
   
    agendamentos = filtrar_periodo_datas(requisicao, id_empresa)
    agendamentos = filtrar_funcionario(requisicao, agendamentos)
    agendamentos = filtrar_servico(requisicao, agendamentos)
    agendamentos = filtrar_status(requisicao, agendamentos)

    funcionarios = filtrar_funcionarios_ativos_por_id_empresa(requisicao, id_empresa)
    servicos = filtrar_servicos_ativos_por_id_empresa(requisicao, id_empresa)
    
    resposta = make_resposta(id_empresa, agendamentos, funcionarios, servicos)
    return render(requisicao, '../templates/agendamento/agenda.html', resposta)


def obter_data_filtro(requisicao, data):
    if data in requisicao.POST and requisicao.POST[data] != "":
        return datetime.strptime(requisicao.POST[data], '%Y-%m-%d').date()
    return None

def filtrar_periodo_datas(requisicao, id_empresa):
    data_inicial = obter_data_filtro(requisicao, 'data_inicial--agendamento')
    data_final = obter_data_filtro(requisicao, 'data_final--agendamento')

    if data_inicial and data_final:
        return filtrar_agendamentos_ativos_por_periodo_data_e_id_empresa(requisicao, id_empresa, data_inicial, data_final)

    elif data_inicial:
        return filtrar_agendamentos_ativos_por_data_e_id_empresa(requisicao, id_empresa, data_inicial)

    elif data_final:
        return filtrar_agendamentos_ativos_por_data_e_id_empresa(requisicao, id_empresa, data_final)
    
    elif data_inicial == None and data_final == None:
        data_inicial = date.today()
        data_final = date.today()

        return filtrar_agendamentos_ativos_por_periodo_data_e_id_empresa(requisicao, id_empresa, data_inicial, data_final)
    
def filtrar_funcionario(requisicao, agendamentos):
    if 'funcionario' in requisicao.POST:
        id_funcionario = requisicao.POST['funcionario']
        if id_funcionario != 'Todos Funcionários':
            return list(filter(lambda x: x.funcionario.id == int(id_funcionario), agendamentos))

    return agendamentos

def filtrar_servico(requisicao, agendamentos):
    if 'servico' in requisicao.POST:
        id_servico = requisicao.POST['servico']
        if id_servico != 'Todos Servicos':
            return list(filter(lambda x: x.servico.id == int(id_servico), agendamentos))

    return agendamentos

def filtrar_status(requisicao, agendamentos):
    if 'status' in requisicao.POST:
        status = requisicao.POST['status']
        if status != 'Todos Status':
            return list(filter(lambda x: x.completo == converter_para_bool(status), agendamentos))

    return agendamentos

def make_resposta(id_empresa, agendamentos, funcionarios, servicos):
    resposta = {
        'id_empresa': id_empresa,
        'agendamentos': agendamentos,
        'funcionarios': funcionarios,
        'servicos': servicos
    }
    return resposta


def tela_adicionar_agendamento(requisicao):
    id_empresa = requisicao.session['id_empresa']

    data = {
        'id_empresa': id_empresa,
        'clientes': list(filtrar_clientes_ativos_por_id_empresa(requisicao, id_empresa)),
        'funcionarios': list(filtrar_funcionarios_ativos_por_id_empresa(requisicao, id_empresa)),
        'servicos': list(filtrar_servicos_ativos_por_id_empresa(requisicao, id_empresa))
    }

    return render(requisicao, '../templates/agendamento/adicionar-agendamento.html', data)


def cadastrar_agendamento(requisicao):
    id_empresa = requisicao.session['id_empresa']

    id_cliente = requisicao.POST['cliente']
    cliente = obter_cliente_ativo_pelo_id(requisicao, id_cliente)
    
    id_servico = requisicao.POST['servico']
    servico = obter_servico_ativo_pelo_id(requisicao, id_servico)
    
    id_funcionario = requisicao.POST['funcionario']
    funcionario = obter_funcionario_ativo_pelo_id(requisicao, id_funcionario)
    
    data_agendamento = requisicao.POST['data_agendamento']
    hora_agendamento = requisicao.POST['hora_agendamento'] 
    
    criar_agendamento(requisicao, servico, cliente, funcionario, data_agendamento, hora_agendamento, id_empresa)



def verifica_botoes_agendamento(requisicao):
    if 'editar_agendamento' in requisicao.POST:
        data = obter_dados_tela_editar_agendamento(requisicao)
        return render(requisicao, '../templates/agendamento/editar-agendamento.html', data)
    elif 'excluir_agendamento' in requisicao.POST:
        excluir_agendamento(requisicao) 
        return redirect('Agendador:tela_agenda')
    elif 'editar_status' in requisicao.POST:
        requisicao.session['id_agendamento'] = requisicao.POST['id_agendamento']
        return redirect('Contas_a_Receber:adicionar_conta_agendamento')

def excluir_agendamento(requisicao):
    id_agendamento = requisicao.POST["id_agendamento"]
    
    deletar_agendamento(requisicao, id_agendamento)


def obter_dados_tela_editar_agendamento(requisicao):
    id_agendamento = requisicao.POST["id_agendamento"]
    id_empresa = requisicao.session["id_empresa"]

    agendamento = obter_agendamento_ativo_pelo_id(requisicao, id_agendamento)

    servicos = filtrar_servicos_ativos_por_id_empresa(requisicao, id_empresa)
    funcionarios = filtrar_funcionarios_ativos_por_id_empresa(requisicao, id_empresa)
    clientes = filtrar_clientes_ativos_por_id_empresa(requisicao, id_empresa)

    dados = {
        'agendamento': agendamento,
        'data_agendamento': str(agendamento.data),
        'servicos': remover_da_lista(servicos, agendamento.servico),
        'funcionarios': remover_da_lista(funcionarios, agendamento.funcionario),
        'clientes': remover_da_lista(clientes, agendamento.cliente)
    }

    return dados


def verificar_botoes_adicionar_agendamento(requisicao):
    if 'cancelar' in requisicao.POST:
        return redirect('Agendador:tela_agenda')
    if 'adicionar' in requisicao.POST:
        cadastrar_agendamento(requisicao)
        return redirect('Agendador:tela_agenda')

def verificar_botoes_editar_agendamento(requisicao):
    if 'cancelar' in requisicao.POST:
        return redirect('Agendador:tela_agenda')
    if 'editar' in requisicao.POST:
        editar_agendamento(requisicao)
        return redirect('Agendador:tela_agenda')

def editar_agendamento(requisicao):
    id_agendamento = requisicao.POST["id_agendamento"]

    data = requisicao.POST["data"]
    hora = requisicao.POST["hora_agendamento"]

    id_servico = requisicao.POST["id_servico"]
    servico = obter_servico_ativo_pelo_id(requisicao, id_servico)

    id_cliente = requisicao.POST["id_cliente"]
    cliente = obter_cliente_ativo_pelo_id(requisicao, id_cliente)

    id_funcionario = requisicao.POST["id_funcionario"]
    funcionario = obter_funcionario_ativo_pelo_id(requisicao, id_funcionario)

    atualizar_agendamento(requisicao, id_agendamento, servico, cliente, funcionario, data, hora)
    

def remover_da_lista(lista, item_a_remover):
    for i in lista:
        if i == item_a_remover:
            lista.remove(item_a_remover)
    
    return lista

def converter_para_bool(string):
    if string == 'True':
        return True
    elif string == 'False':
        return False
    else:
        raise ValueError