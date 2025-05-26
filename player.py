import pygame

class Player:
    def __init__(self, name, color, start_tile=71):
        self.name = name
        self.color = color
        self.tile = start_tile  # ใช้เป็นตำแหน่งหลักบนกระดาน
        self.position = start_tile  # เพิ่มไว้เพื่อใช้กับระบบบันได/งู
        self.score = 0  # ใช้กับเงื่อนไขพิเศษ เช่น บันไดต้องมีคะแนน
        self.cards = []
        self.direction = 1  # 1 = เดินไปข้างหน้า, -1 = เดินย้อนกลับ
        self.cards_sent_this_turn = 0

    def move(self, steps, row_lengths, screen, tile_colors, players, special_tiles):
        zones = [
            (41, 54),
            (71, 88),
            (55, 70),
            (80, 104),
            (105, 118),
        ]

        while steps > 0:
            self.tile += self.direction
            steps -= 1

            # ตรวจว่าอยู่ในโซนไหน
            for min_tile, max_tile in zones:
                if min_tile <= self.tile <= max_tile:
                    if self.tile >= max_tile:
                        self.tile = max_tile
                        self.direction = -1
                    elif self.tile <= min_tile:
                        self.tile = min_tile
                        self.direction = 1
                    break  # เจอโซนแล้วไม่ต้องเช็กต่อ
            else:
                # ถ้าไม่อยู่ในโซนใดเลย ให้ตกช่องสุดท้าย (หรืออะไรก็ได้ที่ต้องการ)
                self.tile = 158

            self.position = self.tile  # อัปเดต position

            self._redraw(screen, row_lengths, tile_colors, players,special_tiles)

    def _redraw(self, screen, row_lengths, tile_colors, players, special_tiles):
        from draw_board import draw_board
        screen.fill((30, 30, 30))
        draw_board(screen, row_lengths, tile_colors, players, self,special_tiles)


        pygame.display.flip()
        pygame.time.wait(100)  # 0.1 วินาที (เร็วขึ้นนิดนึง ถ้าอยาก 0.5 วินาที ให้ใช้ 500)

    def move_to_position(self, target_tile, row_lengths, screen, tile_colors, players, special_tiles):
        self.tile = target_tile
        self.position = target_tile
        self._redraw(screen, row_lengths, tile_colors, players, special_tiles)
        pygame.time.wait(200)
