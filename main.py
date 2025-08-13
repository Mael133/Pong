from pong import *
from rede import *
import threading
import gui
import time

# Configurações iniciais
pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pong")
CLOCK = pygame.time.Clock()
fonte = pygame.font.Font(None, 40)

# cria o estado inicial do jogo
bola = circulo(LARGURA//2, ALTURA//2, 7)
raqueteOponente = retangulo(LARGURA-RAQUETE_LARGURA-ESPACAMENTOPAREDE, (ALTURA-RAQUETE_ALTURA)/2, 
                           RAQUETE_LARGURA, RAQUETE_ALTURA)
raqueteJogador = retangulo(ESPACAMENTOPAREDE, (ALTURA-RAQUETE_ALTURA)/2, 
                            RAQUETE_LARGURA, RAQUETE_ALTURA)

XVALUE = 0
YVALUE = 1

velocidadeBolaYMinima = 3
velocidadeBolaYMaxima = 12

score = 0
oponenteScore = 0

#--- Conexão Inicial ---

# pegar os dados necessários

cargo = gui.menuInput(tela, LARGURA, fonte, "PONG ONLINE",[
                    gui.Botao(300, 250, 200, 50, "CRIAR SALA", fonte, (255, 255, 255), (0, 0, 0), (148, 236, 162)),
                    gui.Botao(300, 350, 200, 50, "CONECTAR", fonte, (255, 255, 255), (0, 0, 0), (148, 193, 236)),
                    gui.Botao(300, 450, 200, 50, "SAIR", fonte, (255, 255, 255), (0, 0, 0), (236, 148, 148))])
protocolo = gui.menuInput(tela, LARGURA, fonte, "QUAL O PROTOCOLO DA SALA?",[
                    gui.Botao(150, 250, 200, 50, "TCP", fonte, (255, 255, 255), (0, 0, 0), (148, 236, 162)),
                    gui.Botao(450, 250, 200, 50, "UDP", fonte, (255, 255, 255), (0, 0, 0), (148, 193, 236))])
tipoIP = gui.menuInput(tela, LARGURA, fonte, "QUAL O TIPO IP DA SALA?",[
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

pygame.display.set_caption(cargo)

# criar o socket e efetivar a conexão
sock = criarSocket(host, protocolo)
conexao = sock

if cargo == "host": # host
    sock.bind((host, porta))
    if protocolo == "tcp":
        sock.listen(1)
        conexao, endereco = sock.accept()
        conexao.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # diminui o delay do tcp
        a, b = endereco
    else:
        dados, endereco = receberDados(conexao, protocolo)
        if endereco:
            a, b = endereco
    print(f"Conectado a {a}:{b} utilizando {protocolo}.") 
else: # cliente
    endereco = (host, porta)
    if protocolo == "tcp":
        sock.connect(endereco)
    else:
        enviarDados(conexao, {}, protocolo, endereco)
    print(f"Conectado a {host}:{porta} utilizando {protocolo}.")

rodando = True

lock = threading.Lock()

# --- Thread de Recebimento ---
def receberEstado():
    global rodando
    global estado
    while rodando:
        dados, _ = receberDados(conexao, protocolo)
        # quando usando tcp, os usuários podem dessincronizar,
        # fazendo com que as mensagens se misturem uma com a outra,
        # então função receberDados dá erro na leitura, e isso faz 
        # com que crashe o programa quando modificando os dados.   
        if dados:
            with lock:
                raqueteOponente.y = dados["y"]
                if cargo == "cliente":
                    bola.x = dados["bolax"]
                    bola.y = dados["bolay"]
            time.sleep(1/60)

# --- Thread de Envio ---
def enviarEstado():
    global rodando
    while rodando:
        with lock:
            if cargo == "host":
                enviarDados(conexao, {
                                    "y":raqueteJogador.y,
                                    "bolax":int(LARGURA-bola.x),
                                    "bolay":int(bola.y)
                                    }, 
                                    protocolo, endereco)
            else:
                enviarDados(conexao, {"y":raqueteJogador.y}, protocolo, endereco)
        time.sleep(1/60)

# inicia as threads
threadRecebimento = threading.Thread(target=receberEstado)
threadEnvio       = threading.Thread(target=enviarEstado)
threadRecebimento.start()
threadEnvio.start()

# --- Loop Principal ---

while rodando:
    # --- Entradas ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    teclas = pygame.key.get_pressed()

    # --- Logica ---
    # mover objetos
    if teclas[pygame.K_UP] and raqueteJogador.y > 0: 
        raqueteJogador.y -= VELOCIDADE_RAQUETE
    if teclas[pygame.K_DOWN] and ((raqueteJogador.y+raqueteJogador.altura) < ALTURA):
        raqueteJogador.y += VELOCIDADE_RAQUETE

    if cargo == "host":
        with lock:
            bola.x += velocidadeBola[XVALUE]
            bola.y += velocidadeBola[YVALUE]

            distanciaMinimaParaColisao = ESPACAMENTOPAREDE + RAQUETE_LARGURA + BOLA_RAIO
            # a bola só pode colidor com algo lateralente se 
            # tiver a pelo menos essa distancia da parede 

            # colisão
            if bola.x < distanciaMinimaParaColisao+1 or bola.x > LARGURA-distanciaMinimaParaColisao-1:
                # O mais ou menos 1 é pra  garantir que em cenários
                # de colisão de quina a bola não entre nas raquetes

                if colisao(bola.x, bola.y, raqueteJogador
                ) or colisao(bola.x, bola.y, raqueteOponente): 
                    bola.x -= velocidadeBola[XVALUE]
                    bola.y -= velocidadeBola[YVALUE]
                    if bola.x < (20+raqueteOponente.largura) or bola.x > (LARGURA-20-raqueteOponente.largura):
                        velocidadeBola[YVALUE] *= -1
                    else:
                        velocidadeBola[XVALUE] *= -1

                # a colisão com a parede lateral também só é possível a partir desse ponto, então
                # não custa nada colocar essa colisão dentro dessa condição também, e salva
                # recursos em não checar esses valores todo frame
                if bola.x+velocidadeBola[XVALUE] <= 0:
                    velocidadeBola = (VELOCIDADE_INICIAL_BOLA*-1).copy()
                    bola.x = LARGURA/2
                    bola.y = ALTURA/2
                    velocidadeBola[XVALUE] *= -1
                elif bola.x+velocidadeBola[XVALUE] >= LARGURA:
                    velocidadeBola = VELOCIDADE_INICIAL_BOLA.copy()
                    bola.x = LARGURA/2
                    bola.y = ALTURA/2
                    velocidadeBola[XVALUE] *= -1

            if bola.y <= 0 or bola.y >= ALTURA: 
                velocidadeBola[YVALUE] *= -1

    # --- Construção da tela ---
    tela.fill(COR_FUNDO)
    pygame.draw.circle(tela, COR_OBJETOS, (bola.x, bola.y), bola.raio)
    pygame.draw.rect(tela, COR_OBJETOS, 
    (raqueteJogador.x, raqueteJogador.y, raqueteJogador.largura, raqueteJogador.altura))
    pygame.draw.rect(tela, COR_OBJETOS, 
    (raqueteOponente.x, raqueteOponente.y, raqueteOponente.largura, raqueteOponente.altura))

    # --- Atualiza a Tela ---
    pygame.display.flip()
    CLOCK.tick(60)


threadRecebimento.join()
threadEnvio.join()

rodando = False
pygame.quit()
sock.close()