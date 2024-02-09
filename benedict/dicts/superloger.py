import time
import super_py as sp #pip install super-py


log = sp.logging.Logger("benchmark",
    ts_color="bright_green",
    terminal=True,
)

@log.benchmark(with_args=[0])
def wait(seconds):
    time.sleep(seconds)

for i in range(10):
    wait(i / 10)

log("Simple Log Message")