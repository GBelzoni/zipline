#
# Copyright 2013 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest

import datetime
import numpy as np
import pytz
import zipline.finance.risk as risk
from zipline.utils import factory

from zipline.finance.trading import SimulationParameters

import answer_key
ANSWER_KEY = answer_key.ANSWER_KEY


class TestRisk(unittest.TestCase):

    def setUp(self):
        start_date = datetime.datetime(
            year=2006,
            month=1,
            day=1,
            hour=0,
            minute=0,
            tzinfo=pytz.utc)
        end_date = datetime.datetime(
            year=2006, month=12, day=29, tzinfo=pytz.utc)

        self.sim_params = SimulationParameters(
            period_start=start_date,
            period_end=end_date
        )

        self.algo_returns_06 = factory.create_returns_from_list(
            answer_key.ALGORITHM_RETURNS.values,
            self.sim_params
        )

        self.cumulative_metrics_06 = risk.RiskMetricsCumulative(
            self.sim_params)

        for dt, returns in answer_key.RETURNS_DATA.iterrows():
            self.cumulative_metrics_06.update(dt,
                                              returns['Algorithm Returns'],
                                              returns['Benchmark Returns'])

    def test_algorithm_volatility_06(self):
        np.testing.assert_almost_equal(
            ANSWER_KEY.ALGORITHM_CUMULATIVE_VOLATILITY,
            self.cumulative_metrics_06.metrics.algorithm_volatility.values)

    def test_sharpe_06(self):
        for dt, value in answer_key.RISK_CUMULATIVE.sharpe.iterkv():
            np.testing.assert_almost_equal(
                value,
                self.cumulative_metrics_06.metrics.sharpe[dt],
                decimal=2,
                err_msg="Mismatch at %s" % (dt,))
