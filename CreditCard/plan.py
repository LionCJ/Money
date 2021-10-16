# -*- coding: utf-8 -*-
"""
作用：定制刷卡计划
具体实施：
1.计算当天起至月底剩余天数；
2.计算银行免息期；
3.随机安排每天的刷卡银行、刷卡金额；
4.计算出每个月刷卡金额
"""
import random
import calendar
import datetime
import pandas as pd


class PayCard:
    def __init__(self):
        self.zg = {
            "name": "中国银行",
            "account_date": 24,
            "final_repayment_date": 14
        }
        self.pa = {
            "name": "平安银行",
            "account_date": 3,
            "final_repayment_date": 21
        }
        self.gd = {
            "name": "光大银行",
            "account_date": 16,
            "final_repayment_date": 4
        }
        self.pf = {
            "name": "浦发银行",
            "account_date": 6,
            "final_repayment_date": 26
        }
        self.gf = {
            "name": "广发银行",
            "account_date": 14,
            "final_repayment_date": 3
        }
        self.zx = {
            "name": "中信银行",
            "account_date": 1,
            "final_repayment_date": 20
        }
        self.hf = {
            "name": "汇丰银行",
            "account_date": 25,
            "final_repayment_date": 15
        }
        self.js = {
            "name": "建设银行",
            "account_date": 25,
            "final_repayment_date": 14
        }
        self.zs = {
            "name": "招商银行",
            "account_date": 8,
            "final_repayment_date": 26
        }
        self.jt = {
            "name": "交通银行",
            "account_date": 19,
            "final_repayment_date": 13
        }
        self.banks_info_list = [self.zg, self.pa, self.gd, self.pf, self.gf, self.zx, self.hf, self.js, self.zs,
                                self.jt]

    @staticmethod
    def get_date_list(start, end):
        """返回日期列表"""
        # 生成日期列表
        dates_list = pd.date_range(start, end).strftime("%Y-%m-%d").to_list()
        return dates_list

    def get_days_remaining(self):
        """返回剩余天数"""
        # 当天日期
        today = datetime.date.today()
        # today = datetime.datetime.strptime("2021-06-15", "%Y-%m-%d").date()

        # 本月最后一天
        now_date = datetime.datetime.now()
        this_month_end = datetime.date(now_date.year, now_date.month,
                                       calendar.monthrange(now_date.year, now_date.month)[1])

        # 调用返回日期列表函数，返回日期列表
        dates_list = self.get_date_list(today, this_month_end)
        return dates_list

    def get_interest_free_period(self, bank_dist):
        """计算银行免息期"""
        account_date = bank_dist["account_date"]
        final_repayment_date = bank_dist["final_repayment_date"]
        # 如果最后还款日 小于 出账日，则代表是跨月计算
        if final_repayment_date < account_date:
            now_date = datetime.datetime.now()
            # 出帐日
            account_date_result = datetime.date(now_date.year, now_date.month, account_date)
            # 最后还款日
            final_repayment_date_result = datetime.date(now_date.year, now_date.month + 1, final_repayment_date)
            # print(account_date_result, final_repayment_date_result)
        else:
            # 否则就是当月计算
            now_date = datetime.datetime.now()
            # 出帐日
            account_date_result = datetime.date(now_date.year, now_date.month, account_date)
            # 最后还款日
            final_repayment_date_result = datetime.date(now_date.year, now_date.month, final_repayment_date)
        # 调用返回日期列表函数，返回日期列表
        date_list = self.get_date_list(account_date_result, final_repayment_date_result)
        return date_list

    def get_banks_list(self):
        """免息期对比，返回刷卡银行列表"""
        # 返回本月剩余日期列表
        days_list = self.get_days_remaining()
        # 返回银行账单信息列表
        banks_info_list = self.banks_info_list
        new_banks_list = []
        new_banks_name = {}
        # 遍历当天到月底日期
        for day in days_list:
            # 遍历银行账单信息列表
            for bank_info in banks_info_list:
                bank_name = bank_info["name"]
                # 返回该银行免息期日期列表
                bank_date_list = self.get_interest_free_period(bank_info)
                # 如果当天日期在免息期内，银行名字增加进列表
                if day in bank_date_list:
                    new_banks_list.append(bank_name)
                    new_banks_name[day] = new_banks_list
            # 每个日期清空一次列表
            new_banks_list = []
        return new_banks_name

    def run(self):
        # 初始化
        amount_sum, interest_sum = 0.0, 0.0
        bank_info = {}
        free_list = self.get_banks_list()
        for day, banks_list in free_list.items():
            print("\n" + day)
            # print(banks_list)
            # 从免息期银行中随机抽取1-3个银行
            if len(banks_list) > 3:
                bank_num = 3
            else:
                bank_num = len(banks_list)
            bank_result = random.sample(banks_list, random.randint(1, bank_num))

            # print(bank_result)
            for bank in bank_result:
                bank_info[bank] = {"amount": round(random.uniform(200, 2500), -1)}
                amount = round(bank_info[bank]["amount"], 0)
                interest = {"interest": round(amount - amount * 0.994, 2)}
                bank_info[bank].update(interest)
                # 计算总刷卡金额，总利息
                amount_sum = amount_sum + bank_info[bank]["amount"]
                interest_sum = interest_sum + bank_info[bank]["interest"]
            for k, v in bank_info.items():
                print("【{}】 刷卡金额：{}  利息：{}  实际到账：{}".format(k, bank_info[k]["amount"],
                                                                 bank_info[k]["interest"],
                                                                 bank_info[k]["amount"] - bank_info[k]["interest"]))
            bank_info = {}
            bak_text = ""
            for bak_bank in banks_list:
                bak_text = bak_text + str(bak_bank) + "  "
            print("免息银行列表：" + bak_text)

        text = "\n 总刷卡金额为：{} ，总利息为：{} ，总实际到账：{}".format(amount_sum, round(interest_sum,2), amount_sum - interest_sum)
        return text

    def test(self):
        return self.run()


if __name__ == '__main__':
    P = PayCard()
    print(P.test())
