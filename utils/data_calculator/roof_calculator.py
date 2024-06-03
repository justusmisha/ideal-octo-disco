import math
from loader import cur


class RoofCalculator:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    async def stropil_length(self):
        min_length = min(self.a, self.b)
        length = math.sqrt(((min_length/2)**2) * 2) + 0.5
        return length

    async def s_roof(self):
        max_length = max(self.a, self.b)
        stropil_length = await self.stropil_length()  # Await here
        s_roof = (stropil_length * (max_length + 1)) * 2
        return s_roof

    async def work_roof_price(self):
        roof_price = await cur("SELECT price FROM constants WHERE name='roof_price';")
        s_roof = await self.s_roof()
        return s_roof * roof_price

    async def stropil_count(self):
        max_length = max(self.a, self.b)
        count = ((max_length/0.6)+1)*2
        return count

    async def v_stropil(self):
        stropil_count = await self.stropil_count()  # Await here
        return stropil_count * 0.045

    async def v_obreshetka(self):
        s_roof = await self.s_roof()  # Await here
        return s_roof/2 * 0.025

    async def v_doska_price(self):
        doska_price = await cur("SELECT price FROM constants WHERE name='doska_price';")
        v_stropil = await self.v_stropil()  # Await here
        v_obreshetka = await self.v_obreshetka()  # Await here
        return (v_stropil + v_obreshetka) * 1.1 * doska_price

    async def s_mch_price(self):
        mch_price = await cur("SELECT price FROM constants WHERE name='mch_price';")
        s_roof = await self.s_roof()  # Await here
        return s_roof * mch_price

    async def roof_price(self):
        work_roof_price = await self.work_roof_price()
        v_doska_price = await self.v_doska_price()
        s_mch_price = await self.s_mch_price()
        return round(work_roof_price + v_doska_price + s_mch_price)
