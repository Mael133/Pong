from pong import *
from rede import *
import threading
import gui
import threads 
import math

# --- Configurações iniciais ---
pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pong")
CLOCK = pygame.time.Clock()
fonte = pygame.font.Font(None, 40)

# --- Constantes do Jogo ---
PONTUACAO_MAXIMA = 400
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
    "jogo_iniciado": False
}
lock = threading.Lock()

# --- Função Principal ---
def main():
    # --- Menu de configuração inicial ---
    cargo, protocolo, porta, host = gui.configuracaoInicial(tela, fonte, LARGURA)

    # --- Conexão inicial ---
    sock, conexao_info = estabelecerConexaoInicial(cargo, protocolo, porta, host, tela, LARGURA, fonte, CLOCK, estado_jogo, lock)

    if not estado_jogo["rodando"] or not estado_jogo["jogo_iniciado"]:
        sock.close()
        pygame.quit()
        return

    # --- Inicialização das Threads ---
    conexao = conexao_info["conexao"]
    endereco = conexao_info["endereco"]
    if protocolo == "tcp":
        conexao.setblocking(False)
        if cargo == "host":
            conexao.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    threadRecebimento = threading.Thread(target=threads.receberEstado, args=(conexao, protocolo, estado_jogo, lock, cargo), daemon=True)
    threadEnvio = threading.Thread(target=threads.enviarEstado, args=(conexao, protocolo, endereco, cargo, estado_jogo, lock), daemon=True)
    
    threadRecebimento.start()
    threadEnvio.start()
    
    # --- Início do jogo e loop principal ---
    bola = circulo(LARGURA//2, ALTURA//2, BOLA_RAIO)
    raqueteJogador = retangulo(ESPACAMENTOPAREDE, (ALTURA-RAQUETE_ALTURA)/2, RAQUETE_LARGURA, RAQUETE_ALTURA)
    raqueteOponente = retangulo(LARGURA-RAQUETE_LARGURA-ESPACAMENTOPAREDE, (ALTURA-RAQUETE_ALTURA)/2, RAQUETE_LARGURA, RAQUETE_ALTURA)
    velocidadeBola = np.array(VELOCIDADE_INICIAL_BOLA)
    fonte_score = pygame.font.Font(None, 74)

    while estado_jogo["rodando"]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                estado_jogo["rodando"] = False
                return
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

                distanciaMinimaParaColisao = ESPACAMENTOPAREDE + RAQUETE_LARGURA + BOLA_RAIO + abs(velocidadeBola[XVALUE])
                if bola.x <= distanciaMinimaParaColisao or bola.x >= (LARGURA - distanciaMinimaParaColisao):
                    if colisao(bola.x, bola.y, raqueteJogador) or colisao(bola.x, bola.y, raqueteOponente):
                        while colisao(bola.x, bola.y, raqueteJogador) or colisao(bola.x, bola.y, raqueteOponente):
                            bola.x -= math.copysign(1, velocidadeBola[XVALUE])
                            bola.y -= math.copysign(1, velocidadeBola[YVALUE])
                        if bola.x < (ESPACAMENTOPAREDE + RAQUETE_LARGURA) or bola.x > (LARGURA - ESPACAMENTOPAREDE - RAQUETE_LARGURA):
                             velocidadeBola[YVALUE] *= -1
                        else:
                             velocidadeBola[XVALUE] *= -1

                if bola.y <= 0 or bola.y >= ALTURA:
                    velocidadeBola[YVALUE] *= -1

                ponto_marcado = False
                if bola.x <= 0:
                    estado_jogo["score_oponente"] += 1
                    ponto_marcado = True
                elif bola.x >= LARGURA:
                    estado_jogo["score_jogador"] += 1
                    ponto_marcado = True
                
                if ponto_marcado:
                    bola.x, bola.y = LARGURA/2, ALTURA/2
                    velocidadeBola[YVALUE] = VELOCIDADE_INICIAL_BOLA[YVALUE]
                    velocidadeBola[XVALUE] *= -1

                estado_jogo["bola_x"], estado_jogo["bola_y"] = bola.x, bola.y

                if estado_jogo["score_jogador"] >= PONTUACAO_MAXIMA or estado_jogo["score_oponente"] >= PONTUACAO_MAXIMA:
                    estado_jogo["rodando"] = False

        tela.fill(COR_FUNDO)

        largura_traco = 5
        altura_traco = 20
        espaco_vazio = 15
        cor_linha = (128, 128, 128) # Um cinza para não distrair tanto

        for y in range(0, ALTURA, altura_traco + espaco_vazio):
            traco = pygame.Rect(LARGURA // 2 - largura_traco // 2, y, largura_traco, altura_traco)
            pygame.draw.rect(tela, cor_linha, traco)

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

    # --- Fim De Jogo ---
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
    
    if sock: sock.close()
    pygame.quit()

if __name__ == '__main__':
    main()