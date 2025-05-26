# snakes_and_ladders.py
from score import calculate_score_details

class BoardEvents:
    def __init__(self):
        self.ladders = {
            # mid 18
            74: 57, 76: 59, 79: 62, 80: 63, 83: 66, 85: 68,
            # uMid 16
            56: 41, 60: 45, 61: 46, 64: 49, 65: 50, 69: 54,
            # dMid 16
            89: 72, 92: 75, 95: 78, 98: 81, 101: 84, 104: 87,
            # uMid 14
            42: 29, 44: 31, 46: 33, 49: 36, 51: 38, 53: 40,
            # dMid 14
            107: 92, 109: 94, 111: 96, 112: 97, 114: 99, 116: 101,
        }

        self.conditional_snakes = {
            #upmid
            57: ("orange",74),
            58: ("green",75),
            62: ("red", 79),
            63: ("red", 80),
            #mid
            72: ("green", 89),
            73: ("red", 90),
            75: ("orange", 92),
            #77: ("orange", 94),
            78: ("orange", 95),
            81: ("green", 98),
            82: ("green", 99),
            86: ("red", 90),
            87: ("red", 90),

            #downmid
            90: ("green", 105),
        }
        self.reverse_tiles = [55, 71, 88, 105, 118]  # ตำแหน่งที่ตกแล้วจะสลับลำดับ

        self.color_map = {
            "red": (139, 0, 0),
            "orange": (255, 140, 0),
            "green": (0, 100, 0),
        }

    def check_event(self, position, player_cards, tile_color):
        """
        คืนค่าตำแหน่งใหม่หลังตรวจบันไดและงูตามเงื่อนไข
        """
        score_summary, white_total, dark_total = calculate_score_details(player_cards)
        total_score = white_total + dark_total

        # 🪜 เช็คบันได: ต้องมีคะแนนรวม > 0
        if position in self.ladders and total_score > 0:
            return self.ladders[position], False, "ladder"

        # 🐍 เช็คงูแบบมีเงื่อนไขสี
        if position in self.conditional_snakes:
            required_color_name, fall_to = self.conditional_snakes[position]
            required_color = self.color_map[required_color_name]

            if tile_color == required_color : # กรณีต้องการให้ ดู สกอรวมด้วย and total_score <= 0:
                # คำนวณคะแนนรวมของสีที่ตกช่อง
                if required_color_name == "red":
                    red_score = score_summary["red-white"] + score_summary["red-dark"]
                    if red_score < 0:
                        return fall_to, False, "snake"

                elif required_color_name == "orange":
                    orange_score = score_summary["orange-white"] + score_summary["orange-dark"]
                    if orange_score < 0:
                        return fall_to, False, "snake"

                elif required_color_name == "green":
                    green_score = score_summary["green-white"] + score_summary["green-dark"]
                    if green_score < 0:
                        return fall_to, False, "snake"

        # --- สลับลำดับผู้เล่น ---
        if position in self.reverse_tiles:
            return position, True, "mixed"

        return position, False, "mixed" # ไม่มีอะไรเกิดขึ้น

