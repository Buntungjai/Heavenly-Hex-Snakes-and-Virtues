import pygame
import sys
import random
from draw_board import draw_board
from player import Player
from snakes_and_ladders import BoardEvents
#from GameLogic import GameLogic
from card import CardManager
from ui import draw_player_cards
from turn_manager import TurnManager
from popup import show_choice_popup

# Initialize pygame
pygame.init()
screen_width, screen_height = 1500, 1000
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Bull Battle")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont("Arial", 24)

# ความยาวของแต่ละแถว
row_lengths = [4, 6, 8, 10, 12, 14, 16, 18, 16, 14, 12, 10, 8, 6, 4]

tile_colors = {


    71: (139, 69, 19),  # น้ำตาลไม้
    72: (0, 100, 0),    # แดงเข้ม
    73: (139, 0, 0),
    75: (255, 140, 0),   # ส้มเข้ม
   # 77: (255, 140, 0),
    78: (255, 140, 0),
    81: (0, 100, 0),     # เขียวเข้ม
    82: (0, 100, 0),
    90: (0, 100, 0),
    100: (0,100,0),

}

players = [
    Player("red", (255, 0, 0)),
    Player("green", (0, 200, 0)),
    Player("blue", (0, 0, 255))
]

current_player_index = 0
current_player = players[current_player_index]

board_events = BoardEvents()
#logic = GameLogic()
card_manager = CardManager()
card_manager.deal_initial_cards(players)
turn_manager = TurnManager(players)
turn_manager.set_card_manager(card_manager)

for player in players:
    print(f"{player.name} ได้การ์ด:")
    for card in player.cards:
        print(f"  - {card['name']} ({card['points']} pts, {card['type']})")

#for player in players:
 #   print(f"{player.name} ได้การ์ด:")
  #  for card in player.cards:
        # ตรวจว่าเป็น wild-white หรือไม่
   #     if card["type"] == "wild-white":
            #chosen_type = random.choice(card["possible_types"])  # หรือกำหนดเองก็ได้
            #print(f"  - {card['name']} ({card['points']} pts, ใช้เป็น: {chosen_type})")
    #        print(' not random la ja')
     #   else:
      #      print(f"  - {card['name']} ({card['points']} pts, {card['type']})")


def draw_wild_white_selector(screen, font, card, on_select):
    screen.fill((0, 0, 0))  # เคลียร์หน้าจอ
    text = font.render(f"เลือกชนิดให้การ์ด {card['name']} (+{card['points']} pts)", True, (255, 255, 255))
    screen.blit(text, (100, 100))

    button_width = 200
    button_height = 50
    spacing = 20
    x = 100
    y = 200

    buttons = []

    for card_type in card["possible_types"]:
        rect = pygame.Rect(x, y, button_width, button_height)
        buttons.append((rect, card_type))
        pygame.draw.rect(screen, (200, 200, 200), rect)
        label = font.render(card_type.upper(), True, (0, 0, 0))
        screen.blit(label, (x + 10, y + 10))
        y += button_height + spacing

    pygame.display.flip()

    selecting = True
    while selecting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for rect, card_type in buttons:
                    if rect.collidepoint(mx, my):
                        #card["selected_type"] = card_type
                        card["chosen_type"] = card_type  # 👈 เพิ่มบรรทัดนี้จ๊ะ!
                        on_select(card_type)
                        selecting = False

special_tiles = {
    "white_red": [74, 76, 83, 85, 56, 60, 61, 64, 65, 69, 89, 92, 95, 98, 101, 104, 107, 109, 111, 112, 114, 116  ],  # ช่องขาวขอบแดง
}

choosing_wild_white_type = False
wild_white_card_to_assign = None  # เก็บการ์ดที่จะเลือกชนิด
selecting_wild_white = False

running = True

# Main game loop
while running:
    screen.fill((30, 30, 30))  # พื้นหลังมืด ๆ

    # แสดงข้อมูลสถานะผู้เล่นและเฟส
    info_text = small_font.render(
        f"{turn_manager.current_player.name}'s turn - Phase: {turn_manager.current_phase}", True, (255, 255, 255)
    )
    screen.blit(info_text, (10, 10))

    # แสดงแต้มที่ทอยได้ (ถ้ามี)
    if turn_manager.dice_value is not None:
        dice_text = small_font.render(f"Dice: {turn_manager.dice_value}", True, (255, 255, 255))
        text_rect = dice_text.get_rect(topright=(screen.get_width() - 10, 10))  # ระยะห่าง 10px จากขอบขวาและขอบบน
        screen.blit(dice_text, text_rect)

    draw_board(screen, row_lengths, tile_colors, players, turn_manager.current_player, special_tiles)

    draw_player_cards(screen, small_font, players, players.index(turn_manager.current_player))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and turn_manager.current_phase == "roll":
                turn_manager.dice_value = random.randint(1, 6)
                turn_manager.next_phase()

            elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6] and turn_manager.current_phase == "roll":
                turn_manager.dice_value = int(event.unicode)
                turn_manager.next_phase()

            elif turn_manager.current_phase == "move":
                turn_manager.current_player.move(turn_manager.dice_value, row_lengths, screen, tile_colors, players, special_tiles)
                turn_manager.next_phase()

            elif turn_manager.current_phase == "check":
                current_pos = turn_manager.current_player.position
                current_tile_color = tile_colors.get(current_pos, (139, 69, 19))

                # ถ้ายังไม่ได้เลือกชนิดให้ wild-white → ไปเลือกก่อน
                for card in turn_manager.current_player.cards:
                    if card["type"] == "wild-white" and "chosen_type" not in card:
                        choosing_wild_white_type = True
                        wild_white_card_to_assign = card
                        selecting_wild_white = True  # บอกว่าเราจะเข้าโหมดเลือก
                        break

                if selecting_wild_white:
                    draw_wild_white_selector(screen, font, wild_white_card_to_assign, lambda _: None)
                    selecting_wild_white = False  # เลือกเสร็จแล้ว
                    break  # รอ frame หน้า

                new_position, should_reverse, event_type_1 = board_events.check_event(
                    current_pos,
                    turn_manager.current_player.cards,
                    current_tile_color
                )
                # บันทึก event แรก
                turn_manager.last_event_type_1 = event_type_1
                turn_manager.last_event_type_2 = None  # เผื่อว่าไม่มีเหตุการณ์รอบสอง

                if new_position != current_pos:
                    turn_manager.current_player.move_to_position(
                        new_position, row_lengths, screen, tile_colors, players, special_tiles
                    )
                    if should_reverse:
                        turn_manager.reverse_order()
                        print("🔁 ลำดับผู้เล่นถูกสลับแล้ว!")

                    # 🔁 Check ครั้งที่สองทันทีหลังจากโดนย้าย
                    second_pos = new_position
                    second_tile_color = tile_colors.get(second_pos, (139, 69, 19))

                    second_new_position, second_should_reverse, event_type_2 = board_events.check_event(
                        second_pos,
                        turn_manager.current_player.cards,
                        second_tile_color
                    )

                    if second_new_position != second_pos:
                        turn_manager.current_player.move_to_position(
                            second_new_position, row_lengths, screen, tile_colors, players, special_tiles
                        )
                        if second_should_reverse:
                            turn_manager.reverse_order()
                            print("🔁 ลำดับผู้เล่นถูกสลับอีกครั้ง!")
                            # บันทึก event ที่สอง
                        turn_manager.last_event_type_2 = event_type_2
                    else:
                        turn_manager.last_event_type_2 = None  # ❌ ไม่มีการย้าย ไม่ถือว่าเกิด event
                turn_manager.next_phase()

            elif turn_manager.current_phase == "draw":
                e1 = turn_manager.last_event_type_1
                e2 = turn_manager.last_event_type_2
                print(f"📦 เช็กผล event ทั้งสองรอบ: {e1}, {e2}")

                if e1 == "ladder" and e2 == "ladder":
                    pile = "white"
                elif e1 == "snake" and e2 == "snake":
                    pile = "dark"
                elif (e1 == "ladder" and e2 == "snake") or (e1 == "snake" and e2 == "ladder"):
                    pile = "mixed"
                elif e1 == "ladder" and e2 is None:
                    pile = "white"
                elif e1 == "snake" and e2 is None:
                    pile = "dark"
                else:
                    pile = "mixed"  # กรณี fallback เผื่อไว้

                print(f"📦 หยิบการ์ดจากกอง {pile}")
                new_card = card_manager.draw_card_from_pile(pile)
                turn_manager.current_player.cards.append(new_card)
                print(f"{turn_manager.current_player.name} จั่วการ์ด: {new_card['name']}")
                turn_manager.next_phase()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            #print( ' lock mai',turn_manager.current_phase, turn_manager.locked)
            if turn_manager.current_phase == "send" and  turn_manager.locked:
                #print(' in not turn_manager.locked')
                mouse_pos = pygame.mouse.get_pos()
                card_rects = draw_player_cards(screen, small_font, players, players.index(turn_manager.current_player))

                for card_rect, card_index in card_rects:
                    if card_rect.collidepoint(mouse_pos):
                        sender = turn_manager.current_player
                        receiver = players[(players.index(sender) + 1) % len(players)]

                        if card_index < len(sender.cards):  # ป้องกัน index error
                            selected_card = sender.cards.pop(card_index)
                            receiver.cards.append(selected_card)
                            print(f"{sender.name} ส่งการ์ด '{selected_card['name']}' ให้ {receiver.name}")

                            # ตรวจสอบว่าอยู่บนช่องขาวขอบแดงไหม
                            white_red_tiles = special_tiles.get("white_red", [])
                            if sender.tile in white_red_tiles and sender.cards_sent_this_turn == 0:
                                # ถ้ายังไม่ได้เลือกจำนวนการ์ดจะส่งเลยในเทิร์นนี้ → แสดง popup ก่อน
                                choice = show_choice_popup(screen, screen_width, screen_height)
                                sender.cards_to_send_this_turn = choice  # เก็บว่าเลือกส่งกี่ใบ
                                sender.cards_sent_this_turn = 1  # ส่งใบแรกไปแล้ว
                            else:
                                sender.cards_sent_this_turn += 1

                            if sender.cards_sent_this_turn >= getattr(sender, 'cards_to_send_this_turn', 1):
                                # ถ้าส่งครบแล้ว → reset แล้วเปลี่ยนเฟส
                                sender.cards_sent_this_turn = 0
                                sender.cards_to_send_this_turn = 0
                                turn_manager.locked = False
                                turn_manager.next_phase()
                            else:
                                print(
                                    f"{sender.name} ยังสามารถส่งได้อีก {sender.cards_to_send_this_turn - sender.cards_sent_this_turn} ใบ")

    clock.tick(60)

pygame.quit()
