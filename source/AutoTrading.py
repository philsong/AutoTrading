import pandas as pd
import sys

pd.options.display.max_rows = 999
pd.set_option('expand_frame_repr', False)
import datetime

from PyQt5.QtWidgets import QApplication
from interface.widgets import MainWindow

from source.dataManager.manager import DataManager
from source.strategies.manager import StrategiesManager
from source.money.account      import AccountManager
from source.order.manager      import OrderManager
from source.money.pnl import pnlCalculator

class AutoTradeManager:

    def __init__(self):
        self.app        = QApplication(sys.argv)
        self.data       = DataManager()
        self.strategies = StrategiesManager()
        self.account    = AccountManager(self.strategies.strategiesPool)
        self.orderAgent = OrderManager()
        self.mainWindow = MainWindow(self)

        #self.run(pd.Timestamp("2015-12-31 16:00:00"), pd.Timestamp("2016-02-26 16:00:00"), "HSI")
        sys.exit(self.app.exec_())

    # reset system
    def resetSystem(self, capital, margin):

        # reset account
        self.account.setAccount(self.strategies.strategiesPool, capital, margin)

    def run(self, start, end, security, capital=100000000.0, margin=0.3):

        # reset system before run
        self.resetSystem(capital, margin)

        # generate trading signals for specific security
        dataSet = self.data.getCSVData()
        signals = self.strategies.monitorMarket(dataSet)
        self.orderAgent.handleSignals(self.account, signals)

        # print history
        self.account.printTradeHistory()
        self.report = pnlCalculator(self.account.queryCapital("MACD"), self.account.queryTradeHistory())
        self.report.run()

        # query position
        # print self.account.queryPosition('HSI', 'Long', 'ACOscillator')

    def launchTechnicalAnalysis(self, capital, securityCode, investmentStrategies, startTime, endTime, tradeStrategy, positionManagement):

        dataSet = self.data.getCSVData(securityCode)
        signals = self.strategies.monitorMarket(dataSet)
        self.orderAgent.handleSignals(self.account, signals)
        
        # print history
        self.account.printTradeHistory()
        self.report = pnlCalculator(self.account.queryCapital("MACD"), self.account.queryTradeHistory())
        self.report.run()

if __name__ == "__main__":

    atm = AutoTradeManager()
    atm.run(pd.Timestamp("2015-12-31 16:00:00"), pd.Timestamp("2016-02-26 16:00:00"), "HSI")
