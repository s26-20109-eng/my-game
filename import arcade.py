import arcade
import random

# 상수 설정
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Arcade Crossy Road"
CHARACTER_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 40
CAR_SPEED_MIN = 2
CAR_SPEED_MAX = 5

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.AMAZON)

        # 리스트 선언
        self.player_list = None
        self.car_list = None
        self.player_sprite = None

    def setup(self):
        """게임 초기화"""
        self.player_list = arcade.SpriteList()
        self.car_list = arcade.SpriteList()

        # 플레이어 설정 (기본 아이콘 사용)
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/robot/robot_idle.png", CHARACTER_SCALING)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = 40
        self.player_list.append(self.player_sprite)

        # 일정 간격으로 자동차 생성 (0.5초마다)
        arcade.schedule(self.create_car, 0.5)

    def create_car(self, delta_time):
        """자동차 장애물 생성"""
        car = arcade.Sprite(":resources:images/items/gemBlue.png", 0.8) # 자동차 대신 보석 이미지 사용
        car.center_x = SCREEN_WIDTH + 50
        # 도로 라인처럼 보이게 40픽셀 단위로 랜덤 배치
        car.center_y = random.randrange(100, SCREEN_HEIGHT - 100, 80)
        car.change_x = -random.uniform(CAR_SPEED_MIN, CAR_SPEED_MAX)
        self.car_list.append(car)

    def on_draw(self):
        """화면 그리기"""
        self.clear()
        self.car_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """키보드 입력 처리"""
        if key == arcade.key.UP:
            self.player_sprite.center_y += PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.center_y -= PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.center_x -= PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.center_x += PLAYER_MOVEMENT_SPEED

    def on_update(self, delta_time):
        """게임 로직 업데이트"""
        self.car_list.update()

        # 화면 밖으로 나간 자동차 삭제
        for car in self.car_list:
            if car.right < 0:
                car.remove_from_sprite_lists()

        # 충돌 감지
        if arcade.check_for_collision_with_list(self.player_sprite, self.car_list):
            print("Game Over!")
            self.setup() # 충돌 시 초기화

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()