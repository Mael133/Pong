import select
import time
import rede
import json
from pong import LARGURA

def receberEstado(conexao, protocolo, estado_jogo, lock, cargo):
    # cria o buffer para as mensagens tcp
    buffer_tcp = b""

    while estado_jogo["rodando"]:
        # Usa select para não bloquear a thread indefinidamente
        pronto_para_ler, _, _ = select.select([conexao], [], [], 0.1)
        if not pronto_para_ler:
            continue

        if protocolo == "tcp":
            # 1. Recebe dados brutos e adiciona ao buffer
            dados_brutos = conexao.recv(1024)
            if not dados_brutos: # Conexão foi fechada pelo outro lado
                print("Conexão encerrada pelo oponente.")
                estado_jogo["rodando"] = False
                break
            
            buffer_tcp += dados_brutos
            # Divide o buffer em pacotes usando o delimitador '\n'
            pacotes = buffer_tcp.split(b'\n')
            if len(pacotes) > 1:
                # O penúltimo item da lista é o último pacote completo recebido
                ultimo_pacote_completo = pacotes[-2]
                # O último item é o que sobrou (um pacote parcial ou vazio)
                buffer_tcp = pacotes[-1]
                if ultimo_pacote_completo:
                    dados = json.loads(ultimo_pacote_completo.decode('utf-8'))
                    # Lógica de processamento do pacote
                    with lock:
                        if cargo == "cliente":
                            if "bolax" in dados: estado_jogo["bola_x"] = dados["bolax"]
                            if "bolay" in dados: estado_jogo["bola_y"] = dados["bolay"]
                            if "score_jogador" in dados: estado_jogo["score_jogador"] = dados["score_oponente"]
                            if "score_oponente" in dados: estado_jogo["score_oponente"] = dados["score_jogador"]
                        
                        if "y" in dados: estado_jogo["raqueteOponente_y"] = dados["y"]
                        if dados.get("controle") == "sair":
                            estado_jogo["rodando"] = False
                            break
        else: # Lógica para UDP
            dados, _ = rede.receberDados(conexao, protocolo)
            if dados:
                with lock:
                    if cargo == "cliente":
                        if "bolax" in dados: estado_jogo["bola_x"] = dados["bolax"]
                        if "bolay" in dados: estado_jogo["bola_y"] = dados["bolay"]
                        if "score_jogador" in dados: estado_jogo["score_jogador"] = dados["score_oponente"]
                        if "score_oponente" in dados: estado_jogo["score_oponente"] = dados["score_jogador"]
                    
                    if "y" in dados: estado_jogo["raqueteOponente_y"] = dados["y"]
                    if dados.get("controle") == "sair":
                        estado_jogo["rodando"] = False
                        break

def enviarEstado(conexao, protocolo, endereco, cargo, estado_jogo, lock):
    while estado_jogo["rodando"]:
        with lock:
            dados_para_enviar = {"y": estado_jogo["raqueteJogador_y"]}
            # O host é a autoridade e envia o estado completo do jogo
            if cargo == "host":
                # Inverte a coordenada X da bola para a perspectiva do cliente
                dados_para_enviar["bolax"] = int(LARGURA - estado_jogo["bola_x"])
                dados_para_enviar["bolay"] = int(estado_jogo["bola_y"])
                dados_para_enviar["score_jogador"] = estado_jogo["score_jogador"]
                dados_para_enviar["score_oponente"] = estado_jogo["score_oponente"]
        
        rede.enviarDados(conexao, dados_para_enviar, protocolo, endereco)
        time.sleep(1/60) # Envia em uma taxa de 60Hz

    # Ao sair do loop, envia uma última mensagem para notificar o oponente
    rede.enviarDados(conexao, {"controle": "sair"}, protocolo, endereco)

def thread_conectar(conexao_info, cargo, sock, host, porta, protocolo):
    try:
        if cargo == "host":
            sock.bind((host, porta))
            if protocolo == "tcp":
                sock.listen(1)
                conexao, endereco = sock.accept()
                conexao_info["conexao"] = conexao
                conexao_info["endereco"] = endereco
            else: # udp
                # Espera a primeira mensagem do cliente para obter seu endereço
                _, endereco = sock.recvfrom(1024)
                conexao_info["endereco"] = endereco
        else: # cliente
            endereco = (host, porta)
            if protocolo == "tcp":
                sock.connect(endereco)
            else: # udp
                # Envia uma mensagem inicial para que o host saiba o endereço do cliente
                sock.sendto(b'connect', endereco)
            conexao_info["endereco"] = endereco
        
        # Sinaliza que a conexão foi bem-sucedida
        conexao_info["conectado"] = True
    except Exception as e:
        print(f"Erro na conexão: {e}")
        conexao_info["erro"] = str(e)