class ExecutionHandler:
    def __init__(self):
        self.order_log = []

    def execute_order(self, signal, price):
        if signal != 0:
            self.order_log.append({'signal': signal, 'price': price})