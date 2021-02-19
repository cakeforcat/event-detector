from readcsv import DataReader
import matplotlib.pyplot as plt
import pandas as pd


def detect_event(diff, max_diff, min_diff):
    if diff > (0.1*max_diff) or diff < (0.1*min_diff):
        return 0
    else:
        return None


class PreProcessor(DataReader):
    def __init__(self, file_name):
        DataReader.__init__(self, file_name)

    def read_and_process(self, data_series, data_range, chunk_size):
        df = None
        df_diffed = None
        with self.read_in_chunks(data_series, data_range, chunk_size) as reader:
            continuity_cache = None
            processed_rows = 0
            for chunk in reader:
                chunk.set_index("Time", drop=True, inplace=True)
                chunk = pd.concat([continuity_cache, chunk])
                continuity_cache = chunk.tail(1)
                chunk_diffed = chunk.diff(periods=1)
                chunk.drop(chunk.index[0], inplace=True)
                chunk_diffed.drop(chunk.index[0], inplace=True)
                df_diffed = pd.concat([df_diffed, chunk_diffed])
                df = pd.concat([df, chunk])
                processed_rows = processed_rows + chunk_size
                percentage = (processed_rows*100)/(data_range[1]-data_range[0])
                print("processed: {:.2f}%".format(percentage))
        return df, df_diffed


def example():
    processor = PreProcessor("Signature Database dataset.csv")
    df, df_diffed = processor.read_and_process(['Kettle'], [100, 30000], 1000)
    print(df_diffed)
    print(df)
    print(df.max()['Kettle'], df.min()['Kettle'])
    df_diffed["Event"] = df_diffed.apply(lambda x: detect_event(x['Kettle'], df_diffed.max()['Kettle'],
                                                                df_diffed.min()['Kettle']), axis=1)
    ax = df.plot()
    df_diffed.reset_index().plot( x="Time", y='Event', kind='scatter', ax=ax, c='orange', s=200)
    plt.gcf().autofmt_xdate(rotation=20)
    plt.show()

example()

table = pandas.read_csv(r'Signature Database dataset.csv', 
            index_col='Time', 
            parse_dates=['Unix'], 
            header=0, 
            names=['Time', 'Unix', 'Aggregate', 'Fridge Freezer', \
                  'Tumble dryer', 'Washing Machine', 'Dishwasher', \
                      'Computer', 'Television', 'Microwave', 'Kettle', \
                          'Toaster', 'Issues'])
print(table)
