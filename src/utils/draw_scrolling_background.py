def draw_scrolling_background(screen, background, speed, dt, positions):
    screen_height = screen.get_height()

    positions[0] += speed * dt
    positions[1] += speed * dt
    if positions[0] >= screen_height:
        positions[0] = -screen_height
    if positions[1] >= screen_height:
        positions[1] = -screen_height

    screen.blit(background, (0, positions[0]))
    screen.blit(background, (0, positions[1]))
