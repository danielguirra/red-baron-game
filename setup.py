import pygame
from shot import (
    Bullet,
)  # Certifique-se de que a classe Bullet está corretamente importada

pygame.init()

screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

shoting = True
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

bullets = []  # Lista de balas
space_pressed = False  # Flag para verificar se a tecla de espaço foi pressionada

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Atualiza o delta time
    dt = clock.tick(60) / 1000  # A cada quadro, calculamos o delta time

    screen.fill("white")  # Preenche a tela com branco

    # Desenha o jogador
    pygame.draw.circle(screen, "red", player_pos, 40)

    # Movimentação do jogador
    keys = pygame.key.get_pressed()

    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    # Lógica de disparo
    if (
        keys[pygame.K_SPACE] and not space_pressed
    ):  # Verifica se a tecla de espaço foi pressionada
        bullet = Bullet(shoting)  # Cria a bala
        bullet.rect.center = (
            player_pos.x,
            player_pos.y - 35,
        )  # Define a posição inicial da bala
        bullets.append(bullet)  # Adiciona a bala à lista
        shoting = not shoting  # Alterna entre as balas 1 e 2
        space_pressed = True  # Marca que a tecla de espaço foi pressionada

    # Se a tecla de espaço foi solta, permite que a próxima bala seja disparada
    if not keys[pygame.K_SPACE]:
        space_pressed = False

    # Atualiza e desenha as balas
    for bullet in bullets:
        bullet.rect.y -= 500 * dt  # Movimenta a bala para cima

        # Se a bala atingir o topo da tela, remove a bala
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)  # Remove a bala da lista

        # Desenha a bala na tela
        screen.blit(bullet.image, bullet.rect)

    pygame.display.flip()  # Atualiza a tela

pygame.quit()
