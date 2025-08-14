import socket
from ipaddress import IPv4Address, IPv6Address, ip_address
import json
from threads import thread_conectar
from threading import Thread
import gui
import pygame
from select import select

# cria e retorna uma referência a um socket
# do tipo especificado
def criarSocket(ip, protocolo):
    
    try: # checa o tipo de ip usado e seleciona o tipo de socket apropriado
        if isinstance(ip_address(ip), IPv4Address):
            tipoIP = socket.AF_INET
        elif isinstance(ip_address(ip), IPv6Address):
            tipoIP = socket.AF_INET6
    except ValueError:
        raise ValueError(f"IP inválido: {ip}")
    
    # checa o protocolo usado e seleciona o tipo de socket apropriado
    if protocolo == "tcp":
        tipoSocket = socket.SOCK_STREAM
    else:
        tipoSocket = socket.SOCK_DGRAM

    # cria o socket de acordo com os parâmetros passados
    sock = socket.socket(tipoIP, tipoSocket)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock

# envia um dicionário em formato de JSON serializado pela rede
def enviarDados(sock, dados, protocolo, oponente_addr=None):
    # cria um JSON com o dicionário em utf-8
    dados = json.dumps(dados).encode("utf-8")

    # manda os dados pela rede usando o protocolo correto
    try:
        if protocolo == "tcp":
            sock.sendall(dados)
        else:
            if oponente_addr: # só manda por UDP se um endereço foi passado
                sock.sendto(dados, oponente_addr)
    except socket.error as e:
        print(f"Erro ao enviar dados: {e}")

# recebe e desserializa um dicionário em formato de JSON pela rede
def receberDados(sock, protocolo, buffer=1024):

    # essa função retorna o endereço do outro lado da conexão
    # porque o protocolo UDP não faz esse controle automaticamente,
    # então a aplicação tem que lidar com essa limitação e guardar o 
    # IP do computador conectado para conseguir mandar mensagens de 
    # volta.

    # recebe o JSON usando o protocolo correto
    try:
        if protocolo == 'tcp':
            payload = sock.recv(buffer)
            if not payload:
                return None, None
            oponente_addr = None
        else:
            payload, oponente_addr = sock.recvfrom(buffer)

        # decodifica o JSON em um dicionário python
        dados = json.loads(payload.decode('utf-8'))
        return dados, oponente_addr
    except (socket.error, json.JSONDecodeError, ConnectionResetError) as e:
        print(f"Erro ao receber dados. {e}")
        return None, None

def estabelecerConexaoInicial(cargo, protocolo, porta, host, tela, largura, fonte, clock, estado_jogo, lock):
    sock = criarSocket(host, protocolo)
    conexao_info = {"thread": None, "conexao": sock, "endereco": None, "conectado": False, "erro": None}

    args_conexao = (conexao_info, cargo, sock, host, porta, protocolo)
    conexao_info["thread"] = Thread(target=thread_conectar, args=args_conexao, daemon=True)
    conexao_info["thread"].start()

    status_info = {"titulo": "Aguardando conexão..."}
    botao_comecar = gui.Botao(largura//2 - 100, 350, 200, 50, "COMEÇAR", fonte, (255, 255, 255), (0, 150, 0), (148, 236, 162))

    esperando_inicio = True
    while esperando_inicio:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                estado_jogo["rodando"] = False
                esperando_inicio = False
            if conexao_info["conectado"] and cargo == "host":
                if botao_comecar.is_clicked(event):
                    enviarDados(conexao_info["conexao"], {"controle": "start"}, protocolo, conexao_info["endereco"])
                    estado_jogo["jogo_iniciado"] = True
                    esperando_inicio = False

        if not estado_jogo["rodando"]: break
        
        if conexao_info["erro"]:
            status_info["titulo"] = "Erro na conexão"
            status_info["info_extra"] = conexao_info["erro"]
        elif conexao_info["conectado"]:
            status_info["titulo"] = f"Conectado a {conexao_info['endereco'][0]}:{conexao_info['endereco'][1]}"
            status_info["info_extra"] = f"Utilizando {protocolo.upper()}"
            if cargo == "host":
                status_info["botao"] = botao_comecar
            else:
                status_info["prompt"] = "Aguardando o host iniciar a partida..."
                pronto_para_ler, _, _ = select([conexao_info["conexao"]], [], [], 0)
                if pronto_para_ler:
                    dados, _ = receberDados(conexao_info["conexao"], protocolo)
                    if dados and dados.get("controle") == "start":
                        with lock:
                            estado_jogo["jogo_iniciado"] = True
                        esperando_inicio = False
        
        gui.menuIntermediario(tela, largura, fonte, status_info)
        pygame.display.flip()
        clock.tick(30)
    
    return sock, conexao_info