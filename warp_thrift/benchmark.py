from .monitor import stress_gpu_with_monitoring
from .scoring import score_gpu_health
from .diagnostics import get_gpu_info

def run_full_benchmark(handle, duration=60):
    """
    Run diagnostics, stress test, and scoring on a single GPU.
    
    Args:
        handle: NVML handle to the GPU.
        duration: Stress test duration in seconds.
    
    Returns:
        dict: Full report with metadata, stress metrics, and score.
    """
    info = get_gpu_info(handle)
    metrics = stress_gpu_with_monitoring(handle, duration)

    score_info = score_gpu_health(
      baseline_temp=metrics["baseline_temp"],
      max_temp=metrics["max_temp"],
      power_draw=metrics["max_power"],
      utilization=metrics["utilization"]
    )


    return {
        "info": info,
        "metrics": metrics,
        "score": score_info
    }
