from readcsv import DataReader
import matplotlib.pyplot as plt
import pandas as pd
from EventDetector import EventDetector, Event, Point
from OutputManager import FileManager, Visualizer


# initialize - prompt the user for input, for now it's faster to hard code it for testing, later it'll be just input()
# may add more input like data range etc. for now it's coded below
#
#
#
#
file_name = "Signature Database dataset.csv"
data_series = "Fridge"
threshold = 15
chunk_size = 150
# Aggregate,Fridge,Freezer,Dryer,Washing Machine,Toaster,Computer,Television,Microwave,Kettle
#
#
#
#
# makes the output directory of it does not exist, stores the working path
output = FileManager(data_series)
output.setup_dir()
# start reading the file
with DataReader(file_name).read_in_chunks_to_series([data_series],
                                                    chunk_size=chunk_size,
                                                    data_range=[5000, 7000]) as reader:
    chunk_list = []
    events_list = []
    chunk_count = 0
    continuity_cache = [0, 0]
    optional_event_cache = Event()
    for chunk in reader:
        # detect the events, uses EventDetector.py
        detector = EventDetector(chunk, threshold)
        if optional_event_cache.is_only_start():
            detector.detect_events(continuity_cache, optional_event_cache)
        else:
            detector.detect_events(continuity_cache)

        events_list.append(detector.get_events())

        if detector.is_final_event_ongoing():
            optional_event_cache = detector.final_event

        # chunk_list.append(chunk)
        # visualize, prints the chunk count and outputs a plotter figure if the chunk contains events
        chunk_count += 1
        print("chunks: ", chunk_count)
        plotter = Visualizer(chunk, detector.get_events())
        plotter.make_plot()
        # fix for events spanning multiple chunks
        if detector.is_final_event_ongoing() and detector.get_events() is None:
            plotter.make_plot(force=True)

        plotter.save_plot(r'{0}\{1}'.format(output.get_path(), "chunk {0}.png".format(chunk_count)))
        plt.clf()

        continuity_cache = chunk.tail(1)    # don't touch this one

    # part of event detection
    if optional_event_cache.is_only_start():
        optional_event_cache.add_end(Point(continuity_cache).get_index())
        events_list.append(optional_event_cache.calc_to_dataframe())

# s = pd.concat(chunk_list)   # s is the loaded data as 1 pandas Series, if its needed for anything
events = pd.concat(events_list, ignore_index=True)
# events is a pandas DataFrame with all events, each row is an event, with the first column holding a start timestamp
# and the second column holding the end timestamp, see print(events)

print(events)
output.save_csv(events)  # saves the events in a neat .csv
