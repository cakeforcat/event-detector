import pandas as pd
import matplotlib.pyplot as plt


class DataReader:
    """
    # file_name is a str containing the file path for the csv file to open
    # data_series is a list containing the names of the columns to be included. for large files stick to around 2.
    # Don't include the "Time" column as it's internally included as an index
    # data_range is a list containing [start, end] numbers of the range of rows to be read. start and end are included
    # omitted, the whole range is read.
    """

    def __init__(self, file_name):
        self.file_name = file_name

    def read_to_dataframe(self, data_series, data_range=None):
        data_series.append("Time")
        if data_range is None:
            return pd.read_csv(self.file_name, usecols=data_series, index_col="Time",
                               parse_dates=True)
        else:
            number_of_rows = data_range[1] - data_range[0]
            skipped_range = range(1, data_range[0] - 1)
            return pd.read_csv(self.file_name, usecols=data_series, index_col="Time",
                               parse_dates=True, nrows=number_of_rows, skiprows=skipped_range)


# example use
reader = DataReader("Signature Database dataset.csv")
df = reader.read_to_dataframe(["Computer", "Kettle"], [30300, 30400])
# plot the example
plt.close("all")
plt.figure()
df.plot()
plt.legend(loc='best')
plt.show()
print(df)