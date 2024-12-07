"""DataFrame Manipulation Library"""
import pandas as pd


def mark_events(
        data: pd.DataFrame,
        ref_frame: int = 5
):
    """Mark events

    Args:
        data (pd.DataFrame): _description_
        ref_frame (int, optional): _description_. Defaults to 5.

    Returns:
        _type_: _description_
    """
    data = data.copy()
    data['sell'] = (
        data['close'] == data['close'].shift(
            -ref_frame
        ).rolling(
            2 * ref_frame
        ).max()
    ).astype(int)
    data['buy'] = (
        data['close'] == data['close'].shift(
            -ref_frame
        ).rolling(
            2 * ref_frame
        ).min()
    ).astype(int)

    data['hold'] = data.apply(lambda row: int(
        not (row['sell'] or row['buy'])), axis=1)

    data['buy_pnl'] = (
        (
            data['close'].rolling(ref_frame).max(
            ).shift(-ref_frame) - data['close']
        ) * data['buy']
    ).round(2).astype(float)

    data['sell_pnl'] = (
        (
            data['close'] -
            data['close'].rolling(ref_frame).min().shift(-ref_frame)
        ) * data['sell']
    ).round(2).astype(float)

    data['buy'] = data['buy'].shift(-1)
    data['sell'] = data['sell'].shift(-1)
    data['hold'] = data['hold'].shift(-1)
    return data


# def simulate_trade(
#         ohlc_df: pd.DataFrame,
#         entry_index: pd.Timestamp,
#         sl_func: Callable[[pd.DataFrame, pd.Timestamp], pd.Series],
#         tp_func: Callable[[pd.DataFrame, pd.Timestamp], pd.Series],
#         time_frame: int = -1,
# ):
#     """Simulate trade
#     """
#     entry_price = ohlc_df.loc[entry_index]['close']

#     sim_df = ohlc_df[entry_index:].copy()
#     sim_df = sim_df[:time_frame].copy() if time_frame > 0 else sim_df
#     sim_df['sl'] = sl_func(ohlc_df, entry_index)
#     sim_df['tp'] = tp_func(ohlc_df, entry_index)
#     entry_sl = sim_df.loc[entry_index]['sl']

#     sim_df = sim_df[1:].copy()
#     sl_exit_df = sim_df[sim_df['close'] < sim_df['sl']].copy()
#     sl_exit_time = sl_exit_df.index[0] if not sl_exit_df.empty else sim_df.index[-1]

#     tp_exit_df = sim_df[sim_df['close'] > sim_df['tp']].copy()
#     tp_exit_time = tp_exit_df.index[0] if not tp_exit_df.empty else sim_df.index[-1]

#     exit_time = min(sl_exit_time, tp_exit_time)
#     exit_price = ohlc_df.loc[exit_time]['close']
#     pnl = exit_price - entry_price

#     exit_type = 'to'

#     if len(tp_exit_df) > 0 and len(sl_exit_df) < len(tp_exit_df):
#         exit_type = 'tp'

#     if len(sl_exit_df) > 0 and len(sl_exit_df) > len(tp_exit_df):
#         exit_type = 'trail_sl'
#         if exit_price < entry_sl:
#             exit_type = 'sl'

#     return {
#         'entry_price': entry_price,
#         'entry_time': entry_index,
#         'exit_price': exit_price,
#         'exit_time': exit_time,
#         'pnl': pnl,
#         'duration': (exit_time - entry_index),
#         'entry_sl': entry_sl,
#         'sl': sim_df.loc[sl_exit_time]['sl'],
#         'tp': sim_df.loc[tp_exit_time]['tp'],
#         'exit_type': exit_type,
#     }
