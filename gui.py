import pygame

# Classe de botões, para criar botões na interface
class Botao:
    # Inicializa o botão e seus parâmetros
    def __init__(self, x, y, largura, altura, texto, fonte, texto_cor, fundo_cor, hover_cor):
        self.rect = pygame.Rect(x, y, largura, altura)
        self.texto = texto
        self.fonte = fonte
        self.hover_cor = hover_cor
        self.texto_cor = texto_cor
        self.fundo_cor = fundo_cor

    # Desenha o botão na tela
    def draw(self, superficie):
        mouse_pos = pygame.mouse.get_pos()
        cor = self.hover_cor if self.rect.collidepoint(mouse_pos) else self.fundo_cor
        pygame.draw.rect(superficie, cor, self.rect)

        texto_renderizado = self.fonte.render(self.texto, True, self.texto_cor)
        texto_rect = texto_renderizado.get_rect(center=self.rect.center)
        superficie.blit(texto_renderizado, texto_rect)

    # Registra se o botão foi clicado
    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )

# Classe de caixas de texto, para criar caixas de texto na interface
class caixaDeTexto:
    # Inicializa a caixa e seus parâmetros
    def __init__(self, x, y, a, l, fonte, cor, texto=''):
        self.rect = pygame.Rect(x, y, a, l)
        self.cor = cor
        self.texto = texto
        self.fonte = fonte
        self.txt_surface = fonte.render(texto, True, self.cor)

    # Desenha a caixa na tela
    def draw(self, tela):
        tela.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        pygame.draw.rect(tela, self.cor, self.rect, 2)

def menuInput(tela, largura, fonte, titulo="", botoes=[], caixaTexto=None, ):
    fonte_titulo = pygame.font.Font(None, 74)

    titulo_cor = (255, 255, 255)
    titulo_superficie = fonte_titulo.render(titulo, True, titulo_cor)

    titulo_rect = titulo_superficie.get_rect()
    titulo_rect.center = (largura//2, 150)
    
    while True:
        tela.fill((30, 30, 30))  # Fundo
        tela.blit(titulo_superficie, titulo_rect)

        # Checa os eventos ocorridos e responde respectivamente
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if caixaTexto and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return caixaTexto.texto
                if event.key == pygame.K_BACKSPACE:
                    caixaTexto.texto = caixaTexto.texto[:-1]
                else:
                    caixaTexto.texto += event.unicode
                # redesenha o texto
                caixaTexto.txt_surface = caixaTexto.fonte.render(caixaTexto.texto, True, caixaTexto.cor)

            for botao in botoes:
                if botao.is_clicked(event):
                    if botao.texto == "SAIR":
                        pygame.quit()
                        exit()
                    elif botao.texto == "CRIAR SALA":
                        return "host"
                    elif botao.texto == "CONECTAR":
                        return "cliente"
                    elif botao.texto == "CONFIRMAR":
                        return caixaTexto.texto
                    return botao.texto.lower()

        #Desenha os elementos
        for botao in botoes:
            botao.draw(tela)
        if caixaTexto:
            caixaTexto.draw(tela)

        pygame.display.flip()

def menuIntermediario(tela, largura, fonte, status_info):
    tela.fill((30, 30, 30))  # Fundo

    fonte_titulo = pygame.font.Font(None, 60)
    fonte_info = pygame.font.Font(None, 32)
    titulo_cor = (255, 255, 255)
    info_cor = (200, 200, 200)

    # Desenha o título (status principal)
    titulo_superficie = fonte_titulo.render(status_info["titulo"], True, titulo_cor)
    titulo_rect = titulo_superficie.get_rect(center=(largura//2, 150))
    tela.blit(titulo_superficie, titulo_rect)

    # Desenha informações adicionais (IP, protocolo)
    if status_info.get("info_extra"):
        info_extra_superficie = fonte_info.render(status_info["info_extra"], True, info_cor)
        info_extra_rect = info_extra_superficie.get_rect(center=(largura//2, 220))
        tela.blit(info_extra_superficie, info_extra_rect)

    # Desenha o prompt/botão
    if status_info.get("prompt"):
        prompt_superficie = fonte_info.render(status_info["prompt"], True, info_cor)
        prompt_rect = prompt_superficie.get_rect(center=(largura//2, 425))
        tela.blit(prompt_superficie, prompt_rect)
    
    if status_info.get("botao"):
        status_info["botao"].draw(tela)

def menuFimDeJogo(tela, largura, fonte, mensagem, botoes):
    fonte_titulo = pygame.font.Font(None, 74)
    titulo_cor = (255, 255, 255)
    
    while True:
        tela.fill((30, 30, 30))  # Fundo

        # Renderizar mensagem de vitória/derrota
        titulo_superficie = fonte_titulo.render(mensagem, True, titulo_cor)
        titulo_rect = titulo_superficie.get_rect(center=(largura//2, 250))
        tela.blit(titulo_superficie, titulo_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "sair" # Sair por fechar a janela

            for botao in botoes:
                if botao.is_clicked(event):
                    return botao.texto.lower() # Retorna o texto do botão clicado

        # Desenhar botões
        for botao in botoes:
            botao.draw(tela)

        pygame.display.flip()