from pong import *
from rede import *
import threading
pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pong")
CLOCK = pygame.time.Clock()

bola = circulo(LARGURA//2, ALTURA//2, 7)
raqueteOponente = retangulo(LARGURA-RAQUETE_LARGURA-20, (ALTURA-RAQUETE_ALTURA)/2, 
                           RAQUETE_LARGURA, RAQUETE_ALTURA)
raqueteJogador = retangulo(20, (ALTURA-RAQUETE_ALTURA)/2, 
                            RAQUETE_LARGURA, RAQUETE_ALTURA)

XVALUE = 0
YVALUE = 1

velocidadeBolaYMinima = 3
velocidadeBolaYMaxima = 12

score = 0
oponenteScore = 0

#--- Conexão Inicial ---

cargo = input("Criar(c) uma partida ou entrar(e) em uma? (c/e): ")
tipoIP = input("Qual a família IP da sala? (ipv4/ipv6): ")
protocolo = input("Qual o protocolo da sala? (tcp/udp): ")
porta = int(input("Qual a porta da sala?(ex.: 12345): "))

if cargo == "c":
    host = "0.0.0.0" if tipoIP == "ipv4" else "::"
else:
    #host = input(f"Qual o {tipoIP.upper()} da sala?: ")
    host = "127.0.0.1"

sock = criarSocket(host, protocolo)
conexao = sock

if cargo == "c": # host
    sock.bind((host, porta))
    if protocolo == "tcp":
        sock.listen(1)
        conexao, endereco = sock.accept()
        conexao.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        # diminui o delay do tcp
        a, b = endereco
        print(f"Conectado a {a}:{b}.") 
    else:
        dados, endereco = receberDados(conexao, protocolo)
        print(dados["teste"])
        if endereco:
            a, b = endereco
            print(f"Conectado a {a}:{b}.")
else: # cliente
    endereco = (host, porta)
    if protocolo == "tcp":
        sock.connect(endereco)
    else:
        enviarDados(conexao, {"teste":"teste"}, protocolo, endereco)
    print(f"Conectado a {host}:{porta}.")

rodando = True

lock = threading.Lock()

# --- Thread de Recebimento ---
def receberEstado():
    global rodando
    global estado
    while rodando:
        dados, endereco = receberDados(conexao, protocolo)
        with lock:
            raqueteOponente.y = dados["y"]
            if cargo == "e":
                bola.x = dados["bolax"]
                bola.y = dados["bolay"]
# --- Thread de Envio ---
def enviarEstado():
    global rodando
    while rodando:
        if cargo == "c":
            enviarDados(conexao, {
                                "y":raqueteJogador.y,
                                "bolax":int(LARGURA-bola.x),
                                "bolay":int(bola.y)
                                }, 
                                protocolo, endereco)
        else:
            enviarDados(conexao, {"y":raqueteJogador.y}, protocolo, endereco)

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
    movendo = 0
    if teclas[pygame.K_UP] and raqueteJogador.y > 0: 
        raqueteJogador.y -= VELOCIDADE_RAQUETE
        movendo = -1
    if teclas[pygame.K_DOWN] and ((raqueteJogador.y+raqueteJogador.altura) < ALTURA):
        raqueteJogador.y += VELOCIDADE_RAQUETE
        movendo = 1

    bola.x += velocidadeBola[XVALUE]
    bola.y += velocidadeBola[YVALUE]

    # colisão
    if cargo == "c":
        if bola.x < 55 or bola.x > LARGURA-55:
            # o número mágico (55) vem do fato de que a bola tem que estar pelo menos
            # a uma distância de
            # 20 (raquete até parede) + 20 (largura da raquete) + 14 (diametro da bola)
            # isso dá 54, aí eu adicionei 1 por desencargo de consciência.
            # Vai que o código quebra, sla.
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