from typing import TYPE_CHECKING

from cryptopay.types import Balance

from .base import CryptoPayMethod

if TYPE_CHECKING:
    import cryptopay


class GetBalance:
    """getBalance method."""

    class GetBalanceMethod(CryptoPayMethod[list[Balance]]):
        __return_type__ = list[Balance]
        __method__ = "getBalance"

    async def get_balance(self: "cryptopay.CryptoPay") -> list[Balance]:
        """
        getBalance method.

        Use this method to get balances of your app.
        Requires no parameters.
        Returns array of :class:`Balance`.

        Source: https://help.crypt.bot/crypto-pay-api#getBalance

        :return: List of :class:`Balance` objects.
        """
        return await self(self.GetBalanceMethod(**locals()))
