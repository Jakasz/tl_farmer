
import pygame

import win32api
import win32con
import win32gui

class AreaOverlay:

    def runGame(self):

        pygame.init()
        info = pygame.display.Info()
        w = info.current_w
        h = info.current_h
        screen = pygame.display.set_mode((w, h), pygame.NOFRAME) # For borderless, use pygame.NOFRAME
        done = False
        fuchsia = (255, 0, 128)  # Transparency color

        # Create layered window
        hwnd = pygame.display.get_wm_info()["window"]
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                            win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
        # Set window transparency color
        win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 50, win32con.LWA_ALPHA)
        click1 = 0
        x1 = 0
        y1 = 0
        x2 = 0
        y2 = 0
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        x1 = 0
                        y1 = 0
                        x2 = 0
                        y2 = 0
                        done = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if click1 == 0:
                            x1, y1 = pygame.mouse.get_pos()
                            click1 = 1
                        elif click1 == 1:
                            x2, y2 = pygame.mouse.get_pos()    
                            win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_ALPHA)
                            click1 = 0
                            win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*fuchsia), 50, win32con.LWA_ALPHA)
                    
                            # x1 = 0
                            # y1 = 0
                            # x2 = 0
                            # y2 = 0

                            done = True
                            
            screen.fill((255, 255, 255))  # Transparent background

            # show_text()
            if click1 == 0:
                mx, my = pygame.mouse.get_pos()
            elif click1 == 1:
                mx2, my2 = pygame.mouse.get_pos()
                x2 = mx2 - x1
                y2 = my2 - y1

            pygame.draw.rect(screen, (0, 255, 255), pygame.Rect(mx, my, x2, y2))
            pygame.display.update()

        pygame.quit()

        return x1,y1,x2,y2