import pygame as pg
import random
import sys

# Config
W, H = 400, 600
FPS = 60
GRAVITY = 0.35
JUMP_VEL = -7.5
PIPE_GAP = 150
PIPE_SPEED = 3
PIPE_INTERVAL = 1400  # ms

pg.init()
pg.display.set_caption("Flabby Bird")
screen = pg.display.set_mode((W, H))
clock = pg.time.Clock()
font = pg.font.SysFont(None, 36)
bigfont = pg.font.SysFont(None, 64)

def draw_text(s, y, big=False):
    f = bigfont if big else font
    surf = f.render(s, True, (20, 20, 20))
    rect = surf.get_rect(center=(W//2, y))
    screen.blit(surf, rect)

def new_pipe(x):
    gap_y = random.randint(130, H-130)
    top = pg.Rect(x, 0, 60, gap_y - PIPE_GAP//2)
    bottom = pg.Rect(x, gap_y + PIPE_GAP//2, 60, H - (gap_y + PIPE_GAP//2))
    return top, bottom

def reset():
    bird = pg.Rect(80, H//2, 34, 24)
    vel_y = 0.0
    pipes = []
    score = 0
    alive = True
    last_pipe_time = pg.time.get_ticks() - PIPE_INTERVAL
    return bird, vel_y, pipes, score, alive, last_pipe_time

def main():
    bird, vel_y, pipes, score, alive, last_pipe_time = reset()

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if e.type == pg.KEYDOWN:
                if e.key in (pg.K_SPACE, pg.K_UP):
                    if alive:
                        vel_y = JUMP_VEL
                    else:
                        bird, vel_y, pipes, score, alive, last_pipe_time = reset()

        if alive:
            now = pg.time.get_ticks()
            if now - last_pipe_time >= PIPE_INTERVAL:
                pipes.extend(new_pipe(W + 40))
                last_pipe_time = now

            vel_y += GRAVITY
            bird.y += int(vel_y)

            for r in pipes:
                r.x -= PIPE_SPEED

            pipes = [p for p in pipes if p.right > -5]

            for i in range(0, len(pipes), 2):
                pair = pipes[i:i+2]
                if len(pair) == 2:
                    top, bottom = pair
                    passed = (top.centerx + PIPE_SPEED < bird.centerx <= top.centerx + PIPE_SPEED + PIPE_SPEED)
                    if passed:
                        score += 1

            if bird.top < 0 or bird.bottom > H:
                alive = False

            for p in pipes:
                if bird.colliderect(p):
                    alive = False
                    break

        screen.fill((235, 245, 255))
        pg.draw.rect(screen, (200, 220, 240), (0, H-50, W, 50))
        pg.draw.rect(screen, (255, 200, 0), bird, border_radius=6)
        pg.draw.circle(screen, (0, 0, 0), (bird.right-10, bird.centery-4), 3)

        for i, p in enumerate(pipes):
            pg.draw.rect(screen, (60, 200, 90), p, border_radius=4)
            cap = p.copy()
            cap.height = 14
            cap.y = p.bottom - 14 if p.y == 0 else p.y
            pg.draw.rect(screen, (40, 170, 70), cap, border_radius=6)

        draw_text(f"Score: {score}", 30)

        if not alive:
            draw_text("Game Over", H//2 - 30, big=True)
            draw_text("Press SPACE to retry", H//2 + 20)

        pg.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
