# baseline info & thresholds

import pynvml # type: ignore

def get_gpu_baseline_info(handle):
    temperature = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
    power_usage = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000
    memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    try:
        fan_speed = pynvml.nvmlDeviceGetFanSpeed(handle)
    except pynvml.NVMLError:
        fan_speed = "Not supported"

    info = {
        "Temperature (C)": temperature,
        "Power Usage (W)": power_usage,
        "Memory Used (MB)": memory_info.used // (1024**2),
        "Memory Total (MB)": memory_info.total // (1024**2),
        "Fan Speed (%)": fan_speed,
    }
    return info

def print_temperature_thresholds(handle):
    try:
        slowdown = pynvml.nvmlDeviceGetTemperatureThreshold(
            handle, pynvml.NVML_TEMPERATURE_THRESHOLD_SLOWDOWN)
        print(f"⚠️  Slowdown Threshold: {slowdown} °C")
    except pynvml.NVMLError as e:
        print(f"Slowdown Threshold: Not supported ({str(e)})")

    try:
        shutdown = pynvml.nvmlDeviceGetTemperatureThreshold(
            handle, pynvml.NVML_TEMPERATURE_THRESHOLD_SHUTDOWN)
        print(f"🔥 Shutdown Threshold: {shutdown} °C")
    except pynvml.NVMLError as e:
        print(f"Shutdown Threshold: Not supported ({str(e)})")
