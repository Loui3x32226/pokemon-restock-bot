import requests
import time
import json
import os

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1465569760975650931/4oJtsPB0x2tgMOG_UrHclEGhYrzfoG6cGRBAjYX8Unfnau40_2JHusPzK6GBA74mO7om"

CHECK_INTERVAL = 180  # 3 minutes

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

PRODUCTS = {
    "Ascended Heroes Pokemon Center Elite": "https://www.pokemoncenter.com/product/10-10315-108/pokemon-tcg-mega-evolution-ascended-heroes-pokemon-center-elite-trainer-box",
    "Mega Evolution Booster Bundle": "https://www.pokemoncenter.com/product/10-10377-109/pokemon-tcg-mega-evolution-perfect-order-booster-bundle-6-packs",
    "Phantasmal Flames Pokemon Center Elite": "https://www.pokemoncenter.com/product/10-10186-109/pokemon-tcg-mega-evolution-phantasmal-flames-pokemon-center-elite-trainer-box",
    "Scarlet & Violet 151 Elite Trainer Box": "https://www.pokemoncenter.com/product/290-85466/pokemon-tcg-scarlet-and-violet-151-pokemon-center-elite-trainer-box",
    "Paradox Rift Elite Trainer Box": "https://www.pokemoncenter.com/product/187-85417/pokemon-tcg-scarlet-and-violet-paradox-rift-pokemon-center-elite-trainer-box-roaring-moon",
    "Paldean Fates Elite Trainer Box": "https://www.pokemoncenter.com/product/290-85619/pokemon-tcg-scarlet-and-violet-paldean-fates-pokemon-center-elite-trainer-box",
    "Prismatic Evolutions Elite Trainer Box": "https://www.pokemoncenter.com/product/BUNDLE1098/prismatic-evolutions-pokemon-center-elite-trainer-box-espeon-pin-and-playmat-bundle",
    "Fusion Strike Elite Trainer Box": "https://www.pokemoncenter.com/product/179-80994/pokemon-tcg-sword-and-shield-fusion-strike-pokemon-center-elite-trainer-box",
    "Brilliant Stars Elite Trainer Box": "https://www.pokemoncenter.com/product/180-85006/pokemon-tcg-sword-and-shield-brilliant-stars-pokemon-center-elite-trainer-box",
    "Mega Evolution-Booster Box": "https://www.pokemoncenter.com/product/10-10380-119/pokemon-tcg-mega-evolution-perfect-order-booster-display-box-36-packs",
    "Scarlet & Violet 151": "https://www.pokemoncenter.com/product/699-85322/pokemon-tcg-scarlet-and-violet-151-booster-bundle",
    "Mega Evolution - Ascneded Heroes Booster bundle 6 Packs": "https://www.pokemoncenter.com/product/10-10311-114/pokemon-tcg-mega-evolution-ascended-heroes-booster-bundle-6-packs",
    "Scarlet & Violet-Obsidian Flames Pokémon Center Elite Trainer Box": "https://www.pokemoncenter.com/product/186-85392/pokemon-tcg-scarlet-and-violet-obsidian-flames-pokemon-center-elite-trainer-box",
    "Scarlet & Violet-Obsidian Flames Booster Display Box": "https://www.pokemoncenter.com/product/699-86374/pokemon-tcg-scarlet-and-violet-obsidian-flames-booster-display-box-36-packs",
    "Scarlet & Violet-Obsidian Flames Booster Bundle (6 Packs)": "https://www.pokemoncenter.com/product/186-85387/pokemon-tcg-scarlet-and-violet-obsidian-flames-booster-bundle-6-packs",
    "Scarlet & Violet-Obsidian Flames 3 Booster Packs & Eevee Promo Card": "https://www.pokemoncenter.com/product/699-85380/pokemon-tcg-scarlet-and-violet-obsidian-flames-3-booster-packs-and-eevee-promo-card",

}

STATUS_FILE = "stock_status.json"


def send_discord(message):
    requests.post(DISCORD_WEBHOOK, json={"content": message})


# 🔹 Load previous stock state from disk
if os.path.exists(STATUS_FILE):
    with open(STATUS_FILE, "r") as f:
        last_status = json.load(f)
else:
    last_status = {}


send_discord("🤖 Pokémon Center bot running (clean stop-drop enabled).")


while True:
    print("Bot alive - checking stock...")
    updated = False

    for product_name, url in PRODUCTS.items():
try:
    response = requests.get(url, headers=HEADERS, timeout=15)
    text = response.text.lower()

    if "out of stock" in text or "sold out" in text:
        current_status = "OUT_OF_STOCK"
    else:
        current_status = "IN_STOCK"

except requests.exceptions.Timeout:
    print(f"Timeout checking {product_name}, will retry next loop.")
    continue

except Exception as e:
    print(f"Error checking {product_name}: {e}")
    continue


            previous_status = last_status.get(product_name)

            # 🔔 Only alert on OUT → IN
            if previous_status == "OUT_OF_STOCK" and current_status == "IN_STOCK":
                send_discord(
                    "🚨 **RESTOCK ALERT!** 🚨\n"
                    f"🛒 **{product_name}**\n"
                    f"{url}"
                )

            if previous_status != current_status:
                last_status[product_name] = current_status
                updated = True

        except Exception as e:
            send_discord(f"⚠️ Error checking {product_name}: {e}")

    # 💾 Save state only if something changed
    if updated:
        with open(STATUS_FILE, "w") as f:
            json.dump(last_status, f, indent=2)

    time.sleep(CHECK_INTERVAL)






