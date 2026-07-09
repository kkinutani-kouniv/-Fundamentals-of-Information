import pyxel

SCREEN_W = 200
SCREEN_H = 200

UI_H = 16

GROUND_H = 12
GROUND_Y = SCREEN_H - GROUND_H

NEWTON_SCALE = 2
NEWTON_SRC_W = 32
NEWTON_SRC_H = 32
NEWTON_W = NEWTON_SRC_W * NEWTON_SCALE
NEWTON_H = NEWTON_SRC_H * NEWTON_SCALE

NEWTON_X = 0
NEWTON_Y = SCREEN_H - NEWTON_H - 8

FACE_NORMAL = 0
FACE_IDEA = 1
FACE_DOUBT = 2

MISS_MAX = 8
MISS_STAGE_1 = 4

SPECIAL_MAX = 3
SPECIAL_FREEZE_TIME = 75

BLACKHOLE_MAX = 3
BLACKHOLE_TIME = 180
BLACKHOLE_CENTER_X = SCREEN_W // 2
BLACKHOLE_CENTER_Y = SCREEN_H // 2
BLACKHOLE_PULL = 0.72
BLACKHOLE_SCORE = 5
BLACKHOLE_CHAIN_GOLD_CHANCE = 45

FPS = 30
DIFFICULTY_START_FRAME = FPS * 75
DIFFICULTY_UP_FRAME = FPS * 35
DIFFICULTY_SCORE_STEP = 600
DIFFICULTY_MAX = 5

TALK_INTERVAL = FPS * 8
TALK_DURATION = FPS * 3

START_APPLE_COUNT = 4
MAX_APPLE_COUNT = 6

GOLD_RATE_STAGE_1 = 20
GOLD_RATE_STAGE_2 = 40

APPLE_W = 16
APPLE_H = 16

CLICK_W = 12
CLICK_H = 12

FORCE_W = 22
FORCE_H = 22

APPLE_COLLISION_SIZE = 12

POPUP_LIFE = 24
SPARK_LIFE = 10

COLLECT_SCORE_NORMAL = 10
COLLECT_SCORE_GOLD = 50
COLLECT_SCORE_SPECIAL = 30
REPEL_SCORE_NORMAL = 2
REPEL_SCORE_GOLD = 6
REPEL_SCORE_SPECIAL = 4
CHAIN_SCORE = 1

COLOR_COLLECT = 8
COLOR_REPEL = 11
COLOR_CHAIN = 13
COLOR_SPECIAL = 10


BIG_FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01111", "10000", "10000", "10111", "10001", "10001", "01111"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["111", "010", "010", "010", "010", "010", "111"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "!": ["1", "1", "1", "1", "1", "0", "1"],
    "'": ["1", "1", "0", "0", "0", "0", "0"],
    " ": ["0", "0", "0", "0", "0", "0", "0"],
}


def clamp(value, low, high):
    return max(low, min(high, value))


def blt_scale(x, y, img, u, v, w, h, scale, colkey=None):
    for iy in range(h):
        for ix in range(w):
            c = pyxel.images[img].pget(u + ix, v + iy)

            if colkey is not None and c == colkey:
                continue

            pyxel.rect(
                x + ix * scale,
                y + iy * scale,
                scale,
                scale,
                c
            )


def draw_big_text(x, y, text, scale, color, shadow_color=None):
    draw_x = x

    for ch in text:
        if ch not in BIG_FONT:
            ch = " "

        pattern = BIG_FONT[ch]
        char_w = len(pattern[0])

        for row, line in enumerate(pattern):
            for col, dot in enumerate(line):
                if dot == "1":
                    if shadow_color is not None:
                        pyxel.rect(
                            draw_x + col * scale + 1,
                            y + row * scale + 1,
                            scale,
                            scale,
                            shadow_color
                        )

                    pyxel.rect(
                        draw_x + col * scale,
                        y + row * scale,
                        scale,
                        scale,
                        color
                    )

        draw_x += (char_w + 1) * scale


def overlap(ax, ay, aw, ah, bx, by, bw, bh):
    return (
        ax < bx + bw
        and ax + aw > bx
        and ay < by + bh
        and ay + ah > by
    )


class Apple:
    def __init__(self, difficulty=0, gold_rate=GOLD_RATE_STAGE_1):
        self.reset(difficulty, gold_rate)

    def reset(self, difficulty=0, gold_rate=GOLD_RATE_STAGE_1):
        self.x = pyxel.rndi(8, SCREEN_W - APPLE_W - 8)
        self.y = pyxel.rndi(-235 - difficulty * 28, -16)

        self.vx = pyxel.rndf(
            -0.32 - difficulty * 0.050,
            0.32 + difficulty * 0.050
        )

        self.vy = pyxel.rndf(
            0.92 + difficulty * 0.095,
            1.72 + difficulty * 0.150
        )

        self.is_gold = pyxel.rndi(1, 100) <= gold_rate
        self.is_special = False
        self.trail = []

        self.hand_hit_cooldown = 0
        self.apple_hit_cooldown = 0

    def update(self, difficulty, frozen, gold_rate=GOLD_RATE_STAGE_1):
        if self.hand_hit_cooldown > 0:
            self.hand_hit_cooldown -= 1

        if self.apple_hit_cooldown > 0:
            self.apple_hit_cooldown -= 1

        if frozen:
            return False

        self.trail.append((self.x + 8, self.y + 8))

        if len(self.trail) > 12:
            self.trail.pop(0)

        if pyxel.frame_count % 18 == 0:
            self.vx += pyxel.rndf(-0.08, 0.08)

        max_vx = 2.6 + difficulty * 0.090
        max_vy = 3.15 + difficulty * 0.145

        self.vx = clamp(self.vx, -max_vx, max_vx)
        self.vy = clamp(
            self.vy + 0.008 + difficulty * 0.0020,
            -4.0,
            max_vy
        )

        self.x += self.vx
        self.y += self.vy

        self.vx *= 0.996

        if self.x < 0:
            self.x = 0
            self.vx = abs(self.vx) * 0.85

        if self.x > SCREEN_W - APPLE_W:
            self.x = SCREEN_W - APPLE_W
            self.vx = -abs(self.vx) * 0.85

        if self.y < UI_H and self.vy < 0:
            self.y = UI_H
            self.vy = abs(self.vy) * 0.7

        if self.y >= GROUND_Y - APPLE_H:
            self.reset(difficulty, gold_rate)
            return True

        return False

    def bounce_from_force(self, force_cx, force_cy):
        apple_cx = self.x + 8
        apple_cy = self.y + 8

        dx = apple_cx - force_cx
        dy = apple_cy - force_cy

        if dx == 0 and dy == 0:
            dx = pyxel.rndf(-1, 1)
            dy = pyxel.rndf(-1, 1)

        length = max(1, (dx * dx + dy * dy) ** 0.5)
        nx = dx / length
        ny = dy / length

        self.vx = clamp(self.vx * 0.25 + nx * 3.0, -3.8, 3.8)
        self.vy = clamp(self.vy * 0.20 + ny * 2.5 - 0.8, -3.8, 2.0)

        self.hand_hit_cooldown = 14

    def make_special(self):
        self.is_gold = False
        self.is_special = True
        self.apple_hit_cooldown = max(self.apple_hit_cooldown, 16)

    def draw_trail(self, ox, oy):
        for i, (tx, ty) in enumerate(self.trail):
            if i % 2 == 0:
                color = 10 if self.is_gold or self.is_special else 7
                pyxel.rect(int(tx) + ox, int(ty) + oy, 2, 2, color)

    def draw(self, ox, oy):
        frame = (pyxel.frame_count // 8) % 2

        if self.is_special:
            if frame == 0:
                u, v = 48, 16
            else:
                u, v = 48, 32
        elif self.is_gold:
            if frame == 0:
                u, v = 32, 16
            else:
                u, v = 32, 32
        else:
            if frame == 0:
                u, v = 32, 0
            else:
                u, v = 48, 0

        pyxel.blt(int(self.x) + ox, int(self.y) + oy, 0, u, v, 16, 16, 0)


class Note:
    def __init__(self):
        self.x = pyxel.rndi(38, 66)
        self.y = pyxel.rndi(102, 124)
        self.vx = pyxel.rndf(-0.3, 0.3)
        self.vy = pyxel.rndf(-0.9, -0.5)
        self.life = 48
        self.sprite_type = pyxel.rndi(0, 1)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, ox, oy):
        if self.sprite_type == 0:
            u, v = 48, 80
        else:
            u, v = 64, 80

        pyxel.blt(int(self.x) + ox, int(self.y) + oy, 0, u, v, 16, 16, 0)


class ScorePopup:
    def __init__(self, x, y, text, color):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.life = POPUP_LIFE

    def update(self):
        self.y -= 0.5
        self.life -= 1

    def draw(self, ox, oy):
        pyxel.text(int(self.x) + ox, int(self.y) + oy, self.text, self.color)


class HitSpark:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.life = SPARK_LIFE

    def update(self):
        self.life -= 1

    def draw(self, ox, oy):
        age = SPARK_LIFE - self.life
        radius = 3 + age
        color = 10 if (self.life // 2) % 2 == 0 else 7

        pyxel.circb(int(self.x) + ox, int(self.y) + oy, radius, color)

        for angle in range(0, 360, 45):
            dist = radius + 2
            sx = int(self.x + pyxel.cos(angle) * dist) + ox
            sy = int(self.y + pyxel.sin(angle) * dist) + oy
            pyxel.pset(sx, sy, color)


class App:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="Newton No Gravity")
        pyxel.mouse(False)
        pyxel.load("assets.pyxres")

        self.scene = "title"
        self.tutorial_frame = 0
        self.tutorial_phase = "catch"
        self.tutorial_phase_frame = 0
        self.tutorial_apple = None
        self.tutorial_bounced = False

        self.apples = [Apple(0) for _ in range(START_APPLE_COUNT)]
        self.notes = []
        self.popups = []
        self.sparks = []

        self.tree_tiles = []
        self.leaf_tiles = []
        self.leaf_under_tiles = []
        self.leaf_apples = []
        self.clouds = []
        self.ground_items = []

        self.shake_timer = 0
        self.edge_alert_timer = 0
        self.discovery_timer = 0

        self.score = 0
        self.miss_count = 0
        self.special_charge = 0
        self.special_timer = 0
        self.blackhole_charge = 0
        self.blackhole_timer = 0
        self.blackhole_flash_timer = 0
        self.gameover = False

        self.play_frame = 0
        self.difficulty = 0

        self.face = FACE_NORMAL
        self.stage = 0
        self.prev_stage = 0

        self.create_clouds()
        self.create_tree_tiles()
        self.create_leaf_tiles()
        self.create_leaf_under_tiles()
        self.create_leaf_apples()
        self.create_ground_items()

        pyxel.run(self.update, self.draw)

    def open_tutorial(self):
        self.reset_game()
        self.scene = "tutorial"
        self.tutorial_frame = 0
        self.tutorial_phase = "catch"
        self.tutorial_phase_frame = 0
        self.tutorial_bounced = False
        self.setup_tutorial_apple("catch")

    def start_game(self):
        self.reset_game()
        self.scene = "play"

    def reset_game(self):
        self.apples = [Apple(0) for _ in range(START_APPLE_COUNT)]
        self.notes.clear()
        self.popups.clear()
        self.sparks.clear()

        self.shake_timer = 0
        self.edge_alert_timer = 0
        self.discovery_timer = 0

        self.score = 0
        self.miss_count = 0
        self.special_charge = 0
        self.special_timer = 0
        self.blackhole_charge = 0
        self.blackhole_timer = 0
        self.blackhole_flash_timer = 0
        self.gameover = False

        self.play_frame = 0
        self.difficulty = 0

        self.face = FACE_NORMAL
        self.stage = 0
        self.prev_stage = 0

    def setup_tutorial_apple(self, phase):
        self.tutorial_apple = Apple(0)
        self.tutorial_apple.x = 92
        self.tutorial_apple.y = -18
        self.tutorial_apple.vx = 0
        self.tutorial_apple.vy = 1.08 if phase == "catch" else 0.98
        self.tutorial_apple.is_gold = False
        self.tutorial_apple.is_special = False
        self.tutorial_apple.trail.clear()
        self.tutorial_apple.hand_hit_cooldown = 0
        self.tutorial_apple.apple_hit_cooldown = 0

    def start_tutorial_phase(self, phase):
        self.tutorial_phase = phase
        self.tutorial_phase_frame = 0
        self.tutorial_bounced = phase == "ready"
        self.popups.clear()
        self.sparks.clear()

        if phase in ("catch", "hold"):
            self.setup_tutorial_apple(phase)

    def update_tutorial_apple_drop(self):
        apple = self.tutorial_apple
        if apple is None:
            return

        apple.trail.append((apple.x + 8, apple.y + 8))
        if len(apple.trail) > 12:
            apple.trail.pop(0)

        if self.tutorial_phase == "hold" and self.tutorial_bounced:
            apple.vy = clamp(apple.vy + 0.012, -3.8, 2.2)
            apple.x += apple.vx
            apple.y += apple.vy
            apple.vx *= 0.992
        else:
            apple.y += apple.vy

        if apple.x < 0:
            apple.x = 0
            apple.vx = abs(apple.vx) * 0.8
        elif apple.x > SCREEN_W - APPLE_W:
            apple.x = SCREEN_W - APPLE_W
            apple.vx = -abs(apple.vx) * 0.8

        if apple.y >= GROUND_Y - APPLE_H:
            self.setup_tutorial_apple(self.tutorial_phase)

    def update_tutorial_catch(self):
        self.update_tutorial_apple_drop()

        apple = self.tutorial_apple
        if apple is None:
            return

        click_x = pyxel.mouse_x + 2
        click_y = pyxel.mouse_y + 2

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and overlap(
            click_x,
            click_y,
            CLICK_W,
            CLICK_H,
            int(apple.x) + 3,
            int(apple.y) + 3,
            10,
            10
        ):
            hit_x = apple.x + 8
            hit_y = apple.y + 8
            self.start_tutorial_phase("hold")
            self.add_text_popup(hit_x, hit_y - 8, "CATCH!", COLOR_COLLECT)
            self.add_spark(hit_x, hit_y)

    def update_tutorial_hold(self):
        self.update_tutorial_apple_drop()

        apple = self.tutorial_apple
        if apple is None:
            return

        if not pyxel.btn(pyxel.MOUSE_BUTTON_LEFT) or self.tutorial_bounced:
            return

        force_cx = pyxel.mouse_x + 8
        force_cy = pyxel.mouse_y + 8
        force_x = force_cx - FORCE_W // 2
        force_y = force_cy - FORCE_H // 2

        if overlap(
            force_x,
            force_y,
            FORCE_W,
            FORCE_H,
            int(apple.x) + 4,
            int(apple.y) + 4,
            8,
            8
        ):
            apple.bounce_from_force(force_cx, force_cy)
            hit_x = apple.x + 8
            hit_y = apple.y + 8
            self.shake_timer = max(self.shake_timer, 8)
            self.start_tutorial_phase("ready")
            self.add_text_popup(hit_x, hit_y - 8, "HOLD!", COLOR_REPEL)
            self.add_spark(hit_x, hit_y)

    def update_tutorial_ready(self):
        if self.tutorial_apple is not None:
            self.update_tutorial_apple_drop()

        if self.tutorial_phase_frame > FPS * 2:
            self.start_game()

    def get_difficulty(self):
        if self.play_frame < DIFFICULTY_START_FRAME:
            return 0

        time_level = (self.play_frame - DIFFICULTY_START_FRAME) // DIFFICULTY_UP_FRAME
        score_level = self.score // DIFFICULTY_SCORE_STEP

        return min(DIFFICULTY_MAX, 1 + time_level + score_level // 2)

    def create_clouds(self):
        self.clouds = [
            {"x": 12, "y": 54, "speed": 0.20},
            {"x": 88, "y": 72, "speed": 0.15},
            {"x": 150, "y": 46, "speed": 0.25},
        ]

    def create_tree_tiles(self):
        for x in [SCREEN_W - 32, SCREEN_W - 16]:
            for y in range(32, SCREEN_H, 16):
                if pyxel.rndi(0, 1) == 0:
                    u, v = 16, 96
                else:
                    u, v = 16, 112

                self.tree_tiles.append((x, y, u, v))

    def create_leaf_tiles(self):
        for y in [0, 16]:
            for x in range(0, SCREEN_W, 16):
                if pyxel.rndi(0, 1) == 0:
                    u, v = 0, 96
                else:
                    u, v = 0, 112

                self.leaf_tiles.append((x, y, u, v))

    def create_leaf_under_tiles(self):
        x = 0
        y = 32

        while x < SCREEN_W:
            if pyxel.rndi(0, 1) == 0 or x > SCREEN_W - 32:
                u, v = 48, 96
                w, h = 16, 8
            else:
                u, v = 48, 112
                w, h = 32, 8

            self.leaf_under_tiles.append((x, y, u, v, w, h))
            x += w

    def create_leaf_apples(self):
        positions = []
        min_dist = 24

        for _ in range(8):
            placed = False

            for _ in range(80):
                x = pyxel.rndi(0, SCREEN_W - 16)
                y = pyxel.rndi(18, 24)

                ok = True
                for px, py in positions:
                    dx = x - px
                    dy = y - py
                    if dx * dx + dy * dy < min_dist * min_dist:
                        ok = False
                        break

                if ok:
                    positions.append((x, y))
                    placed = True
                    break

            if not placed:
                x = pyxel.rndi(0, SCREEN_W - 16)
                y = pyxel.rndi(18, 24)
                positions.append((x, y))

        for x, y in positions:
            if pyxel.rndi(0, 1) == 0:
                u, v = 32, 0
            else:
                u, v = 48, 0

            self.leaf_apples.append((x, y, u, v))

    def create_ground_items(self):
        for x in range(0, SCREEN_W, 12):
            if pyxel.rndi(1, 100) <= 65:
                if pyxel.rndi(0, 1) == 0:
                    u, v = 64, 0
                else:
                    u, v = 64, 16

                item_x = x + pyxel.rndi(-2, 2)
                item_y = GROUND_Y - 14 + pyxel.rndi(-1, 1)

                self.ground_items.append((item_x, item_y, u, v))

    def get_stage(self):
        if self.gameover:
            return 2
        elif self.miss_count >= MISS_STAGE_1:
            return 1
        else:
            return 0

    def update_stage_and_face(self):
        self.stage = self.get_stage()

        if self.stage > self.prev_stage:
            self.edge_alert_timer = 36
            self.shake_timer = max(self.shake_timer, 10)

        self.prev_stage = self.stage

        if self.stage == 2:
            self.face = FACE_IDEA
        elif self.stage == 1:
            self.face = FACE_DOUBT
        else:
            self.face = FACE_NORMAL

    def get_gold_rate(self):
        if not self.gameover and self.miss_count >= MISS_STAGE_1:
            return GOLD_RATE_STAGE_2
        return GOLD_RATE_STAGE_1

    def adjust_apple_count(self):
        target = START_APPLE_COUNT + (self.difficulty + 1) // 3
        target = min(MAX_APPLE_COUNT, target)

        while len(self.apples) < target:
            self.apples.append(Apple(self.difficulty, self.get_gold_rate()))

    def try_activate_special(self):
        if self.special_charge >= SPECIAL_MAX and pyxel.btnp(pyxel.KEY_SPACE):
            self.special_charge = 0
            self.special_timer = SPECIAL_FREEZE_TIME
            self.shake_timer = max(self.shake_timer, 6)

    def start_blackhole(self):
        self.blackhole_charge = 0
        self.blackhole_timer = BLACKHOLE_TIME
        self.blackhole_flash_timer = 30
        self.shake_timer = max(self.shake_timer, 28)
        self.edge_alert_timer = max(self.edge_alert_timer, 20)
        self.add_text_popup(BLACKHOLE_CENTER_X, BLACKHOLE_CENTER_Y - 28, "BLACK HOLE!", 7)

    def update_blackhole(self):
        self.blackhole_timer -= 1

        if self.blackhole_flash_timer > 0:
            self.blackhole_flash_timer -= 1

        phase_power = 1 - self.blackhole_timer / BLACKHOLE_TIME

        for apple in self.apples:
            if apple.hand_hit_cooldown > 0:
                apple.hand_hit_cooldown -= 1

            if apple.apple_hit_cooldown > 0:
                apple.apple_hit_cooldown -= 1

            apple.trail.append((apple.x + 8, apple.y + 8))
            if len(apple.trail) > 14:
                apple.trail.pop(0)

            apple_cx = apple.x + 8
            apple_cy = apple.y + 8
            dx = BLACKHOLE_CENTER_X - apple_cx
            dy = BLACKHOLE_CENTER_Y - apple_cy
            dist = max(1, (dx * dx + dy * dy) ** 0.5)

            # Gentler pull than v2: still gathers apples, but leaves time to see and react to them.
            pull = BLACKHOLE_PULL + phase_power * 0.28
            apple.vx += dx / dist * pull
            apple.vy += dy / dist * pull

            # Keep a visible spiral without overpowering apple readability.
            swirl = 0.12 + phase_power * 0.06
            apple.vx += -dy / dist * swirl
            apple.vy += dx / dist * swirl

            apple.vx = clamp(apple.vx, -6.4, 6.4)
            apple.vy = clamp(apple.vy, -6.4, 6.4)

            apple.x += apple.vx
            apple.y += apple.vy

            # Soft center correction instead of the previous hard snap.
            apple.x += dx * 0.020
            apple.y += dy * 0.020

            apple.vx *= 0.955
            apple.vy *= 0.955

            if dist < 19:
                was_special = apple.is_special
                was_gold = apple.is_gold

                self.score += BLACKHOLE_SCORE
                self.add_text_popup(apple_cx, apple_cy - 8, "ABSORB!", 7)
                self.add_popup(apple_cx, apple_cy + 3, BLACKHOLE_SCORE, COLOR_SPECIAL)
                self.add_spark(apple_cx, apple_cy)

                # Chain chance: absorbed sparkle apples always charge the next black hole.
                # Gold apples sometimes charge it too, so one black hole can lead into another.
                if was_special:
                    self.add_blackhole_charge(apple_cx, apple_cy - 18, "NEXT +1")
                elif was_gold and pyxel.rndi(1, 100) <= BLACKHOLE_CHAIN_GOLD_CHANCE:
                    self.add_blackhole_charge(apple_cx, apple_cy - 18, "NEXT +1")

                apple.reset(self.difficulty, self.get_gold_rate())
                apple.y = pyxel.rndi(-210, -50)

        if self.blackhole_timer <= 0:
            self.blackhole_timer = 0

            if self.blackhole_charge >= BLACKHOLE_MAX:
                self.add_text_popup(BLACKHOLE_CENTER_X, BLACKHOLE_CENTER_Y - 40, "VOID CHAIN!", COLOR_SPECIAL)
                self.start_blackhole()
            else:
                self.blackhole_flash_timer = 12
                self.shake_timer = max(self.shake_timer, 8)

    def add_blackhole_charge(self, x, y, text="VOID +1"):
        old_charge = self.blackhole_charge
        self.blackhole_charge = min(BLACKHOLE_MAX, self.blackhole_charge + 1)

        if self.blackhole_charge > old_charge:
            self.add_text_popup(x, y, text, COLOR_SPECIAL)

            if self.blackhole_charge >= BLACKHOLE_MAX:
                self.add_text_popup(x, y - 9, "VOID READY!", 7)

    def collect_apple(self, apple):
        if apple.is_special:
            gain = COLLECT_SCORE_SPECIAL
            self.score += gain
            self.add_blackhole_charge(apple.x + 8, apple.y - 8)

            if self.blackhole_charge >= BLACKHOLE_MAX and self.blackhole_timer <= 0:
                self.start_blackhole()
        elif apple.is_gold:
            gain = COLLECT_SCORE_GOLD
            self.score += gain
            self.special_charge = min(SPECIAL_MAX, self.special_charge + 1)
        else:
            gain = COLLECT_SCORE_NORMAL
            self.score += gain

        self.add_popup(apple.x + 8, apple.y, gain, COLOR_COLLECT)
        apple.reset(self.difficulty, self.get_gold_rate())

    def repel_apple(self, apple):
        if apple.is_special:
            gain = REPEL_SCORE_SPECIAL
        elif apple.is_gold:
            gain = REPEL_SCORE_GOLD
        else:
            gain = REPEL_SCORE_NORMAL

        self.score += gain
        self.add_popup(apple.x + 8, apple.y, gain, COLOR_REPEL)

    def add_popup(self, x, y, gain, color):
        text = "+" + str(gain)
        popup_x = x - len(text) * 2
        self.popups.append(ScorePopup(popup_x, y, text, color))

    def add_text_popup(self, x, y, text, color):
        popup_x = x - len(text) * 2
        self.popups.append(ScorePopup(popup_x, y, text, color))

    def reduce_gravity_gauge(self, x, y):
        if self.miss_count > 0:
            self.miss_count -= 1
            self.add_text_popup(x, y, "SAFE!", COLOR_SPECIAL)
        else:
            self.add_text_popup(x, y, "SPECIAL!", COLOR_SPECIAL)

    def add_spark(self, x, y):
        self.sparks.append(HitSpark(x, y))

    def update_hand_action(self):
        click_x = pyxel.mouse_x + 2
        click_y = pyxel.mouse_y + 2

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            for apple in self.apples:
                if overlap(
                    click_x,
                    click_y,
                    CLICK_W,
                    CLICK_H,
                    int(apple.x) + 3,
                    int(apple.y) + 3,
                    10,
                    10
                ):
                    self.collect_apple(apple)
                    return

        if not pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            return

        force_cx = pyxel.mouse_x + 8
        force_cy = pyxel.mouse_y + 8

        force_x = force_cx - FORCE_W // 2
        force_y = force_cy - FORCE_H // 2

        for apple in self.apples:
            if apple.hand_hit_cooldown > 0:
                continue

            if overlap(
                force_x,
                force_y,
                FORCE_W,
                FORCE_H,
                int(apple.x) + 4,
                int(apple.y) + 4,
                8,
                8
            ):
                apple.bounce_from_force(force_cx, force_cy)
                self.repel_apple(apple)

    def update_apple_collisions(self):
        for i in range(len(self.apples)):
            for j in range(i + 1, len(self.apples)):
                a = self.apples[i]
                b = self.apples[j]

                if a.apple_hit_cooldown > 0 or b.apple_hit_cooldown > 0:
                    continue

                if overlap(
                    int(a.x) + 2,
                    int(a.y) + 2,
                    APPLE_COLLISION_SIZE,
                    APPLE_COLLISION_SIZE,
                    int(b.x) + 2,
                    int(b.y) + 2,
                    APPLE_COLLISION_SIZE,
                    APPLE_COLLISION_SIZE
                ):
                    dx = (b.x + 8) - (a.x + 8)
                    dy = (b.y + 8) - (a.y + 8)

                    if dx == 0 and dy == 0:
                        dx = pyxel.rndf(-1, 1)
                        dy = pyxel.rndf(-1, 1)

                    length = max(1, (dx * dx + dy * dy) ** 0.5)
                    nx = dx / length
                    ny = dy / length

                    a.x -= nx * 2
                    a.y -= ny * 2
                    b.x += nx * 2
                    b.y += ny * 2

                    avx = a.vx
                    avy = a.vy

                    a.vx = b.vx * 0.35 - nx * 2.2
                    a.vy = b.vy * 0.35 - 0.7

                    b.vx = avx * 0.35 + nx * 2.2
                    b.vy = avy * 0.35 - 0.6

                    a.apple_hit_cooldown = 10
                    b.apple_hit_cooldown = 10

                    hit_x = (a.x + b.x) / 2 + 8
                    hit_y = (a.y + b.y) / 2 + 8

                    player_hit = a.hand_hit_cooldown > 0 or b.hand_hit_cooldown > 0

                    if player_hit:
                        self.score += CHAIN_SCORE
                        self.add_text_popup(hit_x, hit_y - 6, "HIT!", COLOR_CHAIN)
                        self.add_popup(hit_x, hit_y + 3, CHAIN_SCORE, COLOR_CHAIN)
                        self.add_spark(hit_x, hit_y)

                    made_special = False

                    # Any apple that collides with a gold apple can become a sparkle apple.
                    # This no longer requires the player to have touched or flicked either apple.
                    a_was_gold = a.is_gold
                    b_was_gold = b.is_gold

                    if b_was_gold and not a.is_special:
                        a.make_special()
                        made_special = True

                    if a_was_gold and not b.is_special:
                        b.make_special()
                        made_special = True

                    if made_special:
                        self.add_text_popup(hit_x, hit_y - 15, "SPARKLE!", COLOR_SPECIAL)
                        self.reduce_gravity_gauge(hit_x, hit_y - 25)
                        self.add_spark(hit_x, hit_y)

    def get_newton_talk(self):
        if self.gameover:
            return None

        if self.play_frame % TALK_INTERVAL >= TALK_DURATION:
            return None

        if self.stage == 0:
            talks = [
                "NICE WEATHER.",
                "WHAT A FINE DAY.",
                "THE APPLES LOOK GOOD.",
            ]
        elif self.stage == 1:
            talks = [
                "SOMETHING IS OFF...",
                "WHY DO THEY FALL?",
                "I FEEL A STRANGE FORCE...",
            ]
        else:
            talks = [
                "I FOUND IT!",
            ]

        talk_index = (self.play_frame // TALK_INTERVAL) % len(talks)
        return talks[talk_index]

    def update_notes(self):
        if self.face == FACE_NORMAL and not self.gameover:
            if pyxel.frame_count % 22 == 0:
                self.notes.append(Note())
        else:
            self.notes.clear()

        for note in self.notes:
            note.update()

        self.notes = [note for note in self.notes if note.life > 0]

    def update_popups(self):
        for popup in self.popups:
            popup.update()

        self.popups = [popup for popup in self.popups if popup.life > 0]

    def update_sparks(self):
        for spark in self.sparks:
            spark.update()

        self.sparks = [spark for spark in self.sparks if spark.life > 0]

    def update_clouds(self):
        for cloud in self.clouds:
            cloud["x"] += cloud["speed"]

            if cloud["x"] > SCREEN_W + 32:
                cloud["x"] = -32
                cloud["y"] = pyxel.rndi(42, 78)

    def start_gameover(self):
        self.gameover = True
        self.miss_count = MISS_MAX
        self.discovery_timer = 150
        self.edge_alert_timer = 60
        self.shake_timer = 24

    def update_title(self):
        self.update_clouds()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.open_tutorial()

        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            self.open_tutorial()

    def update_tutorial(self):
        self.update_clouds()
        self.tutorial_frame += 1
        self.tutorial_phase_frame += 1

        if self.shake_timer > 0:
            self.shake_timer -= 1

        if self.tutorial_phase == "catch":
            self.update_tutorial_catch()
        elif self.tutorial_phase == "hold":
            self.update_tutorial_hold()
        else:
            self.update_tutorial_ready()

        self.update_popups()
        self.update_sparks()

    def update(self):
        if self.scene == "title":
            self.update_title()
            return

        if self.scene == "tutorial":
            self.update_tutorial()
            return

        if self.gameover:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()

            if self.discovery_timer > 0:
                self.discovery_timer -= 1

        if not self.gameover:
            self.play_frame += 1
            self.difficulty = self.get_difficulty()

            self.try_activate_special()
            self.update_hand_action()

            frozen = self.special_timer > 0

            if self.blackhole_timer > 0:
                self.update_blackhole()
            else:
                for apple in self.apples:
                    hit_ground = apple.update(self.difficulty, frozen, self.get_gold_rate())

                    if hit_ground:
                        self.shake_timer = 12
                        self.miss_count += 1

                        if self.miss_count >= MISS_MAX:
                            self.start_gameover()
                            break

                if not frozen:
                    self.update_apple_collisions()

            if self.special_timer > 0:
                self.special_timer -= 1

        if self.shake_timer > 0:
            self.shake_timer -= 1

        if self.edge_alert_timer > 0:
            self.edge_alert_timer -= 1

        self.update_stage_and_face()
        self.adjust_apple_count()
        self.update_notes()
        self.update_clouds()
        self.update_popups()
        self.update_sparks()

    def get_shake_offset(self):
        if self.blackhole_timer > 0:
            power = 3 if self.blackhole_timer > 25 else 2
            ox = pyxel.rndi(-power, power)
            oy = pyxel.rndi(-power, power)
            return ox, oy

        if self.shake_timer > 0:
            ox = pyxel.rndi(-2, 2)
            oy = pyxel.rndi(-2, 2)
            return ox, oy
        return 0, 0

    def draw_sky(self, ox, oy):
        pyxel.cls(12)

        for cloud in self.clouds:
            pyxel.blt(
                int(cloud["x"]) + ox,
                int(cloud["y"]) + oy,
                0,
                48,
                64,
                32,
                16,
                0
            )

    def draw_void_sky(self, ox, oy):
        pyxel.cls(0)

        # Fewer stars than v2 so the apples stay readable on the black background.
        for i in range(24):
            x = (i * 37 + pyxel.frame_count * (i % 4 + 1)) % SCREEN_W
            y = (i * 23 + pyxel.frame_count * (i % 2 + 1)) % SCREEN_H
            color = 7 if i % 5 == 0 else 13
            pyxel.pset(x + ox, y + oy, color)

        if self.blackhole_flash_timer > 0 and (pyxel.frame_count // 3) % 2 == 0:
            pyxel.rect(0, 0, SCREEN_W, SCREEN_H, 7)

    def draw_blackhole_effect(self, ox, oy):
        if self.blackhole_timer <= 0:
            return

        cx = BLACKHOLE_CENTER_X + ox
        cy = BLACKHOLE_CENTER_Y + oy
        pulse = pyxel.frame_count % 20
        spin = pyxel.frame_count * 7

        # Keep the flashy vortex, but reduce density so apple sprites are easy to track.
        for radius in range(22, 82, 18):
            color = 13 if (radius + pulse) % 36 < 18 else 7
            pyxel.circb(cx, cy, radius + pulse // 3, color)

        for angle in range(0, 360, 24):
            outer = 88 + (angle % 32)
            inner = 18 + (pyxel.frame_count + angle) % 10
            x1 = cx + int(pyxel.cos(angle + spin) * outer)
            y1 = cy + int(pyxel.sin(angle + spin) * outer)
            x2 = cx + int(pyxel.cos(angle + spin * 2) * inner)
            y2 = cy + int(pyxel.sin(angle + spin * 2) * inner)
            color = 7 if angle % 48 == 0 else 13
            pyxel.line(x1, y1, x2, y2, color)

        pyxel.circ(cx, cy, 17 + (pulse // 6), 0)
        pyxel.circb(cx, cy, 24 + (pulse // 5), 7)
        pyxel.circb(cx, cy, 34 + (pulse // 4), 13)

        if self.blackhole_timer > BLACKHOLE_TIME - 42 and (pyxel.frame_count // 5) % 2 == 0:
            draw_big_text(47, 28, "BLACK", 2, 7, 0)
            draw_big_text(58, 48, "HOLE!", 2, 13, 0)

    def draw_apple_focus_markers(self, ox, oy):
        if self.blackhole_timer <= 0:
            return

        for apple in self.apples:
            cx = int(apple.x) + 8 + ox
            cy = int(apple.y) + 8 + oy
            color = 13 if apple.is_special else 10 if apple.is_gold else 7
            pyxel.circb(cx, cy, 10, color)
            if (pyxel.frame_count // 4) % 2 == 0:
                pyxel.pset(cx, cy, 7)

    def draw_trees(self, ox, oy):
        for x, y, u, v in self.tree_tiles:
            pyxel.blt(x + ox, y + oy, 0, u, v, 16, 16)

    def draw_ground_base(self, ox, oy):
        if self.blackhole_timer > 0 or self.special_timer > 0:
            pyxel.rect(0 + ox, GROUND_Y + oy, SCREEN_W, GROUND_H, 0)
            pyxel.line(0 + ox, GROUND_Y + oy, SCREEN_W + ox, GROUND_Y + oy, 7)
            for x in range(0, SCREEN_W, 8):
                if (x + pyxel.frame_count) % 16 == 0:
                    pyxel.pset(x + ox, GROUND_Y - 1 + oy, 13)
        else:
            pyxel.rect(0 + ox, GROUND_Y + oy, SCREEN_W, GROUND_H, 4)
            pyxel.line(0 + ox, GROUND_Y + oy, SCREEN_W + ox, GROUND_Y + oy, 3)

    def draw_leaves(self, ox, oy):
        for x, y, u, v in self.leaf_tiles:
            if y == 0:
                continue
            pyxel.blt(x + ox, y + oy, 0, u, v, 16, 16, 0)

        for x, y, u, v, w, h in self.leaf_under_tiles:
            pyxel.blt(x + ox, y + oy, 0, u, v, w, h, 0)

    def draw_leaf_apples(self, ox, oy):
        for x, y, u, v in self.leaf_apples:
            pyxel.blt(x + ox, y + oy, 0, u, v, 16, 16, 0)

    def draw_ground_items_foreground(self, ox, oy):
        for x, y, u, v in self.ground_items:
            pyxel.blt(x + ox, y + oy, 0, u, v, 16, 16, 0)

    def draw_background(self, ox, oy):
        if self.blackhole_timer > 0 or self.special_timer > 0:
            self.draw_void_sky(ox, oy)
        else:
            self.draw_sky(ox, oy)

        self.draw_trees(ox, oy)
        self.draw_ground_base(ox, oy)

    def draw_newton(self, ox, oy):
        if self.face == FACE_NORMAL:
            blt_scale(
                NEWTON_X + ox,
                NEWTON_Y + oy,
                0,
                0,
                0,
                32,
                32,
                NEWTON_SCALE,
                0
            )

        elif self.face == FACE_IDEA:
            blt_scale(
                NEWTON_X + ox,
                NEWTON_Y + oy,
                0,
                0,
                32,
                32,
                32,
                NEWTON_SCALE,
                0
            )

            frame = (pyxel.frame_count // 8) % 2

            if frame == 0:
                u, v = 32, 48
            else:
                u, v = 32, 56

            blt_scale(
                NEWTON_X + ox,
                NEWTON_Y - 18 + oy,
                0,
                u,
                v,
                32,
                8,
                2,
                0
            )

        elif self.face == FACE_DOUBT:
            blt_scale(
                NEWTON_X + ox,
                NEWTON_Y + oy,
                0,
                0,
                64,
                32,
                32,
                NEWTON_SCALE,
                0
            )

            frame = (pyxel.frame_count // 8) % 2

            if frame == 0:
                u, v = 32, 64
            else:
                u, v = 32, 80

            blt_scale(
                NEWTON_X + 18 + ox,
                NEWTON_Y - 34 + oy,
                0,
                u,
                v,
                16,
                16,
                2,
                0
            )

    def draw_notes(self, ox, oy):
        for note in self.notes:
            note.draw(ox, oy)

    def draw_popups(self, ox, oy):
        for popup in self.popups:
            popup.draw(ox, oy)

    def draw_sparks(self, ox, oy):
        for spark in self.sparks:
            spark.draw(ox, oy)

    def draw_newton_talk(self):
        text = self.get_newton_talk()

        if text is None:
            return

        pyxel.text(56, NEWTON_Y - 20, text, 7)

    def draw_score(self):
        pyxel.text(6, 42, "SCORE " + str(self.score), 7)

        if self.difficulty > 0 and not self.gameover:
            pyxel.text(6, 50, "LEVEL " + str(self.difficulty), 8)

    def draw_special_effect(self, ox, oy):
        if self.special_timer <= 0:
            return

        if (pyxel.frame_count // 5) % 2 == 0:
            pyxel.text(76, 58, "TIME STOP", 7)

        pulse = (pyxel.frame_count // 4) % 3
        pyxel.rectb(2, 18, SCREEN_W - 4, SCREEN_H - 20, 7)
        pyxel.rectb(4, 20, SCREEN_W - 8, SCREEN_H - 24, 13)

        for apple in self.apples:
            cx = int(apple.x) + 8 + ox
            cy = int(apple.y) + 8 + oy
            pyxel.circb(cx, cy, 10 + pulse, 7)
            pyxel.circb(cx, cy, 14 + pulse, 13)

    def draw_force_field(self):
        if not pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            return

        if (pyxel.frame_count // 4) % 2 == 0:
            pyxel.circb(pyxel.mouse_x + 8, pyxel.mouse_y + 8, 11, 10)
        else:
            pyxel.circb(pyxel.mouse_x + 8, pyxel.mouse_y + 8, 10, 7)

    def draw_discovery_effect(self):
        if not self.gameover:
            return

        cx = NEWTON_X + 35
        cy = NEWTON_Y - 8

        if self.discovery_timer > 0:
            radius = 8 + (150 - self.discovery_timer) // 3

            if radius < 70:
                pyxel.circb(cx, cy, radius, 10)
                pyxel.circb(cx, cy, max(1, radius // 2), 7)

            for angle in range(0, 360, 45):
                length = 22 + (pyxel.frame_count % 12)
                x1 = cx + int(pyxel.cos(angle) * 10)
                y1 = cy + int(pyxel.sin(angle) * 10)
                x2 = cx + int(pyxel.cos(angle) * length)
                y2 = cy + int(pyxel.sin(angle) * length)
                pyxel.line(x1, y1, x2, y2, 10)

        frame = (pyxel.frame_count // 8) % 2
        if frame == 0:
            u, v = 32, 48
        else:
            u, v = 32, 56

        blt_scale(
            NEWTON_X,
            NEWTON_Y - 22,
            0,
            u,
            v,
            32,
            8,
            2,
            0
        )

    def draw_gameover_message(self):
        if not self.gameover:
            return

        if self.discovery_timer > 100 and (pyxel.frame_count // 3) % 2 == 0:
            pyxel.rect(0, 0, SCREEN_W, SCREEN_H, 7)

        pyxel.rect(16, 66, 168, 58, 0)
        pyxel.rectb(16, 66, 168, 58, 10)
        pyxel.rectb(18, 68, 164, 54, 7)

        pyxel.text(67, 72, "NEWTON FOUND", 10)
        draw_big_text(36, 84, "GRAVITY!", 3, 10, 8)
        pyxel.text(70, 113, "PRESS R", 7)

    def draw_ui(self):
        pyxel.rect(0, 0, SCREEN_W, UI_H, 3)
        pyxel.line(0, UI_H - 1, SCREEN_W, UI_H - 1, 11)

        miss_x = 4
        miss_y = 4
        miss_w = 84
        miss_h = 8

        pyxel.rect(miss_x, miss_y, miss_w, miss_h, 1)
        pyxel.rectb(miss_x, miss_y, miss_w, miss_h, 7)

        fill_w = int(miss_w * self.miss_count / MISS_MAX)
        if fill_w > 0:
            inner_w = max(1, fill_w - 2)
            pyxel.rect(miss_x + 1, miss_y + 1, inner_w, miss_h - 2, 8)

        stage_x = miss_x + int(miss_w * MISS_STAGE_1 / MISS_MAX)
        pyxel.line(stage_x, miss_y, stage_x, miss_y + miss_h - 1, 10)

        skill_x = 94
        skill_y = 4
        skill_w = 46
        skill_h = 8

        pyxel.rect(skill_x, skill_y, skill_w, skill_h, 1)
        pyxel.rectb(skill_x, skill_y, skill_w, skill_h, 7)

        if self.special_timer > 0:
            skill_fill = int(skill_w * self.special_timer / SPECIAL_FREEZE_TIME)
            if skill_fill > 0:
                inner_w = max(1, skill_fill - 2)
                pyxel.rect(skill_x + 1, skill_y + 1, inner_w, skill_h - 2, 12)
        else:
            skill_fill = int(skill_w * self.special_charge / SPECIAL_MAX)
            if skill_fill > 0:
                inner_w = max(1, skill_fill - 2)
                pyxel.rect(skill_x + 1, skill_y + 1, inner_w, skill_h - 2, 10)

        if self.special_charge >= SPECIAL_MAX and self.special_timer <= 0:
            if (pyxel.frame_count // 10) % 2 == 0:
                pyxel.text(skill_x + 9, skill_y + 2, "SPACE", 0)

        hole_x = 146
        hole_y = 4
        hole_w = 50
        hole_h = 8

        pyxel.rect(hole_x, hole_y, hole_w, hole_h, 1)
        pyxel.rectb(hole_x, hole_y, hole_w, hole_h, 7)

        if self.blackhole_timer > 0:
            hole_fill = int(hole_w * self.blackhole_timer / BLACKHOLE_TIME)
            if hole_fill > 0:
                inner_w = max(1, hole_fill - 2)
                pyxel.rect(hole_x + 1, hole_y + 1, inner_w, hole_h - 2, 13)

            if (pyxel.frame_count // 4) % 2 == 0:
                pyxel.text(hole_x + 18, hole_y + 2, "BH", 7)

            if self.blackhole_charge > 0:
                pyxel.text(hole_x + 2, hole_y + 2, "+" + str(self.blackhole_charge), 13)
        else:
            hole_fill = int(hole_w * self.blackhole_charge / BLACKHOLE_MAX)
            if hole_fill > 0:
                inner_w = max(1, hole_fill - 2)
                pyxel.rect(hole_x + 1, hole_y + 1, inner_w, hole_h - 2, 13)

    def draw_stage_alert(self):
        if self.edge_alert_timer > 0:
            pulse = (self.edge_alert_timer // 3) % 2
            color1 = 8 if pulse == 0 else 10
            color2 = 7 if pulse == 0 else 8

            pyxel.rectb(0, 0, SCREEN_W, SCREEN_H, color1)
            pyxel.rectb(1, 1, SCREEN_W - 2, SCREEN_H - 2, color2)
            pyxel.rectb(2, 2, SCREEN_W - 4, SCREEN_H - 4, color1)
            return

        if self.stage == 1 and not self.gameover:
            pulse = (pyxel.frame_count // 12) % 2
            color = 8 if pulse == 0 else 2

            pyxel.rectb(0, 0, SCREEN_W, SCREEN_H, color)
            pyxel.rectb(1, 1, SCREEN_W - 2, SCREEN_H - 2, color)

    def draw_cursor(self):
        if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
            u, v = 32, 112
        else:
            u, v = 32, 96

        pyxel.blt(
            pyxel.mouse_x,
            pyxel.mouse_y,
            0,
            u,
            v,
            16,
            16,
            0
        )

    def draw_tutorial_screen(self):
        ox, oy = self.get_shake_offset()

        self.draw_sky(ox, oy)
        self.draw_trees(ox, oy)
        self.draw_ground_base(ox, oy)
        self.draw_leaves(ox, oy)
        self.draw_leaf_apples(ox, oy)

        # No gauges during the tutorial, but keep the top band black instead of empty sky.
        pyxel.rect(0, 0, SCREEN_W, UI_H, 0)
        pyxel.line(0, UI_H - 1, SCREEN_W, UI_H - 1, 7)

        if self.tutorial_apple is not None:
            self.tutorial_apple.draw_trail(ox, oy)
            self.tutorial_apple.draw(ox, oy)

        self.draw_ground_items_foreground(ox, oy)

        pyxel.rect(18, 22, 164, 28, 1)
        pyxel.rectb(18, 22, 164, 28, 7)
        draw_big_text(45, 29, "TUTORIAL", 2, 10, 0)

        if self.tutorial_phase == "catch":
            draw_big_text(47, 62, "CLICK!", 3, 7, 0)
            if (pyxel.frame_count // 12) % 2 == 0:
                pyxel.rect(34, 158, 132, 18, 1)
                pyxel.rectb(34, 158, 132, 18, 10)
                pyxel.text(52, 165, "CLICK THE APPLE", 10)
        elif self.tutorial_phase == "hold":
            draw_big_text(55, 62, "HOLD!", 3, 11, 0)
            if (pyxel.frame_count // 12) % 2 == 0:
                pyxel.rect(22, 158, 156, 18, 1)
                pyxel.rectb(22, 158, 156, 18, 11)
                pyxel.text(42, 165, "HOLD CLICK TO REPEL", 11)
        else:
            draw_big_text(53, 62, "READY!", 3, 7, 0)
            if self.tutorial_phase_frame > 24:
                pyxel.text(65, 166, "GAUGES ONLINE", 10)
            if self.tutorial_phase_frame > 34:
                self.draw_ui()

        self.draw_sparks(ox, oy)
        self.draw_popups(ox, oy)
        self.draw_force_field()
        self.draw_cursor()

    def draw_title_screen(self):
        ox = 0
        oy = 0

        self.draw_background(ox, oy)

        self.face = FACE_NORMAL
        self.draw_newton(ox, oy)

        apple_y = 80 + int(pyxel.sin(pyxel.frame_count * 4) * 4)
        pyxel.blt(150, apple_y, 0, 32, 0, 16, 16, 0)

        self.draw_leaves(ox, oy)
        self.draw_leaf_apples(ox, oy)
        self.draw_ground_items_foreground(ox, oy)

        pyxel.rect(4, 22, 192, 86, 1)
        pyxel.rectb(4, 22, 192, 86, 7)
        pyxel.rectb(6, 24, 188, 82, 10)

        draw_big_text(16, 34, "DON'T LET NEWTON", 2, 7, 0)
        draw_big_text(34, 62, "FIND GRAVITY!", 2, 10, 8)

        pyxel.text(25, 126, "CLICK APPLE : GET", 7)
        pyxel.text(25, 138, "CLICK / SPACE START", 10)

        if (pyxel.frame_count // 15) % 2 == 0:
            pyxel.text(66, 174, "PRESS START", 7)

        self.draw_cursor()

    def draw(self):
        if self.scene == "title":
            self.draw_title_screen()
            return

        if self.scene == "tutorial":
            self.draw_tutorial_screen()
            return

        ox, oy = self.get_shake_offset()

        self.draw_background(ox, oy)
        self.draw_blackhole_effect(ox, oy)

        for apple in self.apples:
            apple.draw_trail(ox, oy)

        self.draw_newton(ox, oy)
        self.draw_notes(ox, oy)

        self.draw_leaves(ox, oy)
        self.draw_leaf_apples(ox, oy)

        for apple in self.apples:
            apple.draw(ox, oy)

        self.draw_apple_focus_markers(ox, oy)
        self.draw_newton_talk()
        self.draw_special_effect(ox, oy)
        self.draw_discovery_effect()

        self.draw_score()
        self.draw_ground_items_foreground(ox, oy)

        self.draw_sparks(ox, oy)
        self.draw_popups(ox, oy)

        self.draw_ui()
        self.draw_stage_alert()
        self.draw_force_field()
        self.draw_gameover_message()
        self.draw_cursor()


App()
