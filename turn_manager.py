import pygame

class TurnManager:
    def __init__(self, players):
        self.players = players
        self.current_index = 0
        self.phases = ["roll", "move", "check", "draw", "send"]
        self.current_phase_index = 0
        self.dice_value = None
        self.locked = False  # ใช้ล็อกระหว่างรอ input ผู้เล่น
        #self.last_event_type = None  # เก็บประเภทเหตุการณ์ล่าสุด
        self.last_event_type_1 = None
        self.last_event_type_2 = None

    @property
    def current_player(self):
        return self.players[self.current_index]

    @property
    def next_player(self):
        return self.players[(self.current_index + 1) % len(self.players)]

    @property
    def current_phase(self):
        return self.phases[self.current_phase_index]

    def clear_wild_white_choices(self):
        for card in self.current_player.cards:
            if card["type"] == "wild-white":
                card.pop("chosen_type", None)

    def next_phase(self):
        if self.locked:
            return  # ยังไม่ให้เปลี่ยนเฟส ถ้ายังไม่ได้คลิกส่งการ์ด

        next_index = self.current_phase_index + 1
        if next_index >= len(self.phases):
            self.end_turn()
            return

        # ✅ ยังอยู่ในลำดับ phase ที่ถูกต้อง
        self.current_phase_index = next_index

        if self.current_phase == "check":
            self.clear_wild_white_choices()  # 👈 สำหรับเลือก wild-white ใหม่ทุกครั้ง

        # ✅ ล็อกเฟส "send"
        if self.current_phase == "send":
            self.locked = True

    def end_turn(self):
        self.current_phase_index = 0
        self.current_index = (self.current_index + 1) % len(self.players)
        self.dice_value = None
        self.locked = False

        # ✅ รีเซ็ตตัวนับการ์ดที่ส่งในเทิร์น
        self.current_player.cards_sent_this_turn = 0

    def reset(self):
        self.current_index = 0
        self.current_phase_index = 0
        self.dice_value = None
        self.locked = False

    def set_card_manager(self, card_manager):
        self.card_manager = card_manager

    def phase_draw(self):
        if not hasattr(self, 'card_manager'):
            print("❗ ยังไม่ได้เชื่อมต่อ CardManager เข้ากับ TurnManager")
            return

        current_player = self.current_player
        new_card = self.card_manager.draw_card()
        if new_card:
            current_player.cards.append(new_card)
            print(f"{current_player.name} หยิบการ์ดใหม่: {new_card['name']} ({new_card['points']} pts, {new_card['type']})")
        else:
            print("❗ ไม่มีการ์ดเหลือให้หยิบแล้ว")

    def reverse_order(self):
        self.players.reverse()
        self.current_index = len(self.players) - 1 - self.current_index

