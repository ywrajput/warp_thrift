# health scoring logic

def score_gpu_health(baseline_temp, max_temp, power_draw, utilization, throttled=False, errors=False):
    
    score = 0
    
    if max_temp != -1:
        if max_temp < 80: score += 20
        elif max_temp < 85: score += 15
        elif max_temp < 90: score += 10
        
    if baseline_temp < 50: score += 10
    elif baseline_temp < 60: score += 5
    
    if power_draw != -1:
        if 65 <= power_draw <= 70: score += 10
        elif 60 <= power_draw < 65: score += 5
        
    if utilization >= 99: score += 10
    elif utilization >= 90: score += 5
    
    if not throttled: score += 20 # unimplemented
    
    if not errors: score += 30 # unimplemented
    #elif errors: score += 15 # need to differentiate error types

    if score >= 85:
        status = "healthy"
        recommendation = "Safe for all workloads"
    elif score >= 65:
        status = "degraded"
        recommendation = "Limit to inference or light compute"
    else:
        status = "unstable"
        recommendation = "Do not deploy"

    return score, status, recommendation
