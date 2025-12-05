import numpy as np
from hs_sdk.models import CardSearchResponse
from hs_sdk.client import HearthstoneClient
client = HearthstoneClient(client_id="",
                           client_secret="",
                           region='us')
keyword = input("请输入搜索关键词: ")
print(f"🔥 正在搜索: {keyword} ...")

cards = client.search_cards(keyword)

for card in cards:
        print("-" * 30)
        print(f"【{card.name}】(费用: {card.manaCost})")
        print(f"描述: {card.text}")
        print(f"稀有度: {card.rarityId}")
        print(f"随从类型: {card.minionType}")
        print(f"攻击: {card.attack} / 血量: {card.health}")
        print(f"图片: {card.image}")

print(cards)

