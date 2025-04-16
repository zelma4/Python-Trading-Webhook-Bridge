import time

class HedgeManager:
    def __init__(self):
        self.recent_signals = {"buy": [], "sell": []}
        self.trail_stops = {}

    def track_signal(self, signal_type):
        queue = self.recent_signals[signal_type]
        queue.append(signal_type[0].upper())  # 'B' or 'S'
        if len(queue) > 7:
            queue.pop(0)

    def match_sequence(self, signal_type):
        buy_seq = {
            "1": ["B", "S", "B"],
            "2": ["B", "B", "S"],
            "3": ["B", "B", "B", "S"],
            "4": ["B", "B", "B", "B", "S", "B", "S"]
        }

        sell_seq = {
            "1": ["S", "B", "S"],
            "2": ["S", "S", "B"],
            "3": ["S", "S", "S", "B"],
            "4": ["S", "S", "S", "S", "B", "S", "B"]
        }

        current = self.recent_signals[signal_type]
        sequences = buy_seq if signal_type == "buy" else sell_seq

        for key, pattern in sequences.items():
            if current[-len(pattern):] == pattern:
                return key
        return None