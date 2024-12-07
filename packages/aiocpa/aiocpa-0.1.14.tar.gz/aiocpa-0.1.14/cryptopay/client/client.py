from typing import TYPE_CHECKING

from cryptopay import loggers
from cryptopay.client import MAINNET, TESTNET
from cryptopay.exceptions import APIError, WrongNetworkError
from cryptopay.methods import Methods
from cryptopay.polling import PollingConfig, PollingManager
from cryptopay.tools import Tools
from cryptopay.utils import PropagatingThread
from cryptopay.webhook import AiohttpManager, RequestHandler

from .session import AiohttpSession

if TYPE_CHECKING:
    from cryptopay.client import APIServer
    from cryptopay.methods import CryptoPayMethod
    from cryptopay.types import _CryptoPayType
    from cryptopay.webhook import _APP, WebhookManager

    from .session import BaseSession


class CryptoPay(Methods, Tools, RequestHandler, PollingManager):
    """
    Client class providing API methods.

    :param token: Crypto Bot API token
    :param session: HTTP Session
    :param api_server: Crypto Bot API server
    """

    def __init__(
        self,
        token: str,
        api_server: "APIServer" = MAINNET,
        session: "type[BaseSession]" = AiohttpSession,
        manager: "WebhookManager[_APP] | None" = None,
        polling_config: "PollingConfig | None" = None,
    ) -> None:
        self._token = token
        self._session = session(api_server)
        RequestHandler.__init__(self, manager or AiohttpManager())
        PollingManager.__init__(self, polling_config or PollingConfig())
        thread = PropagatingThread(target=self.__auth)
        thread.start()
        thread.join()

    async def __call__(
        self,
        method: "CryptoPayMethod[_CryptoPayType]",
    ) -> "_CryptoPayType":
        """
        Request method.

        Use this method to make an API request.

        :param method: CryptoPayMethod object.
        :return: :class:`CryptoPayType` object.
        """
        async with self._session as session:
            loggers.client.debug("Requesting: %s", method.__method__)
            return await session.request(self._token, self, method)

    def __auth(self) -> None:
        try:
            me = self.get_me()
            loggers.client.info(
                "Authorized as '%s' id=%d on %s",
                me.name,
                me.app_id,
                self._session.api_server.name,
            )
        except APIError:
            current_net = self._session.api_server
            if current_net == MAINNET:
                self._session = self._session.__class__(TESTNET)
            else:
                self._session = self._session.__class__(MAINNET)
            self.get_me()
            net = self._session.api_server
            msg = (
                "Authorization failed. Token is served by the "
                f"{net.name}, you are using {current_net.name}"
            )
            raise WrongNetworkError(msg) from None
