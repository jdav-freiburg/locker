from datetime import datetime, timezone
from pathlib import Path


def now_timestamp() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def timestamp_to_localtz(timestamp: str) -> datetime:
    timestamp_dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    timestamp_dt = timestamp_dt.replace(tzinfo=timezone.utc)
    return datetime.fromtimestamp(timestamp_dt.timestamp())


class RotatingLog:
    def __init__(self, path: str, n_logs: int, max_size: int):
        """
        Initializes the rotating log.

        Args:
            path: Base path and primary log file. Other logfiles will be named .n.log
            n_logs: Number of logfiles to keep before deleting
            max_size: Maximum size of a logfile before rotating
        """
        self.path = Path(path)
        self.n_logs = n_logs
        self.max_size = max_size
        self.file = open(self.path, 'ab')

    def _logfile(self, i: int):
        return self.path.with_name(self.path.stem + f".{i}" + self.path.suffix)

    def _next_logfile(self):
        next_logfile = self._logfile(self.n_logs - 1)
        if next_logfile.is_file():
            next_logfile.unlink()
        for i in range(self.n_logs - 2, 0, -1):
            logfile = self._logfile(i)
            logfile.rename(next_logfile)
            next_logfile = logfile
        self.file.close()
        self.path.rename(next_logfile)
        self.file = open(self.path, 'ab')

    def write(self, data: str):
        data_b = (now_timestamp() + ": " + data + "\n").encode()
        if self.file.tell() + len(data_b) > self.max_size:
            self._next_logfile()
        self.file.write(data_b)
        self.file.flush()
