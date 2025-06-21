from warp_thrift.benchmark import run_full_benchmark
from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex

nvmlInit()
handle = nvmlDeviceGetHandleByIndex(0)

report = run_full_benchmark(handle, duration=10)

print("\n🧪 Full GPU Diagnostic Report:")
print(report)


