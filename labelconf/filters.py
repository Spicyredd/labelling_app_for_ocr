import logging

class IgnoreStreamlitRequestsFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        if "/_stcore" in message:
            return False
        return True