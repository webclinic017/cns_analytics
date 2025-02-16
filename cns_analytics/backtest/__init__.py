import pandas as pd
from collections import defaultdict
    
from .rebalance_amount import rebalance_amount
from .fix import get_fix_per_day, get_fix_per_day_yearly
from .risk import get_risk


        
def rollover(dfs, amount=100e3, enter='60d', exit='30d'):
    dfs = [df for df in dfs if len(df)]
    
    open_money = 0
    qty = 0

    history = defaultdict(list)
    index = []

    last_ts = None
    df0 = dfs[0]
    dfs[0] = df0[df0.index[-1] - pd.Timedelta(enter):]

    for df in dfs:
        if last_ts is not None:
            df = df[last_ts:]

        rollover_ts = df.index[-1] - pd.Timedelta(exit)

        for ts, px in df.iteritems():
            last_ts = ts

            if qty == 0:
                qty = amount / px
                open_money -= amount

            if ts >= rollover_ts:
                open_money += qty * px
                qty = 0
                break

            history['reval'].append(open_money + qty * px)
            index.append(ts)
            
    return pd.DataFrame(history, index).reval
            