import threading


class CustomLogger:
    logs = []
    lock = threading.Lock()

    @staticmethod
    def add(message: str):
        with CustomLogger.lock:
            CustomLogger.logs.append(message)

    @staticmethod
    def reset():
        with CustomLogger.lock:
            CustomLogger.logs = []

    @staticmethod
    def get():
        with CustomLogger.lock:
            return "\n".join(CustomLogger.logs)
