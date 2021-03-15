from readcsv import DataReader
import matplotlib.pyplot as plt
import pandas as pd
from EventDetector import EventDetector, Event, Point

"""
main file of the project, this is the starting point where all other components are executed.
"""

# initialize - prompt the user for input, for now it's faster to hard code it for testing, later it'll be just input()
# may add more input like chunk size, data range etc. for now it's coded below
file_name = "Signature Database dataset.csv"
data_series = "Toaster"

# start reading the file
file = DataReader(file_name)
# this data_range for Toaster will show you 1 clean event
with file.read_in_chunks_to_series([data_series], data_range=[5320, 5395], chunk_size=1000) as reader:
    chunk_list = []
    events_list = []
    chunk_count = 0
    continuity_cache = [0, 0]
    optional_event_cache = Event()
    for chunk in reader:
        # detect the events, uses EventDetector.py
        detector = EventDetector(chunk)
        if optional_event_cache.is_only_start():
            detector.detect_events(continuity_cache, optional_event_cache)
        else:
            detector.detect_events(continuity_cache)

        events_list.append(detector.get_events())

        if detector.is_final_event_ongoing():
            optional_event_cache = detector.final_event
        # Process the chunk's data TODO
        # visualize, right now it just shows how many chunks have been read so far TODO
        chunk_list.append(chunk)
        chunk_count += 1
        print("chunks: ", chunk_count)
        continuity_cache = chunk.tail(1)    # don't touch this one

    # part of event detection
    if optional_event_cache.is_only_start():
        p = Point(continuity_cache)
        d = continuity_cache.reset_index().iloc[0, 0]
        optional_event_cache.add_end(p.get_index())
        events_list.append(optional_event_cache.to_dataframe())

s = pd.concat(chunk_list)   # s is the loaded data as 1 pandas Series
events = pd.concat(events_list)
# events is a pandas DataFrame with all events, each row is an event, with the first column holding a start timestamp
# and the second column holding the end timestamp, see print(events)

# some quick visualization, will make a figure with the data and events marked with a start and end dot
events.reset_index(inplace=True)
events.rename(columns={"index": "value"}, inplace=True)
print(s)
print(events)
ax = s.plot()
events.plot(x="Start", y="value", kind='scatter', ax=ax, c='green', s=200)
events.plot(x="End", y="value", kind='scatter', ax=ax, c='orange', s=200, xlabel='Time', ylabel='Power', rot=20)

plt.show()  # if you don't see anything use plt.savefig('fig.png')

# events.to_csv('filename.csv', index=False) use this to save the events in one csv if you need
