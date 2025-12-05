import requests
from dataclasses import dataclass
from .models import Card, CardSearchResponse
import json


class BlizzardAuthError(Exception): 
    pass

class HearthstoneClient:
    def __init__(self, client_id: str, client_secret:str, region: 'us'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.region = region
        self.access_token = None 

        # 暴雪认证地址
        self.auth_url = "https://oauth.battle.net/token"
        self.api_url = f"https://{region}.api.blizzard.com/hearthstone"

    def _authenticate(self):
        print("🔄 正在向暴雪申请访问令牌...")

        response = requests.post(
            self.auth_url,
            data={
                "grant_type": "client_credentials"
            },
            auth=(self.client_id, self.client_secret)
        )

        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data['access_token']
            print(f"✅ 拿到令牌了！有效期: {token_data['expires_in']} 秒")
        
        else:
            raise BlizzardAuthError(f"认证失败: {response.status_code} {response.text}")
        
    def request(self, path: str, params = None):
        #请求发送器

        if not self.access_token:
            self._authenticate()
        
        #构造请求头
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

        #发送请求
        full_url= f"{self.api_url}{path}"
        try:
            res = requests.get(full_url, headers=headers, params=params)
            if res.status_code == 401:
                print("⚠️ 令牌好像过期了，尝试重新获取...")
                self._authenticate()
                headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
                res = requests.get(full_url, headers=headers, params=params, timeout=10)
            if res.status_code == 200:
                return res.json()
            else:
                print(f"❌ 请求出错: {res.status_code}")
                return None
        except Exception as e:
            print(f"请求失败: {e}")
            return None

    def search_cards(self, text: str) -> list[CardSearchResponse]:
        """搜索卡牌。
        :param text: 搜索文本
        """
        params = {
            "textFilter": text,
            "locale": "zh_CN",
            "page": 1,
            "pageSize": 5
        }

        data = self.request("/cards", params=params)
        if data:
            print("="*40)
            print("🕵️‍♀️ [侦探模式] 原始数据长这样：")
            # indent=4 让 JSON 缩进显示，ensure_ascii=False 让中文正常显示
            print(json.dumps(data, indent=4, ensure_ascii=False))
            print("="*40)

            response = CardSearchResponse(**data)
            return response.cards
        return []
