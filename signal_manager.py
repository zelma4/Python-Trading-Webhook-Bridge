from collections import deque

class SignalManager:
    def __init__(self):
        self.signals = deque(maxlen=6)  # зберігає останні 6 сигналів

    def add(self, signal: str):
        self.signals.append(signal.upper())  # 'BUY' або 'SELL'

    def check_exit_pattern(self):
        s = list(self.signals)
        
        buy_patterns = [
            ['B', 'S', 'B'],
            ['B', 'B', 'S'],
            ['B', 'B', 'B', 'S'],
            ['B', 'B', 'B', 'B', 'S'],
            ['B', 'B', 'B', 'B', 'B']
        ]

        sell_patterns = [
            ['S', 'B', 'S'],
            ['S', 'S', 'B'],
            ['S', 'S', 'S', 'B'],
            ['S', 'S', 'S', 'S', 'B'],
            ['S', 'S', 'S', 'S', 'S']
        ]

        for pattern in buy_patterns:
            if s[-len(pattern):] == pattern:
                return 'EXIT_BUY'

        for pattern in sell_patterns:
            if s[-len(pattern):] == pattern:
                return 'EXIT_SELL'

        return None