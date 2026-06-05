import arcade
import random
import math

# 상수 설정
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "극악의 죽창 피하기 (Fix)"

PLAYER_SPEED = 5
BULLET_SPEED_MIN = 6
BULLET_SPEED_MAX = 12
SPAWN_RATE = 0.15 # 탄막 생성 주기 (낮을수록 지옥)

class DeathSpearGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        self.player_list = None
        self.bullet_list = None
        self.player_sprite = None
        
        self.score = 0
        self.game_over = False

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

    def setup(self):
        """게임 초기화 및 재시작"""
        self.player_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.score = 0
        self.game_over = False

        # [수정] 내장 이미지 대신 금색 '원(Circle)' 모양 스프라이트 직접 생성
        # 아케이드 버전에 따라 인자 순서가 다를 수 있어 키워드 인자(radius, color) 지정
        self.player_sprite = arcade.SpriteCircle(radius=12, color=arcade.color.GOLD)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = SCREEN_HEIGHT // 2
        self.player_list.append(self.player_sprite)

        # 주기적으로 죽창 생성
        arcade.schedule(self.spawn_spear, SPAWN_RATE)

    def spawn_spear(self, delta_time):
        """화면 바깥 사방에서 플레이어를 향해 날아오는 죽창 생성"""
        if self.game_over:
            return

        # [수정] 내장 이미지 대신 빨간색 사각형을 가시(죽창)로 사용
        spear = arcade.SpriteSolidColor(width=25, height=8, color=arcade.color.RED)

        # 0: 위, 1: 아래, 2: 왼쪽, 3: 오른쪽 (화면 밖 랜덤 위치)
        start_edge = random.randint(0, 3)
        if start_edge == 0: # 위
            spear.center_x = random.randint(0, SCREEN_WIDTH)
            spear.center_y = SCREEN_HEIGHT + 20
        elif start_edge == 1: # 아래
            spear.center_x = random.randint(0, SCREEN_WIDTH)
            spear.center_y = -20
        elif start_edge == 2: # 왼쪽
            spear.center_x = -20
            spear.center_y = random.randint(0, SCREEN_HEIGHT)
        else: # 오른쪽
            spear.center_x = SCREEN_WIDTH + 20
            spear.center_y = random.randint(0, SCREEN_HEIGHT)

        # 플레이어의 현재 위치를 겨냥하여 각도 계산 (조준탄)
        dest_x = self.player_sprite.center_x
        dest_y = self.player_sprite.center_y

        x_diff = dest_x - spear.center_x
        y_diff = dest_y - spear.center_y
        angle = math.atan2(y_diff, x_diff)

        # 속도 및 방향 설정
        speed = random.uniform(BULLET_SPEED_MIN, BULLET_SPEED_MAX)
        spear.change_x = math.cos(angle) * speed
        spear.change_y = math.sin(angle) * speed
        
        # 투사체가 날아가는 방향으로 이미지 회전
        spear.angle = math.degrees(angle)

        self.bullet_list.append(spear)

    def on_draw(self):
        """화면 그리기"""
        self.clear()

        self.bullet_list.draw()
        self.player_list.draw()

        # 점수 표시
        arcade.draw_text(f"SCORE: {int(self.score)}", 10, SCREEN_HEIGHT - 30, arcade.color.WHITE, 16)

        # 게임 오버 메시지
        if self.game_over:
            arcade.draw_text("GAME OVER", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20,
                             arcade.color.RED, 40, anchor_x="center")
            arcade.draw_text("Press 'R' to Restart", SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30,
                             arcade.color.WHITE, 20, anchor_x="center")

    def on_update(self, delta_time):
        """게임 로직 업데이트"""
        if self.game_over:
            return

        self.score += delta_time * 100

        # 플레이어 이동 처리
        if self.left_pressed and self.player_sprite.left > 0:
            self.player_sprite.center_x -= PLAYER_SPEED
        if self.right_pressed and self.player_sprite.right < SCREEN_WIDTH:
            self.player_sprite.center_x += PLAYER_SPEED
        if self.up_pressed and self.player_sprite.top < SCREEN_HEIGHT:
            self.player_sprite.center_y += PLAYER_SPEED
        if self.down_pressed and self.player_sprite.bottom > 0:
            self.player_sprite.center_y -= PLAYER_SPEED

        # 탄막 이동 및 화면 밖 제거
        self.bullet_list.update()
        for bullet in self.bullet_list:
            if (bullet.center_x < -50 or bullet.center_x > SCREEN_WIDTH + 50 or
                bullet.center_y < -50 or bullet.center_y > SCREEN_HEIGHT + 50):
                bullet.remove_from_sprite_lists()

        # 충돌 감지
        if arcade.check_for_collision_with_list(self.player_sprite, self.bullet_list):
            self.game_over = True
            arcade.unschedule(self.spawn_spear)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.R and self.game_over:
            self.setup()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False

def main():
    game = DeathSpearGame()
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()
