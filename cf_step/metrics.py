# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/metrics.ipynb (unless otherwise specified).

__all__ = ['moving_avg']

# Cell
def moving_avg(w, results):
    cumsum, moving_avgs = [0], []

    for i, x in enumerate(results, 1):
        cumsum.append(cumsum[i-1] + x)
        if i >= w:
            moving_avg = (cumsum[i] - cumsum[i-w]) / w
            moving_avgs.append(moving_avg)
    return moving_avgs