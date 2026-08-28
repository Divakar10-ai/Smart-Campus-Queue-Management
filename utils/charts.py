import pandas as pd

def service_summary(rows):
    return pd.DataFrame([dict(r) for r in rows])
