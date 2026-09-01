import threading
import os

"""
Utility to terminate the test process after a configurable timeout.
This is intended for CI/pipeline integration where long-running load tests
must be bounded. Configure with PIPELINE_TIMEOUT (seconds). Default: 10s.
"""


import _thread

def start_terminator(seconds: int | None = None):
    try:
        if seconds is None:
            seconds = int(os.getenv('PIPELINE_TIMEOUT', '10'))
    except Exception:
        seconds = 10

    def _interrupt():
        try:
            _thread.interrupt_main()  # raises KeyboardInterrupt in main thread
        except Exception:
            # fallback to hard exit if interrupt fails
            try:
                os._exit(1)
            except Exception:
                pass

    t = threading.Timer(seconds, _interrupt)
    t.daemon = True
    t.start()
    return t


def stop_terminator(timer: threading.Timer | None):
    if timer is None:
        return
    try:
        timer.cancel()
    except Exception:
        pass
