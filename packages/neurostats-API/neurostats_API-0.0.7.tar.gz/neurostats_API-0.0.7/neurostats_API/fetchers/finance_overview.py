from .base import StatsFetcher, StatsDateTime
import json
import pandas as pd
from ..utils import StatsDateTime, StatsProcessor
import importlib.resources as pkg_resources
import yaml


class FinanceOverviewFetcher(StatsFetcher):
    """
    對應iFa.ai -> 財務分析 -> 重要指標(finance_overview)
    """

    def __init__(self, ticker, db_client):
        super().__init__(ticker, db_client)

        self.target_fields = StatsProcessor.load_yaml("finance_overview_dict.yaml")
        self.inverse_dict = StatsProcessor.load_txt("seasonal_data_field_dict.txt", json_load=True)

    def prepare_query(self, target_year, target_season):

        pipeline = super().prepare_query()

        target_query = {
            "year": "$$target_season_data.year",
            "season": "$$target_season_data.season",
        }

        for key, target_sets in self.target_fields.items():
            try:
                small_target = target_sets['field']
                big_target = self.inverse_dict[
                    small_target]  # balance_sheet/profit_lose/cash_flow
                value_index = target_sets['value']  # "金額" or "%"

                target_query.update({
                    f"{key}":
                    f"$$target_season_data.{big_target}.{small_target}.{value_index}"
                })
            except Exception:
                continue

        pipeline.append({
            "$project": {
                "_id": 0,
                "ticker": 1,
                "company_name": 1,
                "seasonal_data": {
                    "$map": {
                        "input": {
                            "$filter": {
                                "input": "$seasonal_data",
                                "as": "season",
                                "cond": {
                                    "$and": [{
                                        "$eq": ["$$season.year", target_year]
                                    }, {
                                        "$eq":
                                        ["$$season.season", target_season]
                                    }]
                                }
                            }
                        },
                        "as": "target_season_data",
                        "in": target_query
                    }
                }
            }
        })

        return pipeline

    def collect_data(self, target_year, target_season):
        pipeline = self.prepare_query(target_year, target_season)

        fetched_data = self.collection.aggregate(pipeline)

        fetched_data = list(fetched_data)

        return fetched_data[0]

    def query_data(self):
        today = StatsDateTime.get_today()

        year = today.year - 1 if (today.season == 1) else today.year
        season = 4 if (today.season == 1) else today.season - 2
        fetched_data = self.collect_data(year, season)
        finance_dict = fetched_data['seasonal_data'][0]
        FinanceOverviewProcessor.process_all(finance_dict)
        fetched_data['seasonal_data'] = finance_dict
        return fetched_data


class FinanceOverviewProcessor(StatsProcessor):

    @classmethod
    def process_all(cls, finance_dict):
        methods = [
            cls.cal_EBIT,
            cls.cal_share_outstanding,
            cls.cal_fcf,
            cls.cal_revenue_per_share,
            cls.cal_gross_per_share,
            cls.cal_operating_income_per_share,
            cls.cal_operating_cash_flow_per_share,
            cls.fcf_per_share,
            cls.cal_roa, 
            cls.cal_roe,
            cls.cal_gross_over_asset,
            cls.cal_roce,
            cls.cal_gross_profit_marginal,
            cls.cal_operation_profit_rate,
            cls.cal_operating_cash_flow_profit_rate,
            cls.cal_dso,
            cls.cal_account_receive_over_revenue,
            cls.cal_dpo,
            cls.cal_inventories_cycle_ratio,
            cls.cal_dio,
            cls.cal_inventories_revenue_ratio,
            cls.cal_cash_of_conversion_cycle,
            cls.cal_asset_turnover,
            cls.cal_application_turnover,
            cls.cal_current_ratio,
            cls.cal_quick_ratio,
            cls.cal_debt_to_equity_ratio,
            cls.cal_net_debt_to_equity_ratio,
            cls.cal_interest_coverage_ratio,
            cls.cal_debt_to_operating_cash_flow,
            cls.cal_debt_to_free_cash_flow,
            cls.cal_cash_flow_ratio
        ]

        for method in methods:
            method(finance_dict)

    @classmethod
    def cal_EBIT(cls, finance_dict):
        """
        計算EBIT
        EBIT = 營業收入 - 營業成本 - 營業費用
        """
        try:
            finance_dict['EBIT'] = (finance_dict['revenue'] -
                                    finance_dict['operating_cost'] -
                                    finance_dict['operating_expenses'])
        except (KeyError, TypeError) as e:
            finance_dict['EBIT'] = None
            print(f"Error calculating EBIT: {e}")

    @classmethod
    def cal_fcf(cls, finance_dict):
        """
        計算自由現金流(FCF):
        自由現金流 =  營業現金流 + 投資現金流
        """
        try:
            finance_dict["fcf"] = (finance_dict["operating_cash_flow"] +
                                   finance_dict["financing_cash_flow"])
        except Exception as e:
            finance_dict['fcf'] = None
            print(f"Error calculating FCF: {e}")

    @classmethod
    def cal_share_outstanding(cls, finance_dict):
        """
        計算流通股數
        流通股數 = 本期淨利 ÷ 基本每股盈餘
        """
        try:
            finance_dict["share_outstanding"] = (finance_dict['net_income'] /
                                                 finance_dict['eps'])
        except KeyError as e:
            finance_dict['share_outstanding'] = None
            print(f"share_outstanding failed because of {str(e)}")

    @classmethod
    def cal_revenue_per_share(cls, finance_dict):
        """
        計算每股營收
        每股營收 = 營業收入 / 在外流通股數
        """
        try:
            finance_dict['revenue_per_share'] = (
                finance_dict['revenue'] / finance_dict['share_outstanding'])
        except KeyError as e:
            finance_dict['revenue_per_share'] = None
            print(f"revenue_per_share failed because of {str(e)}")

    @classmethod
    def cal_gross_per_share(cls, finance_dict):
        """
        計算每股毛利
        = （當期營業毛利）÷（當期在外流通股數）
        """

        try:
            finance_dict['gross_per_share'] = (
                finance_dict['gross_profit'] /
                finance_dict['share_outstanding'])
        except KeyError as e:
            finance_dict['gross_per_share'] = None
            print(f"gross_per_share failed because of {str(e)}")

    @classmethod
    def cal_operating_income_per_share(cls, finance_dict):
        """
        計算每股營業利益
        每股營業利益= （當期營業利益）÷（當期在外流通股數）
        """
        try:
            finance_dict['operating_income_per_share'] = (
                finance_dict['operating_income'] /
                finance_dict['share_outstanding'])
        except KeyError as e:
            finance_dict['operating_income_per_share'] = None
            print(f"operating_income_per_share failed because of {str(e)}")

    @classmethod
    def cal_operating_cash_flow_per_share(cls, finance_dict):
        """
        計算每股營業現金流
        = (當期營業現金流) ÷（當期在外流通股數）
        """
        try:
            finance_dict["operating_cash_flow_per_share"] = (
                finance_dict["operating_cash_flow"] /
                finance_dict['share_outstanding'])
        except KeyError as e:
            finance_dict['operating_cash_flow_per_share'] = None
            print(f'operating_cash_flow_per_share because of {str(e)}')

    @classmethod
    def fcf_per_share(cls, finance_dict):
        """
        計算每股自由現金流
        每股自由現金流 = (當期自由現金流) ÷（當期在外流通股數）
        """
        try:
            finance_dict['fcf_per_share'] = (finance_dict['fcf'] /
                                             finance_dict['share_outstanding'])
        except KeyError as e:
            finance_dict['fcf_per_share'] = None
            print(f"fcf_per_share failed because of {str(e)}")

# 盈利能力

    @classmethod
    def cal_roa(cls, finance_dict):
        """
        計算資產報酬率(ROA)
        ROA = [ 本期淨利 + 利息費用 × (1-有效稅率) ] ÷（資產總額）
        """
        finance_dict["roa"] = (
            finance_dict['net_income'] + finance_dict['interest'] +
            (1 * 0.1)  # 有效稅率需要改，這裡先設0.1
        ) / finance_dict['inventories']

    @classmethod
    def cal_roe(cls, finance_dict):
        """
        計算股東權益報酬率(ROE)
        ROE = (本期淨利) ÷（權益總額）
        """
        finance_dict['roe'] = (finance_dict['net_income'] /
                               finance_dict['equity'])

    @classmethod
    def cal_gross_over_asset(cls, finance_dict):
        """
        計算營業毛利/總資產
        """
        finance_dict['gross_over_asset'] = (finance_dict['gross_profit'] /
                                            finance_dict['total_asset'])

    @classmethod
    def cal_roce(cls, finance_dict):
        """
        計算資本運用報酬率(ROCE):
        ROCE = (稅前淨利＋利息費用) / (資產總額－流動負債)
        """
        try:
            finance_dict['roce'] = (
                (finance_dict['net_income_before_tax'] +
                 finance_dict['interest']) /
                (finance_dict['asset'] - finance_dict['current_liabilities']))
        except KeyError as e:
            finance_dict['roce'] = None
            print(f"ROCE failed because of {str(e)}")

    @classmethod
    def cal_gross_profit_marginal(cls, finance_dict):
        """
        計算營業毛利率(gross profit margin)
        營業毛利率 = 營業毛利 ÷ 營業收入
        """
        try:
            finance_dict['gross_profit_margin'] = (
                finance_dict['gross_profit'] / finance_dict['revenue'])
        except:
            finance_dict['gross_profit_margin'] = None
            print(f"gross_profit_margin failed because of {str(e)}")

    @classmethod
    def cal_operation_profit_rate(cls, finance_dict):
        """
        計算營業利益率
        營業利益率 = ( 營業收入－營業成本－營業費用）÷ 營業收入
        """
        try:
            finance_dict["operation_profit_rate"] = (
                finance_dict['revenue'] - finance_dict['operating_cost'] -
                finance_dict['operating_price']) / finance_dict['revenue']
        except KeyError as e:
            finance_dict["operation_profit_rate"] = None
            print(f"operation_profit failed because of {str(e)}")

    @classmethod
    def cal_operating_cash_flow_profit_rate(cls, finance_dict):
        """
        計算營業現金流利潤率
        營業現金流利潤率 = 營業活動現金流 ÷ 營業收入
        """
        try:
            finance_dict["operating_cash_flow_profit_rate"] = (
                finance_dict["operating_cash_flow"] / finance_dict["revenue"])
        except KeyError:
            finance_dict["operating_cash_flow_profit_rate"] = None

            print(
                f"operating_cash_flow_profit_rate failed because of {str(e)}")


# 成長動能

    """
    前四個已經有了 revenue_YoY, gross_prof_YoY, operating_income_YoY, net_income_YoY:
    後四個在金流，還需要處理
    """
    # 營運指標

    @classmethod
    def cal_dso(cls, finance_dict):
        """
        計算應收帳款收現天數(DSO)
        DSO = 365 × (營業收入 ÷ 應收帳款平均餘額)
        """
        finance_dict['dso'] = (
            365 * (finance_dict['revenue'] / finance_dict['account_pay']))

    @classmethod
    def cal_account_receive_over_revenue(cls, finance_dict):
        """
        計算應收帳款佔營收比率
        = 應收帳款平均餘額 ÷ 營業收入
        """
        finance_dict["account_receive_over_revenue"] = (
            finance_dict['account_receive'] / finance_dict['revenue'])

    @classmethod
    def cal_dpo(cls, finance_dict):
        """
        計算應付帳款週轉天數
        DPO = 365天 ÷ (銷貨成本÷平均應付帳款)
        """
        finance_dict["dpo"] = (
            365 *
            (finance_dict['operating_cost'] / finance_dict['account_pay']))

    @classmethod
    def cal_inventories_cycle_ratio(cls, finance_dict):
        """
        計算存貨周轉率
        = 銷貨成本 ÷ 存貨
        """

        finance_dict["inventories_cycle_ratio"] = (
            finance_dict['operating_cost'] / finance_dict['inventories'])

    @classmethod
    def cal_dio(cls, finance_dict):
        """
        計算 存貨週轉天數
        DIO = 365天 ÷ (銷貨成本 ÷ 存貨)
        MUDA MUDA MUDA MUDA !!!
        """
        finance_dict["dio"] = (finance_dict["operating_cost"] /
                               finance_dict["inventories"])

    @classmethod
    def cal_inventories_revenue_ratio(cls, finance_dict):
        """
        計算存貨佔營收比率
        存貨佔營收比= 存貨 ÷ 營業收入
        """
        finance_dict["inventories_revenue_ratio"] = (
            finance_dict['inventories'] / finance_dict['revenue'])

    @classmethod
    def cal_cash_of_conversion_cycle(cls, finance_dict):
        """
        計算現金循環週期
        存貨週轉天數 + 應收帳款週轉天數 - 應付帳款週轉天數
        """
        finance_dict["cash_of_conversion_cycle"] = (finance_dict["dio"] +
                                                    finance_dict["dso"] -
                                                    finance_dict['dpo'])

    @classmethod
    def cal_asset_turnover(cls, finance_dict):
        finance_dict["asset_turnover"] = (finance_dict["revenue"] /
                                          finance_dict["inventories"])

    @classmethod
    def cal_application_turnover(cls, finance_dict):
        finance_dict['applcation_turnover'] = (finance_dict['revenue'] /
                                               finance_dict["application"])

    @classmethod
    def cal_current_ratio(cls, finance_dict):
        """
        計算流動比率 = 流動資產 / 流動負債
        """
        try:
            finance_dict['current_ratio'] = finance_dict[
                'current_assets'] / finance_dict['current_liabilities']
        except (KeyError, ZeroDivisionError, TypeError) as e:
            finance_dict['current_ratio'] = None
            print(f"Error calculating current ratio: {e}")

    @classmethod
    def cal_quick_ratio(cls, finance_dict):
        try:
            # 速動比率 = (流動資產 - 存貨) / 流動負債
            finance_dict['quick_ratio'] = (
                finance_dict['current_assets'] - finance_dict['inventories']
            ) / finance_dict['current_liabilities']
        except (KeyError, ZeroDivisionError, TypeError) as e:
            finance_dict['quick_ratio'] = None
            print(f"Error calculating quick ratio: {e}")

    @classmethod
    def cal_debt_to_equity_ratio(cls, finance_dict):
        try:
            # 負債權益比率 = 總負債 / 股東權益
            finance_dict['debt_to_equity_ratio'] = finance_dict[
                'total_liabilities'] / finance_dict['equity']
        except (KeyError, ZeroDivisionError, TypeError) as e:
            finance_dict['debt_to_equity_ratio'] = None
            print(f"Error calculating debt to equity ratio: {e}")

    @classmethod
    def cal_net_debt_to_equity_ratio(cls, finance_dict):
        try:
            # 淨負債權益比率 = (總負債 - 現金及約當現金) / 股東權益
            finance_dict['net_debt_to_equity_ratio'] = (
                finance_dict['total_liabilities'] -
                finance_dict['cash_and_cash_equivalents']
            ) / finance_dict['equity']
        except (KeyError, ZeroDivisionError, TypeError) as e:
            finance_dict['net_debt_to_equity_ratio'] = None
            print(f"Error calculating net debt to equity ratio: {e}")

    @classmethod
    def cal_interest_coverage_ratio(cls, finance_dict):
        try:
            # 利息保障倍數 = EBIT / 利息費用
            finance_dict['interest_coverage_ratio'] = finance_dict[
                'EBIT'] / finance_dict['interest_expense']
        except (KeyError, ZeroDivisionError, TypeError) as e:
            finance_dict['interest_coverage_ratio'] = None
            print(f"Error calculating interest coverage ratio: {e}")

    @classmethod
    def cal_debt_to_operating_cash_flow(cls, finance_dict):
        try:
            # 有息負債 / 營業活動現金流
            finance_dict['debt_to_operating_cash_flow'] = finance_dict[
                'interest_bearing_debt'] / finance_dict['operating_cash_flow']
        except (KeyError, ZeroDivisionError, TypeError) as e:
            finance_dict['debt_to_operating_cash_flow'] = None
            print(f"Error calculating debt to operating cash flow: {e}")

    @classmethod
    def cal_debt_to_free_cash_flow(cls, finance_dict):
        try:
            # 有息負債 / 自由現金流
            finance_dict['debt_to_free_cash_flow'] = finance_dict[
                'interest_bearing_debt'] / finance_dict['fcf']
        except (KeyError, ZeroDivisionError, TypeError) as e:
            finance_dict['debt_to_free_cash_flow'] = None
            print(f"Error calculating debt to free cash flow: {e}")

    @classmethod
    def cal_cash_flow_ratio(cls, finance_dict):
        try:
            # 現金流量比率 = 營業活動現金流 / 流動負債
            finance_dict['cash_flow_ratio'] = finance_dict[
                'operating_cash_flow'] / finance_dict['current_liabilities']
        except (KeyError, ZeroDivisionError, TypeError) as e:
            finance_dict['cash_flow_ratio'] = None
            print(f"Error calculating cash flow ratio: {e}")
