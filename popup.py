# popup.py
import pygame
import os

FONT_PATH = os.path.join("fonts", "THSarabunNew.ttf")

def show_choice_popup(screen, width, height):
    font = pygame.font.Font(FONT_PATH, 48)
    small_font = pygame.font.Font(FONT_PATH, 36)

    popup_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    popup_surface.fill((0, 0, 0, 100))  # โปร่งใส

    # กล่องกลาง
    box_width, box_height = 500, 300
    box_x = (width - box_width) // 2
    box_y = (height - box_height) // 2
    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

    # ปุ่ม
    button1_rect = pygame.Rect(box_x + 50, box_y + 200, 150, 50)
    button2_rect = pygame.Rect(box_x + 300, box_y + 200, 150, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button1_rect.collidepoint(event.pos):
                    return 1  # ส่งการ์ด 1 ใบ
                elif button2_rect.collidepoint(event.pos):
                    return 2  # ส่งการ์ด 2 ใบ

        # วาดพื้นหลัง
        popup_surface.fill((0, 0, 0, 180))
        pygame.draw.rect(popup_surface, (255, 255, 255), box_rect, border_radius=20)

        # ข้อความ
        text = font.render("คิดดี พูดดี ทำดี", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, box_y + 80))
        popup_surface.blit(text, text_rect)

        # วาดปุ่ม
        pygame.draw.rect(popup_surface, (200, 200, 255), button1_rect, border_radius=10)
        pygame.draw.rect(popup_surface, (200, 255, 200), button2_rect, border_radius=10)

        button1_text = small_font.render("ไม่อ่าน (ส่ง 1 ใบ)", True, (0, 0, 0))
        button2_text = small_font.render("อ่าน (ส่ง 2 ใบ)", True, (0, 0, 0))
        popup_surface.blit(button1_text, button1_text.get_rect(center=button1_rect.center))
        popup_surface.blit(button2_text, button2_text.get_rect(center=button2_rect.center))

        screen.blit(popup_surface, (0, 0))
        pygame.display.flip()
