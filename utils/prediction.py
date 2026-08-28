def predict_wait(waiting_count, avg_minutes=4):
    return max(0, int(waiting_count) * int(avg_minutes))

def confidence_score(waiting_count):
    if waiting_count <= 5:
        return 0.90
    if waiting_count <= 10:
        return 0.80
    return 0.70
