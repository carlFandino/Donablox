import asyncio
import json
from roblox import Client
from roblox.utilities.requests import Requests
class Donator:
	def __init__(self, data, image_url, rank):
		self.data = data
		self.name = self.data["agent"]["name"]
		self.date = self.data["created"].split("T")[0]
		self.isPending = self.data["isPending"]
		self.roblox_id = self.data["agent"]["id"]
		self.productName = self.data["details"]["name"]
		self.amount = self.data["currency"]["amount"]
		self.rank = rank
		self.image_url = image_url
	def __repr__(self):
		return f"<{self.__class__.__name__} {self.name}>"


class Transactions:
	def __init__(self, client, req, roblox_id):
		self.req = req
		self.client = client
		self.products = ["Mercury","Venus","Earth","Mars","Jupiter"]

	async def __get_image_url(self, roblox_id):
		_ses = await self.req.get(f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={roblox_id}&size=100x100&format=Png&isCircular=false")
		__image_url = json.loads(_ses.text)
		return __image_url["data"][0]["imageUrl"]

	async def get_donators(self):
		_ses = await self.req.get("https://economy.roblox.com/v2/users/448924843/transactions?cursor=&limit=100&transactionType=Sale")
		__data = json.loads(_ses.text)["data"]
		__donators = []
		rank = 0
		for i in __data:
			if i["details"]["name"] in self.products:
			    _get_user_avatar = await self.req.get(f"https://www.roblox.com/users/3331094552/profile")
			    rank += 1
			    __donators.append(Donator(i, await self.__get_image_url(i["agent"]["id"]), rank))
		return __donators

class Player:
	def __init__(self, client):
		self.client = Client(client)
		
	async def main(self):
		self.__user = await self.client.get_authenticated_user()
		roblox_id = await self.get_id()
		self.Transactions = Transactions(self.client, self.client.requests, roblox_id)

	async def get_donators(self):
		return await self.Transactions.get_donators()

	async def get_id(self):
		return self.__user.id

	async def get_name(self):
		return self.__user.name

	async def get_display_name(self):
		return self.__user.display_name

