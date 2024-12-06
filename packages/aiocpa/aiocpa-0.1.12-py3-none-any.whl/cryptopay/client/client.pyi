from builtins import bool as _bool
from builtins import float as _float
from builtins import list as _list
from collections.abc import Awaitable, Callable, Generator
from datetime import datetime
from typing import Any, TypeVar

from typing_extensions import Self

from cryptopay.client import APIServer
from cryptopay.enums import (
    Asset,
    CheckStatus,
    CurrencyType,
    Fiat,
    InvoiceStatus,
    PaidBtnName,
)
from cryptopay.methods import CryptoPayMethod
from cryptopay.polling import PollingConfig
from cryptopay.polling.manager import Handler, PollingTask
from cryptopay.types import (
    App,
    AppStats,
    Balance,
    Check,
    Currency,
    ExchangeRate,
    Invoice,
    Transfer,
    _CryptoPayType,
)
from cryptopay.webhook import (
    _APP,
    WebhookManager,
)

from .session import BaseSession

_T = TypeVar("_T")

# These classes are needed for syncronous type hinting.
# Stub file annotates the methods as syncronous, but
# while using this lib asynchronously, the actual return type
# is a coroutine that returns an annotated type, so these classes
# will annotate awaited object as return type.

class list(_list[_T]):  # noqa: A001, N801
    def __await__(self) -> Generator[None, None, Self]: ...

class bool(_bool):  # type: ignore[misc]  # noqa: A001, N801
    def __await__(self) -> Generator[None, None, Self]: ...

class float(_float):  # noqa: A001, N801
    def __await__(self) -> Generator[None, None, Self]: ...

class CryptoPay:
    _token: str
    _session: type[BaseSession]
    _timeout: int
    _delay: int
    _tasks: dict[int, PollingTask]
    _handler: Handler | None
    _exp_handler: Handler | None

    def __init__(
        self,
        token: str,
        api_server: APIServer = ...,
        session: type[BaseSession] = ...,
        manager: WebhookManager[_APP] | None = None,
        polling_config: PollingConfig | None = None,
    ) -> None: ...
    async def __call__(
        self,
        method: CryptoPayMethod[_CryptoPayType],
    ) -> _CryptoPayType: ...
    def get_me(self) -> App: ...
    def create_invoice(
        self,
        amount: _float,
        asset: Asset | str | None = None,
        *,
        currency_type: CurrencyType | None = None,
        fiat: Fiat | str | None = None,
        accepted_assets: _list[Asset] | None = None,
        description: str | None = None,
        hidden_message: str | None = None,
        paid_btn_name: PaidBtnName | None = None,
        paid_btn_url: str | None = None,
        payload: str | None = None,
        allow_comments: bool | None = None,
        allow_anonymous: bool | None = None,
        expires_in: int | None = None,
    ) -> Invoice: ...
    def delete_invoice(
        self,
        invoice_id: int,
    ) -> bool: ...
    def create_check(
        self,
        amount: _float,
        asset: Asset | str,
        pin_to_user_id: int | None = None,
        pin_to_username: str | None = None,
    ) -> Check: ...
    def delete_check(
        self,
        check_id: int,
    ) -> bool: ...
    def transfer(
        self,
        user_id: int,
        asset: str,
        amount: float,
        spend_id: str | None = None,
        comment: str | None = None,
        disable_send_notification: bool | None = None,
    ) -> Transfer: ...
    def get_invoices(
        self,
        asset: Asset | None = None,
        fiat: Fiat | None = None,
        invoice_ids: _list[int] | None = None,
        status: InvoiceStatus | None = None,
        offset: int | None = None,
        count: int | None = None,
    ) -> list[Invoice]: ...
    def get_checks(
        self,
        asset: Asset | str | None = None,
        check_ids: _list[int] | None = None,
        status: CheckStatus | str | None = None,
        offset: int | None = None,
        count: int | None = None,
    ) -> list[Check]: ...
    def get_transfers(
        self,
        asset: Asset | None = None,
        transfer_ids: _list[int] | None = None,
        spend_id: str | None = None,
        offset: int | None = None,
        count: int | None = None,
    ) -> list[Transfer]: ...
    def get_balance(self) -> list[Balance]: ...
    def get_exchange_rates(self) -> list[ExchangeRate]: ...
    def get_currencies(self) -> list[Currency]: ...
    def get_stats(
        self,
        start_at: datetime | None = None,
        end_at: datetime | None = None,
    ) -> AppStats: ...
    def delete_all_checks(self) -> None: ...
    def delete_all_invoices(self) -> None: ...
    def exchange(
        self,
        amount: _float,
        source: Asset | Fiat | str,
        target: Asset | Fiat | str,
    ) -> float: ...
    def get_balance_by_asset(
        self,
        asset: Asset | str,
    ) -> float: ...
    def polling_handler(self) -> Callable[[Handler], Handler]: ...
    def expired_handler(self) -> Callable[[Handler], Handler]: ...
    def webhook_handler(
        self,
        app: _APP,
        path: str,
    ) -> Callable[
        [Callable[[Invoice], Awaitable]],
        Callable[[Invoice], Awaitable],
    ]: ...
    def feed_update(
        self,
        handler: Callable[[Invoice], Awaitable],
        body: dict[str, Any],
        headers: dict[str, str],
    ) -> None: ...
    async def __process_invoice(
        self,
        invoice: Invoice,
    ) -> None: ...
    def _add_invoice(
        self,
        invoice: Invoice,
        data: dict[str, Any],
    ) -> None: ...
    async def run_polling(
        self,
        parallel: Callable[[], Any] | None = None,
    ) -> None: ...
