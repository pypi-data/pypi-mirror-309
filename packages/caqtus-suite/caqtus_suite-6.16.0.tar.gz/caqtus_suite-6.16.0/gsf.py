import time

t0 = time.perf_counter()
import PySide6

t1 = time.perf_counter()

print(f"Time: {(t1 - t0) * 1e3:.4f} ms")
