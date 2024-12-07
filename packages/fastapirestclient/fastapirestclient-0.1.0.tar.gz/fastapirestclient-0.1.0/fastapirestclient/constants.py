API_HEADERS = {
    "Content-Type": "application/json",
}

API_TIMEOUT = 10


class API_ENDPOINT:
    fetch_ticker = "ticker"
    fetch_order_book = "order_book"
    place_order = "order"
    cancel_order = "order/cancel"
    get_balance = "balance"
