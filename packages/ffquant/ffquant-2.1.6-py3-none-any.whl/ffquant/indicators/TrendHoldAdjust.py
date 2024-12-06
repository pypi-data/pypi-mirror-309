import backtrader as bt
from ffquant.indicators.Trend import Trend
from ffquant.indicators.TrendHold import TrendHold
from ffquant.indicators.TrendWarrant import TrendWarrant
from ffquant.indicators.TurningPoint import TurningPoint
from ffquant.indicators.ActiveBuySell import ActiveBuySell
from ffquant.utils.Logger import stdout_log
import pytz

__ALL__ = ['TrendHoldAdjust']

class TrendHoldAdjust(bt.Indicator):
    (BEARISH, NA, BULLISH) = (-1, 0, 1)

    params = (
        ('symbol', 'CAPITALCOM:HK50'),
        ('crossover_backpeek_size', 1),
        ('debug', False),
    )

    lines = ('tha',)

    def __init__(self):
        super(TrendHoldAdjust, self).__init__()
        self.addminperiod(1)

        self.trend = Trend(symbol=self.p.symbol, debug=False)
        self.trend_warrant = TrendWarrant(symbol=self.p.symbol, debug=False)
        self.trendhold = TrendHold(symbol=self.p.symbol, debug=False)
        self.tp = TurningPoint(symbol=self.p.symbol, debug=False)
        self.abs = ActiveBuySell(symbol=self.p.symbol, debug=False)
        self.fast_rsi = bt.indicators.RSI(self.data.close, period=3)
        self.slow_rsi = bt.indicators.RSI(self.data.close, period=14)
        self.crossover = bt.indicators.CrossOver(self.fast_rsi, self.slow_rsi)

        # 完成对信号的缓存
        self.trendhold_list = []
        self.tp_list = []
        self.trend_list = []
        self.active_buy_sell_list = []

        # 对上一时刻信号状态的缓存
        self.trendhold_now = TrendHoldAdjust.NA
        self.trendhold_last = TrendHoldAdjust.NA

        self.window_size = 5
        self.discount_factor = 0.9

        # whether current value is inherited from previous value
        self.tha_inherited = False

    def next(self):
        # 对信号进行判断和修改
        # 1. 当 trendhold 保持不变的时候，通过 turning point 和 active buy sell 来判断是否需要进行调整
        # 2. 当 trendhold 变化的时候，如果无明显 turning point 和 active buy sell 的支持，则通过 trend 来判断是否赞成这一次的 trendhold 调整。否则以 turning point 和 active buy sell 为主

        cur_bar_time_str = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")
        support_tp = sum(x * self.discount_factor ** i for i, x in enumerate(reversed(self.tp.get(size=self.window_size))))
        support_active_buy_sell = sum(x * self.discount_factor ** i for i, x in enumerate(reversed(self.abs.get(size=self.window_size))))
        support_trend = sum(x * self.discount_factor ** i for i, x in enumerate(reversed(self.trend.get(size=self.window_size))))

        trendhold_now = self.trendhold[0]
        trendhold_adjust = self.trendhold_last

        # support priority sequence
        # 1. combination of support_tp and support_active_buy_sell
        # 2. support_trend
        # 3. rsi window cross permits
        # 4. permit shift only when target value not conficting with trend_warrant 
        if trendhold_now == self.trendhold_last:
            if support_tp > 0 and support_active_buy_sell > 0:
                trendhold_adjust = TrendHoldAdjust.BULLISH
            elif support_tp < 0 and support_active_buy_sell < 0:
                trendhold_adjust = TrendHoldAdjust.BEARISH
        else:
            if support_tp > 0 and support_active_buy_sell > 0:
                trendhold_adjust = TrendHoldAdjust.BULLISH
            elif support_tp < 0 and support_active_buy_sell < 0:
                trendhold_adjust = TrendHoldAdjust.BEARISH
            elif support_trend > 0:
                trendhold_adjust = TrendHoldAdjust.BULLISH
            else:
                trendhold_adjust = TrendHoldAdjust.BEARISH

        if self.trendhold_last == TrendHoldAdjust.BEARISH and trendhold_adjust == TrendHoldAdjust.BULLISH:
            if self.backpeek_crossover() != 1:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, cur_bar_time_str: {cur_bar_time_str}, not golden RSI crossover({self.crossover[0]}), keep BEARISH")
                trendhold_adjust = self.trendhold_last
                self.tha_inherited = True
        elif self.trendhold_last == TrendHoldAdjust.BULLISH and trendhold_adjust == TrendHoldAdjust.BEARISH:
            if self.backpeek_crossover() != -1:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, cur_bar_time_str: {cur_bar_time_str}, not dead RSI crossover({self.crossover[0]}), keep BULLISH")
                trendhold_adjust = self.trendhold_last
                self.tha_inherited = True
        elif trendhold_adjust != TrendHoldAdjust.NA and trendhold_adjust == self.trendhold_last:
            if self.tha_inherited and trendhold_adjust == TrendHoldAdjust.BULLISH and self.crossover[0] == -1:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, cur_bar_time_str: {cur_bar_time_str}, inherited BULLISH until dead RSI crossover({self.crossover[0]}), reset to original TrendHold")
                trendhold_adjust = self.trendhold[0]
                self.tha_inherited = False
            elif self.tha_inherited and trendhold_adjust == TrendHoldAdjust.BEARISH and self.crossover[0] == 1:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, cur_bar_time_str: {cur_bar_time_str}, inherited BEARISH until gold RSI crossover({self.crossover[0]}), reset to original TrendHold")
                trendhold_adjust = self.trendhold[0]
                self.tha_inherited = False

        # Never allow TrendHold to be the very opposite of TrendWarrant. Otherwise, inherit TrendHold from previous value
        if trendhold_adjust != TrendHoldAdjust.NA and trendhold_adjust == -1 * self.trend_warrant[0]:
            trendhold_adjust = self.trendhold[0]

        self.lines.tha[0] = trendhold_adjust
        self.trendhold_last = trendhold_adjust

        if self.p.debug:
            stdout_log(f"{self.__class__.__name__}, {cur_bar_time_str}, Adjusted TrendHold: {trendhold_adjust}")

    def backpeek_crossover(self):
        rsi_delta_max = 0.0
        for i in range(0, len(self.fast_rsi)):
            if abs(self.fast_rsi[-i] - self.slow_rsi[-i]) > rsi_delta_max:
                rsi_delta_max = abs(self.fast_rsi[-i] - self.slow_rsi[-i])

        if self.p.debug:
            stdout_log(f"{self.__class__.__name__}, rsi_delta_max: {rsi_delta_max}")

        ret = 0
        for i in range(0, self.p.crossover_backpeek_size + 1):
            # the diff between fast_rsi and slow_rsi should be large enough
            if self.crossover[-i] != 0 and abs(self.fast_rsi[-i] - self.slow_rsi[-i]) > (rsi_delta_max * 2 / 3.0):
                ret = self.crossover[-i]
                break
        return ret