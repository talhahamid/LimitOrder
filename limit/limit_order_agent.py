# from trading_framework.execution_client import ExecutionClient
# from trading_framework.price_listener import PriceListener


# class LimitOrderAgent(PriceListener):

#     def __init__(self, execution_client: ExecutionClient) -> None:
#         """

#         :param execution_client: can be used to buy or sell - see ExecutionClient protocol definition
#         """
#         super().__init__()

#     def on_price_tick(self, product_id: str, price: float):
#         # see PriceListener protocol and readme file
#         pass


class LimitOrderAgent:
    def __init__(self, execution_client):
        self.execution_client = execution_client
        self.orders = []

    def price_tick(self, product_id: str, price: float):
        if product_id == 'IBM' and price < 100:
            self.execution_client.execute_order('BUY', 'IBM', 1000, price)

    def add_order(self, action: str, product_id: str, amount: int, limit: float):
        self.orders.append((action, product_id, amount, limit))

    def execute_held_orders(self, current_price: float):
        orders_to_remove = []
        for order in self.orders:
            action, product_id, amount, limit = order
            if (action == 'BUY' and current_price <= limit) or (action == 'SELL' and current_price >= limit):
                self.execution_client.execute_held_orders(action, product_id, amount, current_price)
                orders_to_remove.append(order)  
        for order in orders_to_remove:
            self.orders.remove(order)

