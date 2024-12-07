""" Broker Client
"""

from dataclasses import dataclass
import logging
import warnings
from typing import Any, Mapping, Optional
from datetime import datetime
import requests
from tqdm.auto import tqdm
import pandas as pd
from redis import Redis
from retry import retry
from lib import TIMEFORMAT_TIME, get_db, seconds_between

warnings.filterwarnings('ignore')
_logger = logging.getLogger(__name__)


@dataclass
class Th3N1c3Cl13ntConfig:
    """Configuration for th3n1c3l1b"""
    broker_api_url: str
    pg_conn_url: str
    redis_server_host: str
    redis_server_port: int
    tax_factor: Optional[float] = .002

    def __post_init__(self):
        _logger.debug('Initializing th3n1c3l1b')
        self.pg_engine = get_db(self.pg_conn_url)
        self.redis = Redis(
            host=self.redis_server_host,
            port=self.redis_server_port
        )
        _logger.debug('Initialized th3n1c3l1b')


@dataclass
class OrderRequest:
    """Order Request"""
    exchange_code: str
    stock_code: str
    product_type: str
    action: str
    quantity: int
    right: str
    expiry: str
    strike_price: float
    validity: Optional[str] = 'IOC'
    order_type: Optional[str] = 'MARKET'
    price: Optional[float] = None
    stop_loss: Optional[float] = None


@dataclass
class Position:
    """Position"""
    underlying: str
    strike_price: float
    quantity: int
    right: str
    product_type: str
    exchange_code: str
    expiry_date: str
    stop_loss: Optional[float] = None
    price: Optional[float] = None

    @property
    def expiry(self):
        """Expiry"""
        if self.expiry_date is None:
            return None
        return datetime.strptime(
            self.expiry_date,
            '%d-%b-%Y'
        ).strftime('%Y%m%d')


@dataclass
class HistorySegmentRequest:
    """History Segment Request"""
    stock_code: str
    start_time: datetime
    end_time: datetime
    exchange_code: Optional[str] = "NSE"
    product_type: Optional[str] = "cash"
    strike_price: Optional[int] = None
    right: str = None
    expiry: str = ''
    expiry_day: int = 0
    interval: str = '1second'


class Th3N1c3Cl13nt:
    """Client for th3n1c3l1b"""

    def __init__(
            self,
            config: Th3N1c3Cl13ntConfig,
    ) -> None:
        self._config = config

    def refresh_master(self,) -> Mapping[str, Any]:
        """Refresh master
        Returns:
            Mapping[str, Any]: Response from API
        """
        return requests.get(
            f'{self._config.broker_api_url}/refresh_security_master',
            timeout=600
        ).json()

    def sql(self, query: str) -> pd.DataFrame:
        """SQL Query
        Args:
            query (str): SQL Query
        Returns:
            pd.DataFrame: Dataframe
        """
        _logger.debug('Executing SQL Query: %s', query)
        return pd.read_sql(query, self._config.pg_engine)

    def get_exchange_name(self, code: str) -> str:
        """Get Exchange Name
        Args:
            code (str): ICICI Specific Code
        Returns:
            str: Exchange Name
        """
        _logger.debug('Getting Exchange Name for %s', code)
        df = pd.read_sql('equity_master', self._config.pg_engine)

        return df[df['shortname'].str.contains(code)]

    def get_short_name(self, code: str) -> pd.DataFrame:
        """Get exchange name

        Args:
            code (str):

        Returns:
            pd.DataFrame: _description_
        """
        _logger.debug('Getting Short Name for %s', code)
        df = pd.read_sql('equity_master', self._config.pg_engine)

        return df[df['exchangecode'].str.contains(code)]

    def get_option_chain(
            self,
            stock_code: str,
            right: str,
            expiry: str,
    ) -> pd.DataFrame:
        """ Get Option Chain

        Args:
            stock_code (str): Stock Code
            right (str): Right
            expiry (str): Expiry in YYYYMMDD

        Raises:
            ValueError: Error from API

        Returns:
            pd.DataFrame: Option Chain
        """
        endpoint = '/'.join(
            [
                self._config.broker_api_url,
                'option_chain',
                stock_code,
                right,
                expiry
            ]
        )

        resp = requests.get(
            endpoint,
            timeout=600
        ).json()
        if resp.get('Error') is not None:
            _logger.error(resp['Error'], exc_info=True)
            raise ValueError(resp['Error'])
        return pd.DataFrame(resp['Success'])

    def place_order(
        self,
        order: OrderRequest,
    ) -> dict:
        """Place an order.

        Args:
            client (BreezeConnect): BreezeConnect object.
            action (str): Buy or Sell.
            order (dict): Order details.

        Returns:
            dict: Response from ICICI Direct.
        """
        order_request: Mapping[str, Any] = dict(
            exchange_code=order.exchange_code,
            stock_code=order.stock_code,
            product=order.product_type.lower(),
            action=order.action.upper(),
            order_type=order.order_type,
            quantity=order.quantity,
            right=order.right,
            expiry=order.expiry,
            strike_price=order.strike_price,
            validity=order.validity,
        )

        if order.get('price'):
            order_request['price'] = order['price']

        url = f'{self._config.broker_api_url}/place_order'

        _logger.info('Placing Order: %s', order_request)

        response = requests.post(
            url,
            json=order_request,
            timeout=600
        ).json()
        _logger.info('Place Order Response: %s', response)

        return response

    def portfolio(self):
        """Get Portfolio"""
        url = f'{self._config.broker_api_url}/portfolio'
        response = requests.get(url, timeout=600).json()
        return pd.DataFrame(response) if len(response) else pd.DataFrame(
            columns=[
                'stock_code',
                'right',
                'strike_price',
                'exchange_code',
                'product_type',
                'quantity',
                'ltp',
                'average_price',
            ]
        )

    def get_trades(
            self,
            start_date: str,
            end_date: str,
            stock_code: str,
            exchange_code: str
    ):
        """Get Trades
        Args:
            start_date (str): Start Date
            end_date (str): End Date
            stock_code (str): Stock Code
            exchange_code (str): Exchange Code
        Returns:
            pd.DataFrame: Trades
        """

        def _calculate_balance(x):
            x['Balance'] = float(x['quantity']) * float(
                x['average_cost']
            ) * (-1 if x['action'] == 'Buy' else 1)
            return x

        url_path = '/'.join([
            self._config.broker_api_url,
            'trades',
            exchange_code,
            stock_code,
            start_date,
            end_date,
        ])
        resp = requests.get(
            f'{url_path}?product_type=options',
            timeout=600
        ).json()

        if 'Success' in resp:
            trades = resp['Success']
            return pd.DataFrame(trades).apply(
                _calculate_balance,
                axis=1
            )

        _logger.error('Error in fetching trades: %s', resp)
        return pd.DataFrame()

    def cancel_order(
            self,
            order_id: str,
            exchange_code: str
    ):
        """Cancel order

        Args:
            order_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        url = '/'.join(
            [
                self._config.broker_api_url,
                'cancel_order',
                exchange_code,
                order_id
            ]
        )
        _logger.info('Cancelling Order: %s', order_id)
        resp = requests.post(url, timeout=600).json()
        _logger.info('Cancel Order Response: %s', resp)
        return resp

    def order_list(self, order_date: str) -> pd.DataFrame:
        """Order List

        Args:
            order_date (str): Order Date

        Returns:
            pd.DataFrame: Order List
        """
        url = '/'.join([
            self._config.broker_api_url,
            'order_list',
            'NFO',
            order_date,
            order_date
        ])
        resp = requests.get(
            url,
            timeout=600
        ).json()

        if 'Error' in resp:
            _logger.error('Error in fetching order list: %s', resp)
            return pd.DataFrame()

        return pd.DataFrame(resp['Success'])

    def square_off(
            self,
            position: Position
    ) -> Mapping[str, Any]:
        """Square off position

        Args:
            position (Position): Position

        Returns:
            Mapping[str, Any]: Response from API
        """
        order = {
            'stock_code': position.underlying,
            'strike_price': str(int(position.strike_price)),
            'quantity': int(position.quantity),  # min(q, 1800),
            'right': position.right,
            'product_type': position.product_type.lower(),
            'exchange_code': position.exchange_code,
            'expiry': position.expiry,
            'action': 'sell',
        }

        if position.stop_loss is not None:
            order['stop_loss'] = position.stop_loss
            order['order_type'] = 'stoploss'
            order['validity'] = 'day'
            order['price'] = position.price

        url = f'{self._config.broker_api_url}/square_off'

        _logger.info('Square Off: %s', order)
        response = requests.post(url, json=order, timeout=600).json()
        _logger.info('Square Off Response: %s', response)

        return response

    def modify_order(
            self,
            order_id: str,
            position: Position,
            stop_loss: float,
    ) -> Mapping[str, Any]:
        """Modify Order

        Args:
            order_id (str): Order ID
            position (Position): Position
            stop_loss (float): Stop Loss

        Returns:
            Mapping[str, Any]: Response from API
        """

        _logger.info('Modifying Order: %s', order_id)

        position.stop_loss = (stop_loss//.05)*.05
        position.price = (stop_loss//.05)*.05
        resp = self.cancel_order(
            order_id,
            position.exchange_code
        )
        if resp['Success'] is None:
            return resp

        resp = self.square_off(position)
        return resp

    @retry(tries=3, delay=1, backoff=2)
    def get_history_segment(
        self,
        request: HistorySegmentRequest,
    ):
        """Get history segment

        Args:
            request (HistorySegmentRequest): History Segment Request

        Returns:
            pd.DataFrame: History Segment
        """
        query_options = {
            "symbol": request.stock_code,
            "exchange_code": request.exchange_code,
            "product_type": request.product_type,
            "strike_price": request.strike_price,
            "right": request.right,
            "expiry": request.expiry,
            "weekday": request.expiry_day,
            "interval": request.interval,
        }
        query_str = "&".join(
            [
                f"{k}={v}"
                for k, v in query_options.items()
                if v
            ]
        )

        curr_min_time = request.end_time

        resp = {'Error': None, 'Status': 200, 'Success': ['X']}

        dfs = []

        init_seconds = seconds_between(
            request.start_time,
            request.end_time
        )

        with tqdm(
            total=init_seconds,
            desc=f'history: {request.stock_code}, {request.interval}',
            leave=False,
            dynamic_ncols=True,
            smoothing=0.01,
        ) as pbar:

            while len(resp['Success']) > 0:
                path_url = '/'.join(
                    [
                        self._config.broker_api_url,
                        'history_segment',
                        request.stock_code,
                        request.start_time.strftime(TIMEFORMAT_TIME),
                        request.curr_min_time.strftime(TIMEFORMAT_TIME),
                    ]
                )

                endpoint = f'{path_url}?{query_str}'
                resp = requests.get(endpoint, timeout=600).json()

                if resp.get('Error') is not None:
                    raise ValueError(resp['Error'])

                _df = pd.DataFrame(resp['Success'])
                dfs.append(_df)
                _df.datetime = pd.to_datetime(_df.datetime)
                curr_second_progress = seconds_between(
                    _df.datetime.min(),
                    curr_min_time,
                )
                curr_min_time = _df.datetime.min()

                pbar.update(curr_second_progress)

                if len(resp['Success']) < 1000:
                    pbar.update(
                        seconds_between(
                            curr_min_time,
                            request.end_time,
                        )
                    )
                    pbar.set_description()
                    break

        return pd.concat(dfs)
