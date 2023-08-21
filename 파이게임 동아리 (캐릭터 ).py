import pygame
import sys
import random

# 파이게임 초기화
pygame.init()

# 화면 크기 설정
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Combined Game Example")

# 색깔 정의
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# 원 초기 설정
circle_radius = 100
circle_color = black
circle_center = (screen_width // 2, screen_height // 2)

# 네모 초기 설정
square_size = 10
square_color = red
square_position = [circle_center[0], circle_center[1] - circle_radius + square_size]

# 동그라미 초기 설정
circle_radius_2 = 20
circle_color_2 = blue
circle_position = [circle_center[0], circle_center[1]]

# 타이머 설정
timer_font = pygame.font.Font(None, 36)
start_time = pygame.time.get_ticks()
time_limit = 3 * 60 * 1000  # 3분 (밀리초 단위)
timer_expired = False
size_update_interval = 30 * 1000  # 30초 (밀리초 단위)
last_size_update_time = start_time

# 게임 루프
clock = pygame.time.Clock()

moving_speed = 5
circle_health = 3

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 원 크기 조절
    current_time = pygame.time.get_ticks()
    if not timer_expired:
        elapsed_time = current_time - start_time
        if elapsed_time >= time_limit:
            timer_expired = True
        else:
            if current_time - last_size_update_time >= size_update_interval:
                last_size_update_time = current_time
                circle_radius = max(0, circle_radius - 5)  # 5씩 줄어듦

    # 동그라미 이동 및 체력 감소
    keys = pygame.key.get_pressed()
    if not timer_expired:
        if keys[pygame.K_LEFT]:
            circle_position[0] -= 5
        if keys[pygame.K_RIGHT]:
            circle_position[0] += 5
        if keys[pygame.K_UP]:
            circle_position[1] -= 5
        if keys[pygame.K_DOWN]:
            circle_position[1] += 5

        # 동그라미가 원 안에 있는지 확인
        dx = circle_position[0] - circle_center[0]
        dy = circle_position[1] - circle_center[1]
        if dx ** 2 + dy ** 2 > circle_radius ** 2:
            # 동그라미가 원 바깥으로 나가면 체력 감소
            circle_health = max(0, circle_health - 1)
            circle_position[0] = circle_center[0]
            circle_position[1] = circle_center[1]
            if circle_health == 0:
                running = False  # 체력이 0이면 게임 종료

    # 네모 이동
    square_position = [square_position[0] + 2, square_position[1]]

    # 화면 업데이트
    screen.fill(white)
    pygame.draw.circle(screen, circle_color, circle_center, circle_radius)
    pygame.draw.rect(screen, square_color, (square_position[0], square_position[1], square_size, square_size))
    pygame.draw.circle(screen, circle_color_2, circle_position, circle_radius_2)

    # 체력 표시
    health_text = timer_font.render(f"Health: {circle_health}", True, black)
    screen.blit(health_text, (10, 10))

    # 타이머 표시
    if not timer_expired:
        remaining_time = max(0, (time_limit - elapsed_time) // 1000)
        timer_text = timer_font.render(f"Time: {remaining_time // 60:02}:{remaining_time % 60:02}", True, black)
        timer_rect = timer_text.get_rect(center=(screen_width // 2, 50))
        screen.blit(timer_text, timer_rect)

    pygame.display.flip()

    # 초당 프레임 설정
    clock.tick(60)

# 파이게임 종료
pygame.quit()
sys.exit()
