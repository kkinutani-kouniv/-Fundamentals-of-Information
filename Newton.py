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

SPECIAL_MAX = 5
SPECIAL_FREEZE_TIME = 120

FPS = 30
DIFFICULTY_START_FRAME = FPS * 60
DIFFICULTY_UP_FRAME = FPS * 20
DIFFICULTY_SCORE_STEP = 350
DIFFICULTY_MAX = 6

TALK_INTERVAL = FPS * 8
TALK_DURATION = FPS * 3

START_APPLE_COUNT = 4
MAX_APPLE_COUNT = 7

APPLE_W = 16
APPLE_H = 16

CLICK_W = 12
CLICK_H = 12

FORCE_W = 22
FORCE_H = 22

APPLE_COLLISION_SIZE = 12


BIG_FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01111", "10000", "10000", "10111", "10001", "10001", "01111"],
    "I": ["111", "010", "010", "010", "010", "010", "111"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
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
    def __init__(self, difficulty=0):
        self.reset(difficulty)

    def reset(self, difficulty=0):
        self.x = pyxel.rndi(8, SCREEN_W - APPLE_W - 8)
        self.y = pyxel.rndi(-180 - difficulty * 22, -16)

        self.vx = pyxel.rndf(
            -0.45 - difficulty * 0.08,
            0.45 + difficulty * 0.08
        )

        self.vy = pyxel.rndf(
            1.15 + difficulty * 0.16,
            2.25 + difficulty * 0.24
        )

        self.is_gold = pyxel.rndi(1, 100) <= 20
        self.trail = []

        self.hand_hit_cooldown = 0
        self.apple_hit_cooldown = 0

    def update(self, difficulty, frozen):
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

        max_vx = 3.2 + difficulty * 0.14
        max_vy = 4.2 + difficulty * 0.24

        self.vx = clamp(self.vx, -max_vx, max_vx)
        self.vy = clamp(
            self.vy + 0.014 + difficulty * 0.004,
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
            self.reset(difficulty)
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

    def draw_trail(self, ox, oy):
        for i, (tx, ty) in enumerate(self.trail):
            if i % 2 == 0:
                color = 10 if self.is_gold else 7
                pyxel.rect(int(tx) + ox, int(ty) + oy, 2, 2, color)

    def draw(self, ox, oy):
        frame = (pyxel.frame_count // 8) % 2

        if self.is_gold:
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


class App:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H, title="Newton No Gravity")
        pyxel.mouse(False)
        pyxel.load("assets.pyxres")

        self.scene = "title"

        self.apples = [Apple(0) for _ in range(START_APPLE_COUNT)]
        self.notes = []

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

    def start_game(self):
        self.reset_game()
        self.scene = "play"

    def reset_game(self):
        self.apples = [Apple(0) for _ in range(START_APPLE_COUNT)]
        self.notes.clear()

        self.shake_timer = 0
        self.edge_alert_timer = 0
        self.discovery_timer = 0

        self.score = 0
        self.miss_count = 0
        self.special_charge = 0
        self.special_timer = 0
        self.gameover = False

        self.play_frame = 0
        self.difficulty = 0

        self.face = FACE_NORMAL
        self.stage = 0
        self.prev_stage = 0

    def get_difficulty(self):
        if self.play_frame < DIFFICULTY_START_FRAME:
            return 0

        time_level = (self.play_frame - DIFFICULTY_START_FRAME) // DIFFICULTY_UP_FRAME
        score_level = self.score // DIFFICULTY_SCORE_STEP

        return min(DIFFICULTY_MAX, 1 + time_level + score_level)

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

    def adjust_apple_count(self):
        target = START_APPLE_COUNT + self.difficulty // 2
        target = min(MAX_APPLE_COUNT, target)

        while len(self.apples) < target:
            self.apples.append(Apple(self.difficulty))

    def try_activate_special(self):
        if self.special_charge >= SPECIAL_MAX and pyxel.btnp(pyxel.KEY_SPACE):
            self.special_charge = 0
            self.special_timer = SPECIAL_FREEZE_TIME
            self.shake_timer = max(self.shake_timer, 6)

    def collect_apple(self, apple):
        if apple.is_gold:
            self.score += 50
            self.special_charge = min(SPECIAL_MAX, self.special_charge + 1)
        else:
            self.score += 10

        apple.reset(self.difficulty)

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
            self.start_game()

        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.KEY_RETURN):
            self.start_game()

    def update(self):
        if self.scene == "title":
            self.update_title()
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

            for apple in self.apples:
                hit_ground = apple.update(self.difficulty, frozen)

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

    def get_shake_offset(self):
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

    def draw_trees(self, ox, oy):
        for x, y, u, v in self.tree_tiles:
            pyxel.blt(x + ox, y + oy, 0, u, v, 16, 16)

    def draw_ground_base(self, ox, oy):
        pyxel.rect(0 + ox, GROUND_Y + oy, SCREEN_W, GROUND_H, 4)
        pyxel.line(0 + ox, GROUND_Y + oy, SCREEN_W + ox, GROUND_Y + oy, 3)

    def draw_leaf_foreground(self, ox, oy):
        for x, y, u, v in self.leaf_tiles:
            if y == 0:
                continue
            pyxel.blt(x + ox, y + oy, 0, u, v, 16, 16, 0)

        for x, y, u, v in self.leaf_apples:
            pyxel.blt(x + ox, y + oy, 0, u, v, 16, 16, 0)

        for x, y, u, v, w, h in self.leaf_under_tiles:
            pyxel.blt(x + ox, y + oy, 0, u, v, w, h, 0)

    def draw_ground_items_foreground(self, ox, oy):
        for x, y, u, v in self.ground_items:
            pyxel.blt(x + ox, y + oy, 0, u, v, 16, 16, 0)

    def draw_background(self, ox, oy):
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
            pyxel.text(78, 58, "TIME STOP", 7)

        for apple in self.apples:
            pyxel.circb(int(apple.x) + 8 + ox, int(apple.y) + 8 + oy, 10, 7)

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

        miss_x = 6
        miss_y = 4
        miss_w = 120
        miss_h = 8

        pyxel.rect(miss_x, miss_y, miss_w, miss_h, 1)
        pyxel.rectb(miss_x, miss_y, miss_w, miss_h, 7)

        fill_w = int(miss_w * self.miss_count / MISS_MAX)
        if fill_w > 0:
            inner_w = max(1, fill_w - 2)
            pyxel.rect(miss_x + 1, miss_y + 1, inner_w, miss_h - 2, 8)

        stage_x = miss_x + int(miss_w * MISS_STAGE_1 / MISS_MAX)
        pyxel.line(stage_x, miss_y, stage_x, miss_y + miss_h - 1, 10)

        skill_x = 136
        skill_y = 4
        skill_w = 58
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
                pyxel.text(skill_x + 16, skill_y + 2, "SPACE", 0)

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

    def draw_title_screen(self):
        ox = 0
        oy = 0

        self.draw_background(ox, oy)

        self.face = FACE_NORMAL
        self.draw_newton(ox, oy)

        apple_y = 80 + int(pyxel.sin(pyxel.frame_count * 4) * 4)
        pyxel.blt(150, apple_y, 0, 32, 0, 16, 16, 0)

        self.draw_leaf_foreground(ox, oy)
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

        ox, oy = self.get_shake_offset()

        self.draw_background(ox, oy)

        for apple in self.apples:
            apple.draw_trail(ox, oy)

        self.draw_newton(ox, oy)
        self.draw_notes(ox, oy)

        for apple in self.apples:
            apple.draw(ox, oy)

        self.draw_newton_talk()
        self.draw_special_effect(ox, oy)
        self.draw_discovery_effect()

        self.draw_leaf_foreground(ox, oy)
        self.draw_score()
        self.draw_ground_items_foreground(ox, oy)

        self.draw_ui()
        self.draw_stage_alert()
        self.draw_force_field()
        self.draw_gameover_message()
        self.draw_cursor()


App()