from readcsv import DataReader
import matplotlib.pyplot as plt
import pandas as pd

"""
WARNING OLD
DON'T USE - GO TO MAIN.PY
STORED FOR ARCHIVING
"""


def detect_event(diff, max_diff, min_diff):
    if diff > (0.1*max_diff) or diff < (0.1*min_diff):
        return 0
    else:
        return None


class PreProcessor(DataReader):
    def __init__(self, file_name):
        DataReader.__init__(self, file_name)

    def read_and_process(self, data_series, data_range, chunk_size):
        with self.read_in_chunks_to_series(data_series, data_range, chunk_size) as reader:
            continuity_cache = None
            processed_rows = 0
            chunk_diffed_list = []
            chunk_list = []
            for chunk in reader:
                chunk.set_index("Time", drop=True, inplace=True)
                chunk = pd.concat([continuity_cache, chunk])
                continuity_cache = chunk.tail(1)
                chunk_diffed = chunk.diff(periods=1)
                chunk.drop(chunk.index[0], inplace=True)
                chunk_diffed.drop(chunk.index[0], inplace=True)
                chunk_diffed_list.append(chunk_diffed)
                chunk_list.append(chunk)
                processed_rows = processed_rows + chunk_size
                percentage = (processed_rows*100)/(data_range[1]-data_range[0])
                print("processed: {:.2f}%".format(percentage))
            df = pd.concat(chunk_list)
            df_diffed = pd.concat(chunk_diffed_list)
        return df, df_diffed


def example():
    processor = PreProcessor("Signature Database dataset.csv")
    df, df_diffed = processor.read_and_process(['Kettle'], [1, 129250], 1000)
    print(df_diffed)
    print(df)
    print(df.std(), df.min(), df.max(), df.mean())
    s = df_diffed.mask(df_diffed < 1000)
    e = df_diffed.mask(df_diffed > -1000)
    df_diffed['Start'] = s
    df_diffed['End'] = e
    df_starts = df_diffed[df_diffed.Start > 0]
    print(df_starts)
    df_ends = df_diffed[df_diffed.End < 0]
    print(df_ends)
    ax = df.plot()
    df_diffed.reset_index().plot(x="Time", y='Start', kind='scatter', ax=ax, c='green', s=200)
    df_diffed.reset_index().plot(x="Time", y='End', kind='scatter', ax=ax, c='orange', s=200)
    plt.gcf().autofmt_xdate(rotation=20)
    plt.show()


def example2():
    processor = PreProcessor("Signature Database dataset.csv")
    df, df_diffed = processor.read_and_process(['Kettle'], [100, 5000000], 1000)
    print(df_diffed)
    print(df)
    print(df.max()['Kettle'], df.min()['Kettle'])


example()
