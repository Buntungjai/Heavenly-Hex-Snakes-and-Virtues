import pygame
from score import calculate_score_details, draw_score_summary

#special_tiles = {
#    "white_red": [7, 19, 32]
#}


def draw_board(screen, row_lengths, tile_colors, players, current_player, special_tiles):

    tile_size = 40
    margin = 20
    board_top = margin
    screen_width = screen.get_width()

    tile_number = 1

    for row_index, tiles_in_row in enumerate(row_lengths):
        row_y = board_top + row_index * (tile_size + 5)
        row_width = tiles_in_row * (tile_size + 5)
        row_left = (screen_width - row_width) // 2

        for col in range(tiles_in_row):
            tile_x = row_left + col * (tile_size + 5)

            # ตรวจสอบว่าเป็นช่องขาวขอบแดงไหม
            if tile_number in special_tiles.get("white_red", []):
                pygame.draw.rect(screen, (255, 255, 255), (tile_x, row_y, tile_size, tile_size))  # พื้นขาว
                pygame.draw.rect(screen, (200, 0, 0), (tile_x, row_y, tile_size, tile_size), 4)    # ขอบแดง
            else:
                tile_color = tile_colors.get(tile_number, (80, 80, 80))
                pygame.draw.rect(screen, tile_color, (tile_x, row_y, tile_size, tile_size))


            # หมายเลขช่อง
            font = pygame.font.SysFont(None, 16)
            num_text = font.render(str(tile_number), True, (255, 255, 255))
            screen.blit(num_text, (tile_x + 5, row_y + 5))

            # วาดผู้เล่น
            for player in players:
                if player.tile == tile_number:
                    pygame.draw.circle(screen, player.color, (tile_x + 20, row_y + 20), 10)

            tile_number += 1

    # --- วาดคะแนนของผู้เล่นปัจจุบัน ---
    if players:
        # --- แสดงชื่อผู้เล่นปัจจุบัน ---
        font_title = pygame.font.SysFont(None, 28)
        title_text = font_title.render(f"Current Player: {current_player.name}", True, current_player.color)
        screen.blit(title_text, (1200, 60))

        # --- แสดงคะแนนของผู้เล่นปัจจุบัน ---
        font = pygame.font.SysFont(None, 24)
        score_summary, white_total, dark_total = calculate_score_details(current_player.cards)
        draw_score_summary(screen, font, score_summary, white_total, dark_total)
