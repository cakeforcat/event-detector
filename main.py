from readcsv import DataReader
import matplotlib.pyplot as plt
import pandas as pd
from EventDetector import EventDetector, Event, Point
from OutputManager import FileManager, Visualizer


# initialization, user input
#
#
#
#
file_name = input("filename: ")
data_series = input("data series: ")
threshold = int(input("Event threshold: "))
chunk_size = int(input("reading chunk size: "))
specify_reading_mode = input("read the whole file? (Y/N): ")
if specify_reading_mode == 'N' or specify_reading_mode == 'n':
    start_row = int(input("Start reading at row no: "))
    end_row = int(input("Stop reading at row no: "))
    data_range = [start_row, end_row]
else:
    data_range = None

# in signature database.csv: Aggregate,Fridge,Freezer,Dryer,Washing Machine,Toaster,Computer,Television,Microwave,Kettle
#
#
#
#
# makes the output directory if it does not exist, stores the working path
output = FileManager(data_series)
output.setup_dir()
# start reading the file
with DataReader(file_name).read_in_chunks_to_series([data_series],
                                                    data_range=data_range,
                                                    chunk_size=chunk_size) as reader:
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

        # event continuity
        if detector.is_final_event_ongoing():
            optional_event_cache = detector.final_event

        chunk_list.append(chunk)
        # visualize, prints the chunk count and outputs a plotter figure if the chunk contains events
        chunk_count += 1
        print("chunks: ", chunk_count)
        plotter = Visualizer(chunk, detector.get_events())
        plotter.make_plot()
        # fix for events spanning multiple chunks
        if detector.is_final_event_ongoing() and detector.get_events() is None:
            plotter.make_plot(force=True)

        plotter.save_plot(r'{0}\chunk {1}.png'.format(output.get_path(), chunk_count))
        plt.clf()

        continuity_cache = chunk.tail(1)  # point continuity

    # part of event detection
    if optional_event_cache.is_only_start():
        optional_event_cache.add_end(Point(continuity_cache).get_index())
        events_list.append(optional_event_cache.calc_to_dataframe())

# s is the loaded data as 1 pandas Series, if its needed for anything
s = pd.concat(chunk_list)
# events is a pandas DataFrame with all events, each row is an event, with the first column holding a start timestamp
# and the second column holding the end timestamp, see print(events)
events = pd.concat(events_list, ignore_index=True)

print(s)
print(events)
output.save_csv(events)  # saves the events in a neat .csv
