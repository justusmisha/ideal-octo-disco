import math

from loader import cur
from utils.data_calculator.roof_calculator import RoofCalculator

fundaments = ['lent_fund_price', 'zabiv_fund_price', 'vint_fund_price']


class SrubCalculator:
    def __init__(self, a, b, h, d, extra_wall: bool, roof: bool = None, vinosa_roof: int = None, fundament: int = None,
                 dostavka: int = None):
        super().__init__()
        self.a = a
        self.b = b
        self.h = h
        self.d = d
        self.extra_wall = min(self.a, self.b) if extra_wall else False
        self.fundament = fundaments[fundament - 1] if fundament else False
        self.dostavka = dostavka if dostavka else None
        self.roof = roof if roof else False
        if roof:
            self.l = vinosa_roof if vinosa_roof else False

    async def wall_V(self, wall):
        r2 = (self.d / 100 + wall / 100) / 2
        return 1 / 3 * math.pi * wall * (r2 ** 2 + (r2 * (self.d / 2) / 100) + (((self.d / 2) / 100) ** 2))

    async def brevna_count(self):
        return round(self.h / (self.d / 100 - 0.02))

    async def Vs(self):
        v_all_breven_a = await self.wall_V(self.a) * await self.brevna_count()
        v_all_breven_b = await self.wall_V(self.b) * await self.brevna_count()
        v_breven_extra = await self.wall_V(self.extra_wall) * await self.brevna_count()

        persentage = (((v_all_breven_a + v_all_breven_b) * 2) + v_breven_extra) * (12 / 100)
        if self.extra_wall:
            vs = (((v_all_breven_a + v_all_breven_b) * 2) + v_breven_extra) + persentage
        else:
            persentage = ((v_all_breven_a + v_all_breven_b) * 2) * (12 / 100)
            vs = (v_all_breven_a + v_all_breven_b) * 2 + persentage
        return vs

    async def srub_price(self):
        Vs = await self.Vs()
        les_price = await cur("SELECT price FROM constants WHERE name='les_price';")
        rubka_price = await cur("SELECT price FROM constants WHERE name='rubka_price';")
        total_price = Vs * les_price + Vs * rubka_price * 1.1
        return round(total_price)

    async def fundament_price(self):
        if self.fundament:
            fundament_price = await cur("SELECT price FROM constants WHERE name=%s;", self.fundament)
            price = (self.a + self.b) * 2 * 0.4 * 0.7 * fundament_price
            return price

    async def final_sborka_price(self):
        Vs = await self.Vs()
        sborka_price = await cur("SELECT price FROM constants WHERE name='sborka_price';")
        return round(Vs * sborka_price)

    async def mat_for_sborka_price(self):
        srub_price = await self.srub_price()
        return srub_price * 0.05

    async def dostavka_price(self):
        v = await self.Vs()
        if v <= 5:
            dostavka_per_km = 75
        elif 5 < v <= 10:
            dostavka_per_km = 90
        else:
            dostavka_per_km = 120

        return round((self.dostavka + 70) * 2 * dostavka_per_km)

    async def srub_usadka_price(self):
        srub_price = await self.srub_price()
        fundament_price = await self.fundament_price()
        final_sborka_price = await self.final_sborka_price()
        mat_for_sborka_price = await self.mat_for_sborka_price()
        price_no_dost_roof = srub_price + fundament_price + final_sborka_price + mat_for_sborka_price
        prices_dict = {'srub_usadka': round(price_no_dost_roof),
                       'srub': srub_price,
                       'fundament': fundament_price,
                       'sborka': final_sborka_price,
                       'mat_for_sborka': mat_for_sborka_price}

        if self.roof and self.dostavka:
            r = RoofCalculator(self.a, self.b)
            dostavka_price = await self.dostavka_price()
            roof_price = await r.roof_price()
            prices_dict['srub_usadka'] = price_no_dost_roof + dostavka_price + roof_price
            prices_dict['roof'] = roof_price
            prices_dict['dostavka'] = dostavka_price
        elif self.dostavka:
            prices_dict['srub_usadka'] = price_no_dost_roof + await self.dostavka_price()
            prices_dict['dostavka'] = await self.dostavka_price()
        elif self.roof:
            r = RoofCalculator(self.a, self.b)
            prices_dict['srub_usadka'] = price_no_dost_roof + await r.roof_price()
            prices_dict['roof'] = await r.roof_price()
        return prices_dict
