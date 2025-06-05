import os
try:
    import pygame
except:
    os.system("pip install pygame")
    import pygame
import win32api
import win32con
import win32gui
import time


def show_reaction_time(x, y, scale, driver_name, reaction_time):
    pygame.init()
    w, h = pygame.display.Info().current_w, pygame.display.Info().current_h
    fuchsia = (255, 0, 128)

    screen = pygame.display.set_mode((w, h), pygame.NOFRAME)
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY)

    exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, exstyle | win32con.WS_EX_TRANSPARENT)

    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)

    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)

    screen.fill(fuchsia)
    pygame.display.update()

    image_width, image_height = 300*scale, 92*scale

    if x == "auto":
        x = int(w/2-image_width/2)
    if y == "auto":
        y = int(h/2-image_height/2)


    sec_from_start = 0
    time_from_start = 0

    title_fade_time = 0
    title_alpha = 0

    line_fade_time = 0
    line_length = 2

    text1_fade_time = 0
    text1_alpha = 0

    image2_fade_time = 0
    image2_alpha = 0
    image2_an = False

    image = pygame.image.load("Icons/Nocolor template.png")
    image = pygame.transform.scale(image, (image_width, image_height))

    if reaction_time < 0.3:
        image2 = pygame.image.load("Icons/Green template.png")
    elif reaction_time < 0.4:
        image2 = pygame.image.load("Icons/Orange template.png")
    else:
        image2 = pygame.image.load("Icons/Red template.png")

    image2 = pygame.transform.scale(image2, (image_width, image_height))

    image2.set_alpha(0)

    font_italic = pygame.font.Font("Fonts/F1-Italic.ttf", int(round(14*scale, 0)))
    font_bold = pygame.font.Font("Fonts/F1-Bold.ttf", int(round(30*scale, 0)))

    title = font_italic.render(f"{driver_name}'s reaction time", True, (255, 255, 255))
    title.set_alpha(0)
    text1 = font_bold.render(str(round(reaction_time, 3)), True, (255, 255, 255))
    text1.set_alpha(0)

    text1_an_done = False
    title_an_done = False

    backward_an = False
    y_rect_diff = 0

    disappear_time = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                run = False

        screen.fill(fuchsia)
        screen.blit(image, (x, y))
        screen.blit(image2, (x, y))

        screen.blit(title, (x+image.get_width()/2-title.get_width()/2, y+5))

        if sec_from_start > 1:
            if round(time.time(), 4) != round(line_fade_time, 4):

                pygame.draw.line(screen, (255, 255, 255), (x+image.get_width()/line_length, y+image.get_height()/3), (x+image.get_width()-image.get_width()/line_length, y+image.get_height()/3), 2)


                if line_length < 11:
                    line_length += 0.1*scale
                else:
                    pass
                line_fade_time = time.time()

        screen.blit(text1, (x+image.get_width()/2-text1.get_width()/2, y+image.get_height()/1.6-text1.get_height()/2))
    
        if not title_an_done and round(time.time(), 4) != round(title_fade_time, 4):
            title.set_alpha(title_alpha)
            if title_alpha < 200:
                title_alpha += 1*scale
            elif title_alpha < 255:
                title_alpha += 7*scale
            else:
                title_an_done = True
            title_fade_time = time.time()

        if not text1_an_done and sec_from_start > 2:
            if round(time.time(), 4) != round(text1_fade_time, 4):
                text1.set_alpha(text1_alpha)
                if text1_alpha < 200:
                    text1_alpha += 1*scale
                elif text1_alpha < 255:
                    text1_alpha += 7*scale
                else:
                    time.sleep(0.1)

                    image2_an = True
                    text1_an_done = True
                text1_fade_time = time.time()

        if image2_an:
            if round(time.time(), 4) != round(image2_fade_time, 4):
                image2.set_alpha(image2_alpha)
                image2_alpha += 1*scale

                if image2_alpha > 255:
                    image2_an = False
                    backward_an = True
                    time.sleep(2)
                    image.set_alpha(0)

                image2_fade_time = time.time()

        if backward_an:
            if round(time.time(), 4) != round(disappear_time, 4):
                pygame.draw.rect(screen, fuchsia, (x, y+image.get_height()-y_rect_diff, image_width, image_height+10*scale))

                y_rect_diff += 0.7*(scale*scale)

                if y_rect_diff > image_height+5*scale:
                    backward_an = False
                    time.sleep(0.5)
                    run = False

                disappear_time = time.time()

        if round(time.time(), 1) != round(time_from_start, 1):
            sec_from_start += 0.1
            time_from_start = time.time()

        pygame.display.update()

    pygame.quit()
