import backtrader as bt
import pytz

__ALL__ = ['FluctAgg']

class FluctAgg(bt.Indicator):
    params = (
        ('fast_rsi_period', 3),
        ('slow_rsi_period', 14),
        ('backpeek_size', 3),
    )

    lines = ('fluct', 'fluct_agg',)  # 增加 'fluct' line

    def __init__(self):
        super(FluctAgg, self).__init__()
        self.addminperiod(1)

        # RSI and CrossOver
        self.fast_rsi = bt.indicators.RSI(self.data.close, period=self.params.fast_rsi_period)
        self.slow_rsi = bt.indicators.RSI(self.data.close, period=self.params.slow_rsi_period)
        self.rsi_crossover = bt.indicators.CrossOver(self.fast_rsi, self.slow_rsi)

    def next(self):
        # Calculate fluctuation for the current bar
        rsi_delta_max = max(abs(self.fast_rsi[-i] - self.slow_rsi[-i]) for i in range(len(self.fast_rsi)))

        max_slow_rsi = max(self.slow_rsi.get(size=len(self.slow_rsi)))
        min_slow_rsi = min(self.slow_rsi.get(size=len(self.slow_rsi)))

        fluct = 0
        if self.rsi_crossover[0] == 1 and abs(self.fast_rsi[0] - self.slow_rsi[0]) < (rsi_delta_max * 2 / 3.0) and \
           self.slow_rsi[0] > (max_slow_rsi - min_slow_rsi) / 3.0 + min_slow_rsi:
            fluct = 1
        elif self.rsi_crossover[0] == -1 and abs(self.fast_rsi[0] - self.slow_rsi[0]) < (rsi_delta_max * 2 / 3.0) and \
             self.slow_rsi[0] < (max_slow_rsi - min_slow_rsi) * 2 / 3.0 + min_slow_rsi:
            fluct = -1

        # Assign fluct to the 'fluct' line
        self.lines.fluct[0] = fluct

        # Aggregate fluctuation over the backpeek window
        count = 0
        last_fluct = fluct
        index = 0

        for _ in range(self.p.backpeek_size):
            f, index = self._backpeek(index)
            if f != 0 and f != last_fluct:
                count += 1
            last_fluct = f

        self.lines.fluct_agg[0] = 1 if count == self.p.backpeek_size else 0

    def _backpeek(self, index):
        """
        Look back to find the most recent non-zero fluctuation within the backpeek size.
        """
        ret = 0
        i = 0
        while i < self.p.backpeek_size:
            if self.lines.fluct[index - i - 1] != 0:
                ret = self.lines.fluct[index - i - 1]
                break
            i += 1
        return ret, index - i - 1

    def log(self, txt):
        dt = self.datas[0].datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')
        print(f'{dt}: {txt}')
