# Copyright (c) 2025 - dato Nejat Philip Eryiğit. All rights reserved.
import errno
import json
import os
import time
from pathlib import Path

class _DomainLock:

    def __init__(self, lock_path: Path, timeout: float=4.0, stale_after: float=12.0):
        self.lock_path = lock_path
        self.timeout = timeout
        self.stale_after = stale_after
        self._fd = None

    def __enter__(self):
        deadline = time.monotonic() + self.timeout
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        while True:
            try:
                self._fd = os.open(str(self.lock_path), os.O_CREAT | os.O_EXCL | os.O_RDWR)
                os.write(self._fd, f'{os.getpid()}:{time.time()}'.encode('utf-8'))
                return True
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    return False
                try:
                    if time.time() - self.lock_path.stat().st_mtime > self.stale_after:
                        self.lock_path.unlink(missing_ok=True)
                        continue
                except OSError:
                    pass
                if time.monotonic() >= deadline:
                    return False
                time.sleep(0.025)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._fd is not None:
            try:
                os.close(self._fd)
            except OSError:
                pass
            self._fd = None
        try:
            self.lock_path.unlink(missing_ok=True)
        except OSError:
            pass

class AtomicStateStore:

    @staticmethod
    def read_state(state_file: Path) -> dict:
        if not state_file.is_file():
            return {}
        try:
            return json.loads(state_file.read_text(encoding='utf-8'))
        except Exception:
            return {}

    @staticmethod
    def write_state_atomic(state_file: Path, data: dict):
        tmp_file = state_file.with_name(f'.{state_file.name}.{os.getpid()}.tmp')
        try:
            tmp_file.write_text(json.dumps(data, indent=2), encoding='utf-8')
            os.replace(str(tmp_file), str(state_file))
        except OSError:
            try:
                tmp_file.unlink(missing_ok=True)
            except OSError:
                pass
