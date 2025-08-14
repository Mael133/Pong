from pong import *
from rede import *
import threading
import gui
import time
import select

# Configurações iniciais
pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pong")
CLOCK = pygame.time.Clock()
fonte = pygame.font.Font(None, 40)

# --- Constantes do Jogo ---
PONTUACAO_MAXIMA = 20
XVALUE = 0
YVALUE = 1

# --- Estado do Jogo (compartilhado entre threads) ---
estado_jogo = {
    "raqueteJogador_y": (ALTURA - RAQUETE_ALTURA) / 2,
    "raqueteOponente_y": (ALTURA - RAQUETE_ALTURA) / 2,
    "bola_x": LARGURA // 2,
    "bola_y": ALTURA // 2,
    "score_jogador": 0,
    "score_oponente": 0,
    "rodando": True,
    "jogo_iniciado": False,
}
lock = threading.Lock()

# --- Funções de Rede (Threads) ---
def receberEstado(conexao, protocolo):
    global estado_jogo
    while estado_jogo["rodando"]:
        pronto_para_ler, _, _ = select.select([conexao], [], [], 0.1)
        if not pronto_para_ler:
            continue

        dados, _ = receberDados(conexao, protocolo)
        if dados:
            with lock:
                if dados.get("controle") == "start":
                    estado_jogo["jogo_iniciado"] = True
                
                if "y" in dados:
                    estado_jogo["raqueteOponente_y"] = dados["y"]

                if cargo == "cliente":
                    if "bolax" in dados:
                        estado_jogo["bola_x"] = dados["bolax"]
                    if "bolay" in dados:
                        estado_jogo["bola_y"] = dados["bolay"]
                    if "score_jogador" in dados:
                        estado_jogo["score_jogador"] = dados["score_oponente"]
                    if "score_oponente" in dados:
                        estado_jogo["score_oponente"] = dados["score_jogador"]

                if dados.get("controle") == "sair":
                    estado_jogo["rodando"] = False
                    break
        else: 
            print("Conexão perdida.")
            estado_jogo["rodando"] = False
            break

def enviarEstado(conexao, protocolo, endereco, cargo):
    while estado_jogo["rodando"]:
        with lock:
            dados_para_enviar = {"y": estado_jogo["raqueteJogador_y"]}
            if cargo == "host":
                dados_para_enviar["bolax"] = int(LARGURA - estado_jogo["bola_x"])
                dados_para_enviar["bolay"] = int(estado_jogo["bola_y"])
                dados_para_enviar["score_jogador"] = estado_jogo["score_jogador"]
                dados_para_enviar["score_oponente"] = estado_jogo["score_oponente"]
        
        enviarDados(conexao, dados_para_enviar, protocolo, endereco)
        time.sleep(1/60)

    enviarDados(conexao, {"controle": "sair"}, protocolo, endereco)

# --- Função Principal ---
def main():
    global cargo

    # menu inicial e configuração
    cargo = gui.menuInput(tela, LARGURA, fonte, "PONG ONLINE", [
                        gui.Botao(300, 250, 200, 50, "CRIAR SALA", fonte, (255, 255, 255), (0, 0, 0), (148, 236, 162)),
                        gui.Botao(300, 350, 200, 50, "CONECTAR", fonte, (255, 255, 255), (0, 0, 0), (148, 193, 236)),
                        gui.Botao(300, 450, 200, 50, "SAIR", fonte, (255, 255, 255), (0, 0, 0), (236, 148, 148))])
    protocolo = gui.menuInput(tela, LARGURA, fonte, "QUAL O PROTOCOLO?", [
                        gui.Botao(150, 250, 200, 50, "TCP", fonte, (255, 255, 255), (0, 0, 0), (148, 236, 162)),
                        gui.Botao(450, 250, 200, 50, "UDP", fonte, (255, 255, 255), (0, 0, 0), (148, 193, 236))])
    tipoIP = gui.menuInput(tela, LARGURA, fonte, "QUAL O TIPO DE IP?", [
                        gui.Botao(150, 250, 200, 50, "IPV4", fonte, (255, 255, 255), (0, 0, 0), (148, 236, 162)),
                        gui.Botao(450, 250, 200, 50, "IPV6", fonte, (255, 255, 255), (0, 0, 0), (148, 193, 236))])
    porta = int(gui.menuInput(tela, LARGURA, fonte, "QUAL A PORTA DA SALA?",
                    [gui.Botao(300, 350, 200, 50, "CONFIRMAR", fonte, (255, 255, 255), (0, 0, 0), (148, 236, 162))],
                    gui.caixaDeTexto(150, 250, 500, 50, fonte, (255, 255, 255))))
    if cargo == "host":
        host = "0.0.0.0" if tipoIP == "ipv4" else "::"
    else:
        host = gui.menuInput(tela, LARGURA, fonte, "QUAL O IP DA SALA?",
                    [gui.Botao(300, 350, 200, 50, "CONFIRMAR", fonte, (255, 255, 255), (0, 0, 0), (148, 236, 162))],
                    gui.caixaDeTexto(150, 250, 500, 50, fonte, (255, 255, 255)))

    # tela intermediária e conexão
    sock = criarSocket(host, protocolo)
    conexao_info = {"thread": None, "conexao": sock, "endereco": None, "conectado": False, "erro": None}

    def thread_conectar():
        try:
            if cargo == "host":
                sock.bind((host, porta))
                if protocolo == "tcp":
                    sock.listen(1)
                    conexao, endereco = sock.accept()
                    conexao_info["conexao"] = conexao
                    conexao_info["endereco"] = endereco
                else: 
                    _, endereco = sock.recvfrom(1024)
                    conexao_info["endereco"] = endereco
            else: 
                endereco = (host, porta)
                if protocolo == "tcp":
                    sock.connect(endereco)
                else:
                    sock.sendto(b'connect', endereco)
                conexao_info["endereco"] = endereco
            conexao_info["conectado"] = True
        except Exception as e:
            conexao_info["erro"] = str(e)

    conexao_info["thread"] = threading.Thread(target=thread_conectar, daemon=True)
    conexao_info["thread"].start()

    status_info = {"titulo": "Aguardando conexão..."}
    botao_comecar = gui.Botao(LARGURA//2 - 100, 350, 200, 50, "COMEÇAR", fonte, (255, 255, 255), (0, 150, 0), (148, 236, 162))

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
                pronto_para_ler, _, _ = select.select([conexao_info["conexao"]], [], [], 0)
                if pronto_para_ler:
                    dados, _ = receberDados(conexao_info["conexao"], protocolo)
                    if dados and dados.get("controle") == "start":
                        with lock:
                            estado_jogo["jogo_iniciado"] = True
                        esperando_inicio = False
        
        gui.menuIntermediario(tela, LARGURA, fonte, status_info)
        pygame.display.flip()
        CLOCK.tick(30)

    if not estado_jogo["rodando"] or not estado_jogo["jogo_iniciado"]:
        sock.close()
        pygame.quit()
        return

    # icicialização das threads
    conexao = conexao_info["conexao"]
    endereco = conexao_info["endereco"]
    if protocolo == "tcp":
        conexao.setblocking(False)
        if cargo == "host":
            conexao.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    threadRecebimento = threading.Thread(target=receberEstado, args=(conexao, protocolo), daemon=True)
    threadEnvio = threading.Thread(target=enviarEstado, args=(conexao, protocolo, endereco, cargo), daemon=True)
    threadRecebimento.start()
    threadEnvio.start()
    
    bola = circulo(LARGURA//2, ALTURA//2, BOLA_RAIO)
    raqueteJogador = retangulo(ESPACAMENTOPAREDE, (ALTURA-RAQUETE_ALTURA)/2, RAQUETE_LARGURA, RAQUETE_ALTURA)
    raqueteOponente = retangulo(LARGURA-RAQUETE_LARGURA-ESPACAMENTOPAREDE, (ALTURA-RAQUETE_ALTURA)/2, RAQUETE_LARGURA, RAQUETE_ALTURA)
    velocidadeBola = np.array(VELOCIDADE_INICIAL_BOLA)
    fonte_score = pygame.font.Font(None, 74)

    # --- Loop Principal ---
    while estado_jogo["rodando"]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                estado_jogo["rodando"] = False
        teclas = pygame.key.get_pressed()

        with lock:
            if teclas[pygame.K_UP] and estado_jogo["raqueteJogador_y"] > 0:
                estado_jogo["raqueteJogador_y"] -= VELOCIDADE_RAQUETE
            if teclas[pygame.K_DOWN] and ((estado_jogo["raqueteJogador_y"] + RAQUETE_ALTURA) < ALTURA):
                estado_jogo["raqueteJogador_y"] += VELOCIDADE_RAQUETE

            raqueteJogador.y = estado_jogo["raqueteJogador_y"]
            raqueteOponente.y = estado_jogo["raqueteOponente_y"]
            bola.x = estado_jogo["bola_x"]
            bola.y = estado_jogo["bola_y"]
            
            if cargo == "host":
                bola.x += velocidadeBola[XVALUE]
                bola.y += velocidadeBola[YVALUE]

                if colisao(bola.x, bola.y, raqueteJogador) or colisao(bola.x, bola.y, raqueteOponente):
                    velocidadeBola[XVALUE] *= -1
                
                if bola.y - BOLA_RAIO <= 0 or bola.y + BOLA_RAIO >= ALTURA:
                    velocidadeBola[YVALUE] *= -1

                ponto_marcado = False
                if bola.x - BOLA_RAIO <= 0:
                    estado_jogo["score_oponente"] += 1
                    ponto_marcado = True
                elif bola.x + BOLA_RAIO >= LARGURA:
                    estado_jogo["score_jogador"] += 1
                    ponto_marcado = True
                
                if ponto_marcado:
                    bola.x, bola.y = LARGURA/2, ALTURA/2
                    velocidadeBola = np.array(VELOCIDADE_INICIAL_BOLA)
                    if np.random.rand() < 0.5: velocidadeBola[XVALUE] *= -1

                estado_jogo["bola_x"], estado_jogo["bola_y"] = bola.x, bola.y

                if estado_jogo["score_jogador"] >= PONTUACAO_MAXIMA or estado_jogo["score_oponente"] >= PONTUACAO_MAXIMA:
                    estado_jogo["rodando"] = False

        tela.fill(COR_FUNDO)
        pygame.draw.circle(tela, COR_OBJETOS, (int(bola.x), int(bola.y)), bola.raio)
        pygame.draw.rect(tela, COR_OBJETOS, 
        (raqueteJogador.x, raqueteJogador.y, raqueteJogador.largura, raqueteJogador.altura))
        pygame.draw.rect(tela, COR_OBJETOS, 
        (raqueteOponente.x, raqueteOponente.y, raqueteOponente.largura, raqueteOponente.altura))

        score_texto = f"{estado_jogo['score_jogador']}    {estado_jogo['score_oponente']}"
        score_superficie = fonte_score.render(score_texto, True, BRANCO)
        score_rect = score_superficie.get_rect(center=(LARGURA//2, 50))
        tela.blit(score_superficie, score_rect)

        pygame.display.flip()
        CLOCK.tick(60)

    # --- Fim de Jogo ---
    threadEnvio.join(timeout=1)
    threadRecebimento.join(timeout=1)

    vencedor = "jogador" if estado_jogo["score_jogador"] >= PONTUACAO_MAXIMA else "oponente" if estado_jogo["score_oponente"] >= PONTUACAO_MAXIMA else None

    if (cargo == "host" and vencedor == "jogador") or (cargo == "cliente" and vencedor == "oponente"):
        mensagem_final = "Voce Venceu!"
    elif vencedor is not None:
        mensagem_final = "Voce Perdeu!"
    else:
        mensagem_final = "Jogo encerrado."

    botoes_fim = [gui.Botao(LARGURA//2 - 75, 350, 150, 50, "SAIR", fonte, (255, 255, 255), (0, 0, 0), (236, 148, 148))]
    gui.menuFimDeJogo(tela, LARGURA, fonte, mensagem_final, botoes_fim)
    
    sock.close()
    pygame.quit()

if __name__ == '__main__':
    main()