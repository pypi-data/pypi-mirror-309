import backtrader as bt
from ffquant.indicators.BaseIndicator import BaseIndicator
from ffquant.utils.Logger import stdout_log
from datetime import datetime
import pytz

__ALL__ = ['TrendHoldAdjust']

class TrendHoldAdjust(BaseIndicator):
    (BEARISH, NA, BULLISH) = (-1, 0, 1)

    lines = ('tha',)

    def __init__(self):
        super(TrendHoldAdjust, self).__init__()

        self.p.url = "http://192.168.25.127:8288/index/list"

        self.addminperiod(1)

    def handle_api_resp(self, item):
        result_time_str = datetime.fromtimestamp(item['openTime']/ 1000).strftime('%Y-%m-%d %H:%M:%S')
        self.cache[result_time_str] = float('-inf')
        if item.get('data', None) is not None:
            self.cache[result_time_str] = item['data']

        if self.p.debug:
            stdout_log(f"{self.__class__.__name__}, result_time_str: {result_time_str} {item.get('data', None)}")

    def determine_final_result(self):
        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_bar_time_str = current_bar_time.strftime('%Y-%m-%d %H:%M:%S')
        self.lines.tha[0] = self.cache[current_bar_time_str]

    def get_internal_key(self):
        return 'indicator_trend_hold_adjust'

    def prepare_params(self, start_time_str, end_time_str):
        params = {
            'type': self.get_internal_key(),
            'startTime' : start_time_str,
            'endTime' : end_time_str,
            'symbol' : self.p.symbol,
            'key_list': 'data'
        }

        return params