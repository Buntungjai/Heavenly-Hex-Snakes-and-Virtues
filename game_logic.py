# game_logic.py
'''
import random

reverse_order_tiles = [74, 75, 76]

conditional_snakes = []
ladders = []

white_card_pool = [{"name": "บันได"}, {"name": "ได้แต้ม"}]
dark_card_pool = [{"name": "งู"}, {"name": "เสียแต้ม"}]
mixed_card_pool = [{"name": "สุ่ม"}]

def roll_dice():
    return random.randint(1, 6)

def update_position_path(position, dice_value, direction):
    # ใช้ระบบของอัปดุลเดิมในการสร้าง path
    path = []
    for _ in range(dice_value):
        position += direction
        path.append(position)
    return path, direction

def handle_tile_effect(player, position):
    pass  # ใส่ logic งู/บันไดตามที่ทำไว้แล้ว

def draw_card_for_tile(position):
    if position in ladders:
        return random.choice(white_card_pool)
    elif position in conditional_snakes:
        return random.choice(dark_card_pool)
    return random.choice(mixed_card_pool)

def calculate_score(cards):
    score = 0
    for card in cards:
        score += card.get("point", 0)
    return score

def check_special_tile_effects(player_name, players, player_order):
    player_index = player_name_to_index[player_name]
    current_position = players[player_index]["position"]
    if current_position in reverse_order_tiles:
        print(f"{player_name} ตกช่องพิเศษ! ลำดับการเล่นย้อนกลับ!")
        player_order.reverse()
        print(f"ลำดับใหม่: {player_order}")
        return player_order, 0  # reset index after reverse
    return player_order, player_order.index(player_name)
'''