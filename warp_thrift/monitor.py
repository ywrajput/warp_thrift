# stress test & telemetry

import torch # type: ignore
import time
from datetime import datetime
import pynvml # type: ignore

def stress_gpu_with_monitoring(handle, duration_seconds=60):
    device = torch.device("cuda") # ensures it's on the GPU
    
    a = torch.randn((4096, 4096), device=device)
    b = torch.randn((4096, 4096), device=device)

    max_temp = -1
    max_power = -1
    last_util = -1 # will change to avg utilization over the course of the test
    
    start_time = time.time()
    iterations = 0
    
    telemetry_log = [] # want to update live while the test is running

    while time.time() - start_time < duration_seconds:
        c = torch.matmul(a, b)
        torch.cuda.synchronize() # wait for completion because torch.matmul is async
        
        timestamp = round(time.time() - start_time, 2) # in order to be consistent with the telemetry log
        temp = power = util = -1

        try:
            temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            max_temp = max(max_temp, temp)
        except pynvml.NVMLError: pass

        try:
            power = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000
            max_power = max(max_power, power)
        except pynvml.NVMLError: pass

        try:
            util = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
            last_util = util
        except pynvml.NVMLError: pass
        
        # live telemetry
        telemetry_log.append({
            "time_sec": timestamp,
            "temp_C": temp,
            "power_W": power,
            "utilization_pct": util
        })

        iterations += 1

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "max_temp": max_temp,
        "max_power": max_power,
        "utilization": last_util,
        "iterations": iterations,
        #"telemetry": telemetry_log
    }
