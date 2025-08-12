import pygame

#Classe de botões, para criar botões na interface
class Botao:
    #Inicializa o botão e seus parâmetros
    def __init__(self, x, y, largura, altura, texto, fonte, texto_cor, fundo_cor, hover_cor):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.fonte = fonte
        self.hover_cor = hover_cor
        self.texto_cor = texto_cor
        self.fundo_cor = fundo_cor

    #Desenha o botão na tela
    def draw_button(self, superficie):
        mouse_pos = pygame.mouse.get_pos()
        cor = self.hover_cor if self.rect.collidepoint(mouse_pos) else self.fundo_cor
        pygame.draw.rect(superficie, cor, self.rect)

        texto_renderizado = self.fonte.render(self.texto, True, self.texto_cor)
        texto_rect = texto_renderizado.get_rect(center=self.rect.center)
        superficie.blit(texto_renderizado, texto_rect)

    #Registra se o botão foi clicado
    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )
    
#Função para executar o menu
def menu_principal(tela, largura, altura):
    fonte = pygame.font.Font(None, 40)
    fonte_titulo = pygame.font.Font(None, 80)

    titulo = "PONG ONLINE"
    titulo_cor = (255, 255, 255)
    titulo_superficie = fonte_titulo.render(titulo, True, titulo_cor)

    titulo_rect = titulo_superficie.get_rect()
    titulo_rect.center = (largura//2, altura//4)

    # Criar botões
    botao_host = Botao(300, 400, 200, 50, "CRIAR SALA", fonte, (255, 255, 255), (0, 0, 0), (148, 236, 162))
    botao_conect = Botao(300, 200, 200, 50, "CONECTAR", fonte, (255, 255, 255), (0, 0, 0), (148, 193, 236))
    botao_sair = Botao(300, 300, 200, 50, "SAIR", fonte, (255, 255, 255), (0, 0, 0), (236, 148, 148))

    
    while True:
        tela.fill((30, 30, 30))  # Fundo
        tela.blit(titulo_superficie, titulo_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if botao_conect.is_clicked(event):
                menu_conexao(tela, largura, altura)

            if botao_sair.is_clicked(event):
                pygame.quit()
                exit()

        #Desenha os botões
        botao_conect.draw_button(tela)
        botao_sair.draw_button(tela)
        botao_host.draw_button(tela)

        pygame.display.flip()

#Menu de conexão
def menu_conexao(tela, largura, altura):
    fonte = pygame.font.Font(None, 40)
    fonte_titulo = pygame.font.Font(None, 80)

    titulo = "PONG ONLINE"
    titulo_superficie = fonte_titulo.render(titulo, True, (255, 255, 255))

    titulo_rect = titulo_superficie.get_rect()
    titulo_rect.center = (largura//2, altura//4)

    # Criar botões
    botao_TCP = Botao(150, 250, 200, 50, "TCP", fonte, (255, 255, 255), (0, 0, 0), (148, 193, 236))
    botao_UDP = Botao(450, 250, 200, 50, "UDP", fonte, (255, 255, 255), (0, 0, 0), (148, 193, 236))

    
    while True:
        tela.fill((30, 30, 30))  # Fundo
        tela.blit(titulo_superficie, titulo_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if botao_TCP.is_clicked(event):
                pygame.quit()
                exit()

            if botao_UDP.is_clicked(event):
                pygame.quit()
                exit()

        #Desenha os botões
        botao_TCP.draw_button(tela)
        botao_UDP.draw_button(tela)

        pygame.display.flip()
