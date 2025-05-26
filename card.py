import random

special_card = {
    "name": "Special Dark Orange",
    "points": -5,
    "type": "orange-dark"
}
bonus_card = {
    "name": "Bonus Wild White",
    "points": +3,
    "type": "wild-white",
    "possible_types": ["red-white", "orange-white", "green-white"]
}

class CardManager:
    def __init__(self):
        self.white_types = ["red-white", "orange-white", "green-white"]
        self.dark_types = ["red-dark", "orange-dark", "green-dark"]
        self.all_types = self.white_types + self.dark_types
        self.white_pile = []
        self.dark_pile = []
        self.mixed_pile = []
        self._initialize_piles()

    def _initialize_piles(self):
        full_pool = self._create_full_card_pool()

        self.white_pile = [card for card in full_pool if card["from"] == "white"]
        self.dark_pile = [card for card in full_pool if card["from"] == "dark"]
        self.mixed_pile = [card for card in full_pool if card["from"] == "mixed"]

        random.shuffle(self.white_pile)
        random.shuffle(self.dark_pile)
        random.shuffle(self.mixed_pile)

    def _create_full_card_pool(self):
        card_pool = []

        # White cards
        for i in range(1, 34):
            card_pool.append({
                "name": f"White Card {i}",
                "points": random.randint(1, 5),
                "type": random.choice(self.white_types),
                "from": "white"
            })

        # Dark cards
        for i in range(1, 38):
            card_pool.append({
                "name": f"Dark Card {i}",
                "points": -random.randint(1, 5),
                "type": random.choice(self.dark_types),
                "from": "dark"
            })

        # Mixed cards
        counter = 1
        for card_type in self.all_types:
            for _ in range(10):
                is_dark = "dark" in card_type
                points = -random.randint(1, 5) if is_dark else random.randint(1, 5)
                card_pool.append({
                    "name": f"Mixed Card {counter}",
                    "points": points,
                    "type": card_type,
                    "from": "mixed"
                })
                counter += 1

        random.shuffle(card_pool)
        return card_pool

    def deal_initial_cards(self, players):
        # ดึงการ์ดจาก mixed pile
        for i, player in enumerate(players):
            for _ in range(2):
                card = self.draw_card_from_pile("mixed")
                player.cards.append(card)

            if i == 0:
                # ผู้เล่นคนแรกได้การ์ดพิเศษ
                player.cards.append(special_card)
                print(f"{player.name} ได้รับการ์ดพิเศษ: {special_card['name']}")
            elif i == 1:
                # ผู้เล่นคนที่สองได้การ์ด wild white
                player.cards.append(bonus_card)
                print(f"{player.name} ได้รับการ์ดพิเศษ: {bonus_card['name']}")

    def pass_card_to_next_player(self, current_index, players, card_index):
        current_player = players[current_index]
        next_player = players[(current_index + 1) % len(players)]

        if 0 <= card_index < len(current_player.cards):
            card = current_player.cards.pop(card_index)
            next_player.cards.append(card)
           # print(f"ส่งการ์ด {card['name']} จาก {current_player.name} ไปให้ {next_player.name}")

    def draw_card_from_pile(self, pile_name):
        if pile_name == "white":
            if not self.white_pile:
                print("กอง white cards หมดแล้ว สร้างกองใหม่...")
                self._initialize_piles()  # สร้างกองใหม่ทั้ง 3 กองใหม่
            return self.white_pile.pop()

        elif pile_name == "dark":
            if not self.dark_pile:
                print("กอง dark cards หมดแล้ว สร้างกองใหม่...")
                self._initialize_piles()
            return self.dark_pile.pop()

        elif pile_name == "mixed":
            if not self.mixed_pile:
                print("กอง mixed cards หมดแล้ว สร้างกองใหม่...")
                self._initialize_piles()
            return self.mixed_pile.pop()

        else:
            raise ValueError(f"ไม่รู้จักกองการ์ด: {pile_name}")

   # def draw_card(self):
      #  if not self.card_pool:
       #     print("ไพ่หมดแล้ว สร้างใหม่...")
       #     self.card_pool = self._create_full_card_pool()
#
     #   return self.card_pool.pop(random.randint(0, len(self.card_pool) - 1))
#
