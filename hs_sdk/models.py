from pydantic import BaseModel, Field
from typing import Optional, List

class Card(BaseModel):
    id: int
    name: str
    set: str = Field(default="") #来源
    class_: str = Field(default="", alias="class") #类型
    text: str = ""  # 卡牌描述（有的卡没描述，给个默认值）
    manaCost: int = Field(alias="manaCost", default=0) # 费用
    attack: int = Field(default=0)
    health: int = Field(default=0)
    type: str = Field(default="")
    minionType: str = Field(default="")
    rarityId: int = Field(alias="rarityId", default=1)
    cardTypeId: int = Field(alias="cardTypeId")
    image: Optional[str] = None # 卡牌图片的URL

class CardSearchResponse(BaseModel):
    cards: List[Card]
    cardCount: int
    pageCount: int