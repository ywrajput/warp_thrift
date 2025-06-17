from warp_thrift.diagnostics import get_gpu_baseline_info
from warp_thrift.monitor import stress_gpu_with_monitoring
from warp_thrift.scoring import score_gpu_health
import pynvml # type: ignore

def run_full_diagnostic(index=0, duration=30):
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(index)

    # Step 1: Get GPU metadata
    gpu_info = get_gpu_info(handle)

    # Step 2: Stress test with monitoring
    telemetry = stress_gpu_with_monitoring(handle, duration)

    # Step 3: Score the GPU
    score_result = score_gpu_health(telemetry)

    return {
        "gpu_name": gpu_info.get("name", "Unknown"),
        "score": score_result["score"],
        "status": score_result["status"],
        "recommendation": score_result["recommendation"],
        "max_temp": telemetry["max_temp"],
        "max_power": telemetry["max_power"],
        "utilization": telemetry["utilization"],
        "iterations": telemetry["iterations"]
    }

if __name__ == "__main__":
    result = run_full_diagnostic()
    for k, v in result.items():
        print(f"{k}: {v}")

