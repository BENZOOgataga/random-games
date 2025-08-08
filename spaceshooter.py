import pygame, random, math, time

# ------------------------- Setup -------------------------
pygame.init()
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter+")
clock = pygame.time.Clock()
FONT = pygame.font.SysFont("consolas", 22)
BIG = pygame.font.SysFont("consolas", 48)
WHITE, BLACK = (255,255,255), (0,0,0)
GRAY = (140,140,160)

# ------------------------- Utils -------------------------
def clamp(x, a, b): return a if x < a else b if x > b else x

def draw_glow_polygon(surf, points, color, glow_sizes=(12,8,4)):
    for r,a in [(glow_sizes[0],25),(glow_sizes[1],50),(glow_sizes[2],100)]:
        glow = pygame.Surface((surf.get_width(), surf.get_height()), pygame.SRCALPHA)
        pygame.draw.polygon(glow, (*color, a), _inflate_poly(points, r))
        surf.blit(glow, (0,0))
    pygame.draw.polygon(surf, color, points)

def _inflate_poly(points, r):
    # simple outward scale around centroid
    cx = sum(p[0] for p in points)/len(points)
    cy = sum(p[1] for p in points)/len(points)
    out = []
    for x,y in points:
        vx, vy = x-cx, y-cy
        d = math.hypot(vx,vy) or 1
        k = (d+r)/d
        out.append((cx+vx*k, cy+vy*k))
    return out

def circle_with_shade(radius, base=(210,210,220)):
    s = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
    for i in range(radius,0,-1):
        t = i/radius
        c = (int(base[0]*t), int(base[1]*t*0.95), int(base[2]*t*0.9))
        pygame.draw.circle(s, c, (radius, radius), i)
    # highlight
    pygame.draw.circle(s, (255,255,255,50), (int(radius*0.6), int(radius*0.6)), int(radius*0.5))
    return s

# ------------------------- Background -------------------------
class StarLayer:
    def __init__(self, n, speed, size, alpha):
        self.speed = speed
        self.stars = []
        self.size = size
        self.alpha = alpha
        for _ in range(n):
            self.stars.append([random.randint(0,WIDTH), random.randint(0,HEIGHT)])
    def update(self, dt):
        for s in self.stars:
            s[1] += self.speed*dt
            if s[1] > HEIGHT: s[0], s[1] = random.randint(0,WIDTH), -5
    def draw(self, surf, offset=(0,0)):
        col = (255,255,255,self.alpha)
        for x,y in self.stars:
            pygame.draw.rect(surf, col, (x+offset[0], y+offset[1], self.size, self.size))

layers = [StarLayer(90, 30, 2, 80), StarLayer(60, 55, 3, 120), StarLayer(35, 90, 4, 180)]

# ------------------------- Entities -------------------------
class Ship:
    def __init__(self):
        self.x, self.y = WIDTH//2, HEIGHT-90
        self.v = 360
        self.cooldown = 0.25
        self.power = 1
        self.inv = 0
        self.recoil = 0
    def rect(self):
        return pygame.Rect(self.x-20, self.y-18, 40, 36)
    def update(self, dt, keys):
        spd = self.v
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:  self.x -= spd*dt
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: self.x += spd*dt
        if keys[pygame.K_UP] or keys[pygame.K_w]:    self.y -= spd*dt
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:  self.y += spd*dt
        self.x = clamp(self.x, 30, WIDTH-30)
        self.y = clamp(self.y, 50, HEIGHT-50)
        if self.inv>0: self.inv -= dt
        if self.recoil>0: self.recoil -= dt
    def draw(self, surf, offset=(0,0)):
        fx = int(math.sin(pygame.time.get_ticks()*0.01)*2)
        pts = [(self.x+offset[0], self.y-22+offset[1]+fx),
               (self.x-18+offset[0], self.y+18+offset[1]),
               (self.x+18+offset[0], self.y+18+offset[1])]
        col = (120,200,255) if self.inv<=0 else (255,200,120)
        draw_glow_polygon(surf, pts, col)
        # engine flame
        flame = pygame.Surface((60,40), pygame.SRCALPHA)
        h = 18+int(8*math.sin(pygame.time.get_ticks()*0.02))
        pygame.draw.polygon(flame, (100,180,255,120), [(30,22),(20,40),(40,40)])
        pygame.draw.polygon(flame, (120,220,255,180), [(30,22),(28,22+h),(32,22+h)])
        surf.blit(flame, (self.x-30+offset[0], self.y+6+offset[1]))

class Bullet:
    def __init__(self, x, y, vx=0, power=1):
        self.x, self.y, self.vy = x, y, -620
        self.vx = vx
        self.power = power
        self.dead = False
    def update(self, dt):
        self.x += self.vx*dt
        self.y += self.vy*dt
        if self.y < -20 or self.x< -20 or self.x>WIDTH+20: self.dead=True
    def draw(self, surf, offset=(0,0)):
        r = pygame.Rect(self.x-3+offset[0], self.y-10+offset[1], 6, 18)
        glow = pygame.Surface((12,28), pygame.SRCALPHA)
        pygame.draw.ellipse(glow,(120,240,255,160),(0,0,12,28))
        surf.blit(glow,(self.x-6+offset[0], self.y-14+offset[1]))
        pygame.draw.rect(surf,(200,255,255), r)

class Meteor:
    sprite_cache = {}
    def __init__(self, x, y, size=44, hp=1):
        self.size = size
        self.hp = hp
        self.x, self.y = x, y
        self.vy = random.uniform(60, 140)
        self.vx = random.uniform(-40, 40)
        self.rot = random.uniform(0, math.tau)
        self.rotv = random.uniform(-1.5, 1.5)
        self.dead = False
        if size not in Meteor.sprite_cache:
            Meteor.sprite_cache[size] = circle_with_shade(size//2)
        self.sprite = Meteor.sprite_cache[size]
    def update(self, dt):
        self.x += self.vx*dt
        self.y += self.vy*dt
        self.rot += self.rotv*dt
        if self.y > HEIGHT+80: self.dead=True
    def draw(self, surf, offset=(0,0)):
        img = pygame.transform.rotozoom(self.sprite, math.degrees(self.rot), 1.0)
        surf.blit(img, (self.x-img.get_width()/2+offset[0], self.y-img.get_height()/2+offset[1]))
    def hit(self, dmg):
        self.hp -= dmg
        if self.hp<=0:
            self.dead=True
            return True
        return False
    def rect(self):
        return pygame.Rect(self.x-self.size//2, self.y-self.size//2, self.size, self.size)

class Particle:
    def __init__(self, x, y):
        ang = random.uniform(0, math.tau)
        spd = random.uniform(80, 320)
        self.vx = math.cos(ang)*spd
        self.vy = math.sin(ang)*spd
        self.x, self.y = x, y
        self.t = 0
        self.life = random.uniform(0.35,0.7)
        self.r = random.randint(2,5)
    def update(self, dt):
        self.t += dt
        self.x += self.vx*dt
        self.y += self.vy*dt
        self.vy += 100*dt
    def draw(self, surf, offset=(0,0)):
        a = 255 * (1 - self.t/self.life)
        if a<0: return
        pygame.draw.circle(surf, (255,200,120,int(a)), (int(self.x+offset[0]), int(self.y+offset[1])), self.r)

# ------------------------- Game State -------------------------
ship = Ship()
bullets = []
meteors = []
particles = []
score = 0
split_chance = 0.35
spawn_timer = 0
fire_timer = 0
shake = 0.0

# shop
points = 0
cost_fire = 50
cost_speed = 50
cost_power = 80

def spawn_wave():
    for _ in range(random.randint(2,4)):
        size = random.choice([38,44,56])
        x = random.randint(40, WIDTH-40)
        meteors.append(Meteor(x, -60, size=size, hp=1+size//40))

# ------------------------- Main Loop -------------------------
running = True
last = time.time()
while running:
    now = time.time()
    dt = now - last
    last = now
    if dt>0.05: dt = 0.05

    for e in pygame.event.get():
        if e.type == pygame.QUIT: running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]: running = False

    # shooting
    fire_timer -= dt
    if keys[pygame.K_SPACE] and fire_timer<=0:
        spread = 0.12 if ship.power>=3 else 0.07 if ship.power>=2 else 0.0
        vx1 = -180*spread if spread>0 else 0
        vx2 = 180*spread if spread>0 else 0
        bullets.append(Bullet(ship.x, ship.y-26, vx=vx1, power=ship.power))
        bullets.append(Bullet(ship.x, ship.y-26, vx=vx2, power=ship.power))
        if ship.power>=4:
            bullets.append(Bullet(ship.x, ship.y-26, vx=0, power=ship.power))
        fire_timer = ship.cooldown
        ship.recoil = 0.06
        shake = max(shake, 0.12)

    ship.update(dt, keys)

    # spawn meteors
    spawn_timer -= dt
    if spawn_timer<=0:
        spawn_wave()
        spawn_timer = random.uniform(0.7, 1.6)

    # update bullets/meteors/particles
    for b in bullets: b.update(dt)
    for m in meteors: m.update(dt)
    for p in particles: p.update(dt)

    bullets = [b for b in bullets if not b.dead]
    meteors = [m for m in meteors if not m.dead]
    particles = [p for p in particles if p.t < p.life]

    # collisions
    for m in meteors[:]:
        mr = m.rect()
        hit_any = False
        for b in bullets[:]:
            if mr.collidepoint(b.x, b.y):
                bullets.remove(b)
                destroyed = m.hit(b.power)
                shake = max(shake, 0.08)
                hit_any = True
                if destroyed:
                    # score and points
                    score += 10
                    points += 10
                    # explosion
                    for _ in range(18):
                        particles.append(Particle(m.x, m.y))
                    # split
                    if m.size>28 and random.random()<split_chance:
                        for sgn in (-1,1):
                            size = max(22, m.size//2)
                            child = Meteor(m.x+sgn*10, m.y-6, size=size, hp=max(1, size//36))
                            child.vx = sgn*random.uniform(60,120)
                            child.vy = random.uniform(120,200)
                            meteors.append(child)
                if hit_any: break

    # upgrades (shop)
    if keys[pygame.K_1] and points>=cost_fire:
        points -= cost_fire
        ship.cooldown = max(0.08, ship.cooldown*0.85)
        cost_fire = int(cost_fire*1.6)
        shake = max(shake, 0.1)
    if keys[pygame.K_2] and points>=cost_speed:
        points -= cost_speed
        ship.v = min(600, ship.v+40)
        cost_speed = int(cost_speed*1.6)
        shake = max(shake, 0.1)
    if keys[pygame.K_3] and points>=cost_power:
        points -= cost_power
        ship.power = min(5, ship.power+1)
        cost_power = int(cost_power*1.8)
        shake = max(shake, 0.12)

    # screen shake
    if shake>0:
        shake -= dt*2.5
        ox = int((random.random()-0.5)*10*shake)
        oy = int((random.random()-0.5)*10*shake)
    else:
        ox, oy = 0, 0

    # ------------------------- Draw -------------------------
    screen.fill((6,8,15))
    for i,ly in enumerate(layers):
        ly.update(dt)
        ly.draw(screen, (ox//(3-i), oy//(3-i)))

    # ship, bullets, meteors, particles
    for b in bullets: b.draw(screen, (ox,oy))
    for m in meteors: m.draw(screen, (ox,oy))
    for p in particles: p.draw(screen, (ox,oy))
    ship.draw(screen, (ox,oy))

    # HUD
    ui = pygame.Surface((WIDTH, 70), pygame.SRCALPHA)
    pygame.draw.rect(ui, (20,25,35,180), (0,0,WIDTH,70))
    screen.blit(ui, (0,0))
    screen.blit(FONT.render(f"Score: {score}", True, WHITE), (14, 14))
    screen.blit(FONT.render(f"Points: {points}", True, WHITE), (14, 40))
    screen.blit(FONT.render(f"[1] Fire {cost_fire}  [2] Speed {cost_speed}  [3] Power {cost_power}", True, (180,220,255)), (180, 22))
    screen.blit(FONT.render(f"Fire cd: {ship.cooldown:.2f}  V: {int(ship.v)}  Pow: {ship.power}", True, GRAY), (180, 44))

    # title watermark
    t = BIG.render("SPACE SHOOTER+", True, (50,80,130))
    screen.blit(t, (WIDTH - t.get_width() - 16, HEIGHT - t.get_height() - 12))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
