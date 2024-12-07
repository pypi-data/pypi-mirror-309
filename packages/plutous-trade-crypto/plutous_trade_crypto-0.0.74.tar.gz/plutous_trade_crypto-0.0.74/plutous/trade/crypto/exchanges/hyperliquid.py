import asyncio

from ccxt.base.types import FundingRate, Market
from ccxt.pro import hyperliquid


class Hyperliquid(hyperliquid):
    async def fetch_markets(self, params={}) -> list[Market]:
        """
        retrieves data on all markets for hyperliquid

        https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/perpetuals#retrieve-perpetuals-asset-contexts-includes-mark-price-current-funding-open-interest-etc
        https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint/spot#retrieve-spot-asset-contexts

        :param dict [params]: extra parameters specific to the exchange API endpoint
        :returns dict[]: an array of objects representing market data
        """
        type, params = self.safe_value(params, "type"), self.omit(params, "type")
        if type == "spot":
            return await self.fetch_spot_markets(params)
        elif type == "swap":
            return await self.fetch_swap_markets(params)
        else:
            rawPromises = [
                self.fetch_swap_markets(params),
                self.fetch_spot_markets(params),
            ]
            promises = await asyncio.gather(*rawPromises)
            swapMarkets = promises[0]
            spotMarkets = promises[1]
            return self.array_concat(swapMarkets, spotMarkets)

    def parse_funding_rate(self, info, market: Market = None) -> FundingRate:
        fr = super().parse_funding_rate(info, market)
        fr["timestamp"] = self.milliseconds()
        fr["datetime"] = self.iso8601(fr["timestamp"])
        return fr
