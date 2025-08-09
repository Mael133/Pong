from pong import *

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

rodando = True
while rodando:
    # --- Entradas ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    teclas = pygame.key.get_pressed()

    # --- Logica ---

    # mover raquete
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

    if bola.y <= 0 or bola.y >= ALTURA: 
        velocidadeBola[YVALUE] *= -1

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


    # mover bola


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

pygame.quit()
