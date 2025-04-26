from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os

EMOJIS = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"]

def generate_thumbnail(subs):
    subs = int(subs)

    # Setup background and message based on range
    if subs < 10:
        bg_color = (40, 40, 40)  # Grey background
        main_text = f"{subs} SUBS!"
        extra_text = "JUST STARTING! 🚀"
        emoji_count = 1

    elif subs < 100:
        bg_color = (40, 40, 40)  # Purple background
        main_text = f"{subs} SUBS!"
        extra_text = "TINY BUT MIGHTY 💥"
        emoji_count = 3

    elif subs < 1000:
        bg_color = (0, 102, 204)  # Blue background
        main_text = f"{subs} SUBS!"
        extra_text = "GROWTH MODE ON! 📈"
        emoji_count = 4

    elif subs < 10000:
        bg_color = (255, 215, 0)  # Gold background
        main_text = f"{subs} SUBS!"
        extra_text = "INSANE LEVEL 🚀🔥"
        emoji_count = 5

    else:
        bg_color = (255, 0, 0)  # Red alert background for crazy subs
        main_text = f"{subs} SUBS!"
        extra_text = "LEGENDARY STATUS 💀🔥"
        emoji_count = 6

    # Create background
    img = Image.new("RGB", (1280, 720), color=bg_color)
    img = img.filter(ImageFilter.GaussianBlur(6))  # Light blur
    draw = ImageDraw.Draw(img)

    font_big = ImageFont.truetype("luckiest-guy.ttf", 160)
    font_small = ImageFont.truetype("luckiest-guy.ttf", 90)

    # Draw text with GLOW
    def draw_text_with_glow(draw, position, text, font, glow_color, text_color):
        x, y = position
        # Draw multiple shadows around the text
        for offset in range(-3, 4):
            for offset2 in range(-3, 4):
                draw.text((x + offset, y + offset2), text, font=font, fill=glow_color)
        draw.text((x, y), text, font=font, fill=text_color)

    w1, h1 = draw.textbbox((0, 0), main_text, font=font_big)[2:]
    w2, h2 = draw.textbbox((0, 0), extra_text, font=font_small)[2:]

    total_height = h1 + 40 + h2
    y1 = (720 - total_height) // 2
    y2 = y1 + h1 + 40

    x1 = (1280 - w1) // 2
    x2 = (1280 - w2) // 2

    # Glow colors
    glow_color_main = (0, 0, 0)  # Black shadow glow
    glow_color_sub = (0, 0, 0)

    # Main and subtext with glow
    draw_text_with_glow(draw, (x1, y1), main_text, font_big, glow_color_main, "white")
    draw_text_with_glow(draw, (x2, y2), extra_text, font_small, glow_color_sub, "white")

    # Safe zone around text
    safe_zone = (300, 200, 980, 520)

    # Add emojis randomly without covering text
    for _ in range(emoji_count):
        emoji_name = random.choice(EMOJIS)
        emoji_path = os.path.join("emojis", f"{emoji_name}.png")
        if os.path.exists(emoji_path):
            emoji_img = Image.open(emoji_path).convert("RGBA")
            emoji_img = emoji_img.resize((120, 120))

            for _ in range(30):  # Try random positions
                rand_x = random.randint(0, 1280 - 120)
                rand_y = random.randint(0, 720 - 120)

                if not (safe_zone[0] < rand_x < safe_zone[2] - 120 and safe_zone[1] < rand_y < safe_zone[3] - 120):
                    img.paste(emoji_img, (rand_x, rand_y), emoji_img)
                    break

    img.save("thumbnail.jpg")
