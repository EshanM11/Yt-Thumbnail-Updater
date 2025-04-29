from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os

EMOJIS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18"]

def generate_thumbnail(subs):
    subs = int(subs)

    # Setup background and message based on range
    if subs < 10:
        bg_color = (40, 40, 40)
        extra_text = ":/"
        emoji_count = 1

    elif subs < 100:
        bg_color = (128, 0, 128)
        extra_text = "its alive guys"
        emoji_count = 3

    elif subs < 1000:
        bg_color = (0, 102, 204)
        extra_text = "lol"
        emoji_count = 4

    elif subs < 10000:
        bg_color = (192, 192, 192)
        extra_text = "OMG! I'm Famouss!"
        emoji_count = 5

    elif subs < 100000:
        bg_color = (255, 0, 0)
        extra_text = "SIUUUUUUUU"
        emoji_count = 6
    else:
        bg_color = (255, 215, 0)
        extra_text = "Thank you soo much :)"
        emoji_count = 6

    # Create background
    img = Image.new("RGB", (1280, 720), color=bg_color)
    img = img.filter(ImageFilter.GaussianBlur(6))  # Light blur
    draw = ImageDraw.Draw(img)

    font_big = ImageFont.truetype("luckiest-guy.ttf", 160)
    font_small = ImageFont.truetype("luckiest-guy.ttf", 90)

    # Main text (show only the number if subs >= 100,000)
    if subs >= 100000:
        main_text = f"{subs}"
    else:
        main_text = f"{subs} SUBS!"

    # Draw text with glow
    def draw_text_with_glow(draw, position, text, font, glow_color, text_color):
        x, y = position
        for offset_x in range(-3, 4):
            for offset_y in range(-3, 4):
                draw.text((x + offset_x, y + offset_y), text, font=font, fill=glow_color)
        draw.text((x, y), text, font=font, fill=text_color)

    # Calculate text position
    w1, h1 = draw.textbbox((0, 0), main_text, font=font_big)[2:]
    w2, h2 = draw.textbbox((0, 0), extra_text, font=font_small)[2:]

    total_height = h1 + 40 + h2
    y1 = (720 - total_height) // 2
    y2 = y1 + h1 + 40

    x1 = (1280 - w1) // 2
    x2 = (1280 - w2) // 2

    # Glow colors
    glow_color_main = (0, 0, 0)
    glow_color_sub = (0, 0, 0)

    # Draw main and subtext
    draw_text_with_glow(draw, (x1, y1), main_text, font_big, glow_color_main, "white")
    draw_text_with_glow(draw, (x2, y2), extra_text, font_small, glow_color_sub, "white")

    # Define safe zone around the texts
    safe_zone = (x1 - 50, y1 - 50, x1 + w1 + 50, y2 + h2 + 50)  # Little padding

    # Store placed emoji positions to avoid overlap
    emoji_positions = []

    def is_overlapping_with_text_or_other_emoji(x, y):
        # Check if it overlaps with the safe zone (text area)
        if safe_zone[0] < x < safe_zone[2] and safe_zone[1] < y < safe_zone[3]:
            return True
        # Check if it overlaps with another emoji
        for (ex, ey) in emoji_positions:
            if abs(ex - x) < 120 and abs(ey - y) < 120:
                return True
        return False

    # Add emojis
    for _ in range(emoji_count):
        emoji_name = random.choice(EMOJIS)
        emoji_path = os.path.join("emojis", f"{emoji_name}.png")
        if os.path.exists(emoji_path):
            emoji_img = Image.open(emoji_path).convert("RGBA")
            emoji_img = emoji_img.resize((120, 120))

            # Try placing emoji
            placed = False
            for _ in range(50):  # Try 50 random positions
                rand_x = random.randint(0, 1280 - 120)
                rand_y = random.randint(0, 720 - 120)

                # Check if the position is free (doesn't overlap with text or other emojis)
                if not is_overlapping_with_text_or_other_emoji(rand_x, rand_y):
                    img.paste(emoji_img, (rand_x, rand_y), emoji_img)
                    emoji_positions.append((rand_x, rand_y))
                    placed = True
                    break

            if not placed:
                print(f"Could not place emoji {emoji_name} due to overlap")

    img.save("thumbnail.jpg")
