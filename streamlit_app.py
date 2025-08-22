import pygame
import sys
import time

# -------------------------------
# 초기화
# -------------------------------
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Click Tycoon")

clock = pygame.time.Clock()
FPS = 60

# 색상
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RAINBOW = [(255,0,0),(255,127,0),(255,255,0),(0,255,0),(0,0,255),(75,0,130),(148,0,211)]

# -------------------------------
# 게임 변수
# -------------------------------
gold = 0
click_value = 1
GOAL = 99999
game_over = False

# 상점 상태
shop = {
    "auto1": False,   # 100골드, 5초 1골드
    "auto2": False,   # 300골드, 8초 4골드
    "party": False,   # 500골드, 클릭 3배, 쿨타임 20초, 활성 7초
    "auto3": False,   # 1000골드, 5초 30골드
    "auto4": False    # 5000골드, 4초 50골드
}

# 시간 추적
last_auto1 = time.time()
last_auto2 = time.time()
last_auto3 = time.time()
last_auto4 = time.time()
party_last_used = -20
party_active_until = 0

# 클릭 버튼
click_btn = pygame.Rect(WIDTH//2-15, HEIGHT//2-15, 30, 30)

# 상점 버튼
shop_buttons = {
    "100": pygame.Rect(50, 50, 100, 30),
    "300": pygame.Rect(50, 90, 100, 30),
    "500": pygame.Rect(50, 130, 100, 30),
    "1000": pygame.Rect(50, 170, 100, 30),
    "5000": pygame.Rect(50, 210, 100, 30)
}

font = pygame.font.SysFont(None, 24)

# -------------------------------
# 게임 루프
# -------------------------------
running = True
while running:
    clock.tick(FPS)
    current_time = time.time()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 클릭 처리
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            if click_btn.collidepoint(event.pos):
                if shop["party"] and current_time <= party_active_until:
                    gold += click_value*3
                else:
                    gold += click_value
                if gold >= GOAL:
                    gold = GOAL
                    game_over = True

            # 상점 버튼 클릭
            if shop_buttons["100"].collidepoint(event.pos) and gold >= 100:
                gold -= 100
                shop = {"auto1": True, "auto2": False, "party": False, "auto3": False, "auto4": False}
            if shop_buttons["300"].collidepoint(event.pos) and gold >= 300:
                gold -= 300
                shop = {"auto1": False, "auto2": True, "party": False, "auto3": False, "auto4": False}
            if shop_buttons["500"].collidepoint(event.pos) and gold >= 500:
                gold -= 500
                shop = {"auto1": False, "auto2": False, "party": True, "auto3": False, "auto4": False}
                party_last_used = current_time
                party_active_until = current_time + 7
            if shop_buttons["1000"].collidepoint(event.pos) and gold >= 1000:
                gold -= 1000
                shop = {"auto1": False, "auto2": False, "party": False, "auto3": True, "auto4": False}
            if shop_buttons["5000"].collidepoint(event.pos) and gold >= 5000:
                gold -= 5000
                shop = {"auto1": False, "auto2": False, "party": False, "auto3": False, "auto4": True}

    # -------------------------------
    # 자동 골드
    # -------------------------------
    if not game_over:
        if shop["auto1"] and current_time - last_auto1 >= 5:
            gold += 1
            last_auto1 = current_time
        if shop["auto2"] and current_time - last_auto2 >= 8:
            gold += 4
            last_auto2 = current_time
        if shop["auto3"] and current_time - last_auto3 >= 5:
            gold += 30
            last_auto3 = current_time
        if shop["auto4"] and current_time - last_auto4 >= 4:
            gold += 50
            last_auto4 = current_time
        if shop["party"] and current_time - party_last_used >= 20:
            party_last_used = current_time
            party_active_until = current_time + 7
        if gold >= GOAL:
            gold = GOAL
            game_over = True

    # -------------------------------
    # 화면 그리기
    # -------------------------------
    screen.fill(WHITE)

    # 클릭 버튼
    if shop["party"] and current_time <= party_active_until:
        color_idx = int((current_time*10)%7)
        pygame.draw.ellipse(screen, RAINBOW[color_idx], click_btn)
    elif game_over:
        pygame.draw.ellipse(screen, GRAY, click_btn)
    else:
        pygame.draw.ellipse(screen, RED, click_btn)

    # 상점 버튼
    for key, rect in shop_buttons.items():
        pygame.draw.rect(screen, BLACK, rect)
        text = font.render(f"{key} 골드", True, WHITE)
        screen.blit(text, (rect.x+5, rect.y+5))

    # 골드 표시
    gold_text = font.render(f"Gold: {gold}", True, BLACK)
    screen.blit(gold_text, (WIDTH-150, 50))

    # 목표 달성 메시지
    if game_over:
        msg = font.render("축하합니다! 목표 99999 골드 달성!", True, RED)
        screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - 50))

    pygame.display.flip()

pygame.quit()
sys.exit()
