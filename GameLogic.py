class GameLogic:
    def __init__(self):
        self.ladders = {
            74: 57, 76: 59, 79: 62, 80: 63, 83: 66, 85: 68,
            56: 41, 60: 45, 61: 46, 64: 49, 65: 50, 69: 54,
            89: 72, 92: 75, 95: 78, 98: 81, 101: 84, 104: 87,
            42: 29, 44: 31, 46: 33, 49: 36, 51: 38, 53: 40,
            107: 92, 109: 94, 111: 96, 112: 97, 114: 99, 116: 101
        }

        self.conditional_snakes = {
            72: ("red", 89), 73: ("red", 90),
            75: ("orange", 92), 77: ("orange", 94), 78: ("orange", 95),
            81: ("green", 98), 82: ("green", 99), 90: ("green", 105)
        }

        self.color_map = {
            "red": (139, 0, 0),
            "orange": (255, 140, 0),
            "green": (0, 100, 0),
        }

    def check_event(self, position, player_score, tile_color):
        if position in self.ladders and player_score > 0:
            return self.ladders[position]

        if position in self.conditional_snakes:
            required_color_name, fall_to = self.conditional_snakes[position]
            required_color = self.color_map[required_color_name]

            if tile_color == required_color:
                return fall_to

        return position
