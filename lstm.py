import pandas as pd

from scalecast.SeriesTransformer import SeriesTransformer
from scalecast.Forecaster import Forecaster
import matplotlib.pyplot as plt

def forcast(data: pd.DataFrame, next_date: int):
    data['time'] = pd.to_datetime(data['time'])
    data = data.sort_values("time", ascending= True)
    f = Forecaster(y = data['close'], current_dates=data['time'])
    f.set_test_length(next_date)
    f.generate_future_dates(next_date)

    transformer = SeriesTransformer(f)
    f = transformer.DiffTransform()

    f.add_ar_terms(24)
    f.add_seasonal_regressors('month','quarter',dummy=True)
    f.add_seasonal_regressors('year')
    f.add_time_trend()

    f.set_estimator('mlr')
    f.manual_forecast()

    f = transformer.DiffRevert(
        exclude_models = [m for m in f.history if m != 'mlr']
    ) # exclude all lstm models from the revert

    return f.export(models='mlr')["lvl_fcsts"]