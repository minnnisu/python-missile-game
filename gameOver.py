from share import IMAGES_DIR, FONT_DIR, BACKGROUND_COLOR, FONT_COLOR


def DieUser(monitor, pygame, sheight):
    r = BACKGROUND_COLOR['r']
    g = BACKGROUND_COLOR['g']
    b = BACKGROUND_COLOR['b']

    myfont = pygame.font.Font(FONT_DIR + 'NanumGothic.ttf', 20)
    txt = myfont.render('Game Over', True,
                        (FONT_COLOR['r'], FONT_COLOR['g'], FONT_COLOR['b']))

    button_image = pygame.image.load(
        IMAGES_DIR + "retry-button.png")  # 버튼 이미지 파일 경로
    button_rect = button_image.get_rect()
    button_rect.center = (400, 300)  # 버튼의 위치 (x, y)

    running = True

    while running:
        (pygame.time.Clock()).tick(100)  # 게임 진행을 늦춘다(10~100 정도가 적당).
        monitor.fill((r, g, b))  # 배경 색칠
        monitor.blit(txt, (100, sheight - 100))
        monitor.blit(button_image, button_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 버튼을 눌렀을 때
                if event.button == 1:  # 마우스 왼쪽 버튼을 클릭했을 때
                    mouse_pos = pygame.mouse.get_pos()  # 마우스 위치 가져오기
                    if button_rect.collidepoint(mouse_pos):  # 버튼 위에서 클릭한 경우
                        print("Button Clicked!")
        pygame.display.update()
