from pong import *

pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pong")
CLOCK = pygame.time.Clock()

bola = circulo(LARGURA//2, ALTURA//2, 7)
raqueteJogador = retangulo(LARGURA-60, (ALTURA-200)/2, 40, 200)
raqueteOponente = retangulo(20, (ALTURA-200)/2, 40, 200)


jogo = {
    "ballVelX":6,
    "ballVelY":6,
    "ballX": LARGURA//2,
    "ballY": ALTURA//2,
    "oponentY": ALTURA//2,
    "selfY": ALTURA//2
}

rodando = True
while rodando:
    # --- Entradas ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
    teclas = pygame.key.get_pressed()

    # --- Logica ---
    if teclas[pygame.K_UP]: 
        bola.y -= VELOCIDADE_INICIAL_BOLA
    if teclas[pygame.K_DOWN]:
        bola.y += VELOCIDADE_INICIAL_BOLA
    if teclas[pygame.K_LEFT]:
        bola.x -= VELOCIDADE_INICIAL_BOLA
    if teclas[pygame.K_RIGHT]:
        bola.x += VELOCIDADE_INICIAL_BOLA
    
    cor = BRANCO
    if colisao(bola, raqueteJogador):
        cor = (255,0,0)
    

    # --- Construção da tela ---
    tela.fill(COR_FUNDO)
    pygame.draw.circle(tela, cor, (bola.x, bola.y), bola.raio)
    pygame.draw.rect(tela, cor, raqueteJogador.rect)
    #pygame.draw.rect(tela, BRANCO, raqueteOponente.rect)


    # --- Atualiza a Tela ---
    pygame.display.flip()
    CLOCK.tick(60)

pygame.quit()
