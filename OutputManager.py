import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt


class FileManager:
    def __init__(self, data_series):
        self.name = data_series
        self.path = r"events\{0}\{1}".format(self.name, datetime.datetime.now().strftime("%d.%m.%Y %H;%M;%S"))

    def get_full_path(self):
        return r"{0}\{1}".format(os.getcwd(), self.path)

    def get_path(self):
        return self.path

    def setup_dir(self):
        if not os.path.exists(self.get_path()):
            os.makedirs(self.get_full_path())
        else:
            print("path exists")

    def save_csv(self, data):
        df = data
        df.to_csv(r'{0}\{1}.csv'.format(self.path, self.name), index=False)


class Visualizer:
    def __init__(self, raw_data, events):
        self.series = raw_data
        self.events = events
        self.ax = None

    def make_plot(self):
        if self.events is None:
            return
        else:
            self.ax = self.series.plot()
            self.events.reset_index().rename(columns={"index": "value"}).plot(x="Start", y="value", kind='scatter',
                                                                              ax=self.ax, marker=5, c='green', s=200)
            self.events.reset_index().rename(columns={"index": "value"}).plot(x="End", y="value", kind='scatter',
                                                                              ax=self.ax, marker=4, c='orange', s=200,
                                                                              xlabel='Time', ylabel='Power', rot=20)
            pd.plotting.table(self.ax, self.events.round({'Energy (kWh)': 3}), loc='top', cellLoc='center')

    def save_plot(self, file_name):
        if self.events is None:
            return
        else:
            plt.savefig(file_name)

    def show_plot(self):
        if self.events is None:
            return
        else:
            plt.show()
