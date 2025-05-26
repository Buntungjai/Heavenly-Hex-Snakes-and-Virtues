import pygame

# ควรจะมี WIDTH และ HEIGHT ที่กำหนดไว้ใน main.py หรือ constants.py
WIDTH = 1500
HEIGHT = 1000

def draw_player_cards(screen, font, players, current_player_index):
    cards = players[current_player_index].cards
    card_width = 160
    card_height = 50
    spacing_x = 15
    spacing_y = 10  # ระยะห่างแนวตั้งระหว่างแถวการ์ด

    cards_per_row = 8

    # คำนวณตำแหน่งเริ่มต้นแนวนอนให้อยู่กึ่งกลางจอสำหรับ 5 ใบ
    start_x = (WIDTH - ((card_width + spacing_x) * cards_per_row - spacing_x)) // 2
    # เริ่มวาดจากล่างสุดก่อน (ปรับ y ขึ้นบนเรื่อย ๆ ตามจำนวนแถว)
    start_y = HEIGHT - card_height - 20

    card_rects = []

    for i, card in enumerate(cards):
        row = i // cards_per_row
        col = i % cards_per_row

        x = start_x + col * (card_width + spacing_x)
        y = start_y - row * (card_height + spacing_y)

        card_rect = pygame.Rect(x, y, card_width, card_height)
        card_rects.append((card_rect, i))

        # สีพื้นและขอบตามประเภทการ์ด
        type_colors = {
            "red-white":      ((255, 230, 230), (200, 0, 0), (0, 0, 0)),
            "orange-white":   ((255, 245, 230), (255, 140, 0), (0, 0, 0)),
            "green-white":    ((230, 255, 230), (0, 150, 0), (0, 0, 0)),
            "red-dark":       ((90, 0, 0), (200, 0, 0), (255, 255, 255)),
            "orange-dark":    ((120, 60, 0), (255, 140, 0), (255, 255, 255)),
            "green-dark":     ((0, 80, 0), (0, 180, 0), (255, 255, 255)),
        }

        bg_color, border_color, text_color = type_colors.get(
            card["type"],
            ((50, 50, 50), (100, 100, 100), (255, 255, 255))
        )

        # วาดการ์ด
        pygame.draw.rect(screen, bg_color, card_rect)
        pygame.draw.rect(screen, border_color, card_rect, 3)

        # ข้อความบนการ์ด
        name_surface = font.render(card["name"], True, text_color)
        point_surface = font.render(f"{card['points']} pts", True, text_color)
        key_surface = font.render(f"[{i+1}]", True, text_color)

        screen.blit(name_surface, (x + 5, y + 5))
        screen.blit(point_surface, (x + 5, y + 25))
        screen.blit(key_surface, (x + card_width - 30, y + 5))

    return card_rects
