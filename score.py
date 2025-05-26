import random
def calculate_score(cards):
    score = 0
    for card in cards:
        if card["type"] == "wild-white":
            chosen_type = card.get("chosen_type")
            if chosen_type in ["red-white", "orange-white", "green-white"]:
                score += card["points"]
        elif card["type"] in ["red-white", "orange-white", "green-white"]:
            score += card["points"]
        elif card["type"] in ["red-dark", "orange-dark", "green-dark"]:
            score += card["points"]  # การ์ดลบอยู่แล้ว
    return score

def calculate_score_details(cards):
    score_summary = {
        "red-white": 0,
        "orange-white": 0,
        "green-white": 0,
        "red-dark": 0,
        "orange-dark": 0,
        "green-dark": 0,
    }

    for card in cards:
        card_type = card["type"]

        if card_type == "wild-white":
            chosen_type = card.get("chosen_type")
            if chosen_type and chosen_type in score_summary:
                score_summary[chosen_type] += card["points"]
                print(f"[+] เพิ่มแต้ม {card['points']} ให้ {chosen_type}")
            else:
                print(f"❗ wild-white ยังไม่มี chosen_type หรือไม่ถูกต้อง: {chosen_type}")
        elif card_type in score_summary:
            score_summary[card_type] += card["points"]
        else:
            print(f"❗ พบการ์ดที่ไม่รู้จัก type: {card_type}")
            #print (chosen_type)

    # รวมคะแนนกลุ่ม white และ dark
    white_total = (
        score_summary["red-white"]
        + score_summary["orange-white"]
        + score_summary["green-white"]
    )
    dark_total = (
        score_summary["red-dark"]
        + score_summary["orange-dark"]
        + score_summary["green-dark"]
    )

    return score_summary, white_total, dark_total

def draw_score_summary(screen, font, score_summary, white_total, dark_total):
    x = 1200
    y = 120
    line_height = 25

    # White cards
    screen.blit(font.render("White Cards:", True, (255, 255, 255)), (x, y))
    y += line_height
    screen.blit(font.render(f"  Red:    {score_summary['red-white']} pts", True, (255, 100, 100)), (x, y))
    y += line_height
    screen.blit(font.render(f"  Orange: {score_summary['orange-white']} pts", True, (255, 165, 0)), (x, y))
    y += line_height
    screen.blit(font.render(f"  Green:  {score_summary['green-white']} pts", True, (100, 255, 100)), (x, y))
    y += line_height
    screen.blit(font.render(f"  Total White: {white_total} pts", True, (255, 255, 255)), (x, y))
    y += line_height * 2

    # Dark cards
    screen.blit(font.render("Dark Cards:", True, (255, 255, 255)), (x, y))
    y += line_height
    screen.blit(font.render(f"  Red:    {score_summary['red-dark']} pts", True, (139, 0, 0)), (x, y))
    y += line_height
    screen.blit(font.render(f"  Orange: {score_summary['orange-dark']} pts", True, (255, 140, 0)), (x, y))
    y += line_height
    screen.blit(font.render(f"  Green:  {score_summary['green-dark']} pts", True, (0, 100, 0)), (x, y))
    y += line_height
    screen.blit(font.render(f"  Total Dark: {dark_total} pts", True, (255, 255, 255)), (x, y))
