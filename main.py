import pygame
import random

pygame.init()

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 255, 0)
WIDTH = 400
HEIGHT = 500

# Загрузка изображений
background = pygame.transform.scale(pygame.image.load('doodle_background.jpg'), (400, 500))
player_img = pygame.transform.scale(pygame.image.load('doodlejumper.png'), (90, 70))

# Игровые переменные
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
timer = pygame.time.Clock()
score = 0
high_score = 0
game_over = False
game_state = 'menu'  #

# Переменные, связанные с игроком
player_x = 170
player_y = 400
player_speed = 3
super_jumps = 2
jump = False
y_change = 0
x_change = 0

# Платформы
platforms = [[175, 475, 70, 10], [85, 370, 70, 10], [265, 370, 70, 10],
             [175, 260, 70, 10], [85, 150, 70, 10], [265, 150, 70, 10], [175, 40, 70, 10]]

# Экран
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Doodle Jump')

# Хранение рекорда

def load_high_score():
    try:
        with open('high_score.txt', 'r') as f:
            return int(f.read())
    except:
        return 0  # если файл пуст или поврежден — обнуляем

def save_high_score(score):
    try:
        with open('high_score.txt', 'w') as f:
            f.write(str(score))
    except:
        pass  # ошибка записи — просто игнор

high_score = load_high_score()

# Проверка коллизий
def check_collisions(rect_list, j):
    for rect in rect_list:
        if rect.colliderect([player_x + 30, player_y + 60, 30, 5]) and not j and y_change > 0:
            return True
    return j

# Обновление позиции игрока
def update_player(y_pos):
    global jump, y_change
    jump_height = 10
    gravity = 0.4
    if jump:
        y_change = -jump_height
        jump = False
    y_pos += y_change
    y_change += gravity
    return y_pos

# Обновление платформ
def update_platforms(my_list, y_pos, change):
    global score
    if y_pos < 250 and y_change < 0:
        for plat in my_list:
            plat[1] -= change
    for plat in my_list:
        if plat[1] > HEIGHT:
            plat[0] = random.randint(10, 320)
            plat[1] = random.randint(-50, -10)
            score += 1
    return my_list

# Сброс игры
def reset_game():
    global player_x, player_y, y_change, x_change, platforms, score, super_jumps, game_over
    player_x = 170
    player_y = 400
    y_change = 0
    x_change = 0
    super_jumps = 2
    score = 0
    game_over = False
    platforms[:] = [[175, 475, 70, 10], [85, 370, 70, 10], [265, 370, 70, 10],
                    [175, 260, 70, 10], [85, 150, 70, 10], [265, 150, 70, 10], [175, 40, 70, 10]]

# Главный цикл
running = True
while running:
    timer.tick(fps)
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            save_high_score(high_score)
            running = False

        if event.type == pygame.KEYDOWN:
            if game_state == 'menu' and event.key == pygame.K_SPACE:
                game_state = 'playing'
                reset_game()

            if game_state == 'game_over' and event.key == pygame.K_SPACE:
                game_state = 'playing'
                reset_game()

            if game_state == 'playing':
                if event.key == pygame.K_w and super_jumps > 0:
                    super_jumps -= 1
                    y_change = -15
                if event.key == pygame.K_a:
                    x_change = -player_speed
                if event.key == pygame.K_d:
                    x_change = player_speed

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_a, pygame.K_d):
                x_change = 0

    if game_state == 'menu':
        title = font.render("DOODLE JUMP", True, black)
        prompt = font.render("Нажми ПРОБЕЛ, чтобы начать", True, black)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 240))

    elif game_state == 'playing':
        screen.blit(player_img, (player_x, player_y))
        blocks = []

        for plat in platforms:
            block = pygame.draw.rect(screen, green, plat, 0, 3)
            blocks.append(block)

        jump = check_collisions(blocks, jump)
        player_x += x_change
        player_y = update_player(player_y) if player_y < 440 else player_y

        if player_y >= 440:
            game_over = True
            y_change = 0
            x_change = 0
            game_state = 'game_over'

        platforms = update_platforms(platforms, player_y, y_change)

        if player_x < -20:
            player_x = -20
        elif player_x > 330:
            player_x = 330

        if score > high_score:
            high_score = score

        screen.blit(font.render(f'Score: {score}', True, black), (10, 10))
        screen.blit(font.render(f'High Score: {high_score}', True, black), (10, 30))

    elif game_state == 'game_over':
        over_text = font.render("GAME OVER", True, black)
        prompt = font.render("Нажми ПРОБЕЛ, чтобы сыграть снова", True, black)
        final_score = font.render(f'Ваш счёт: {score}', True, black)
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, 200))
        screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, 230))
        screen.blit(prompt, (WIDTH // 2 - prompt.get_width() // 2, 260))

    pygame.display.flip()

pygame.quit()
