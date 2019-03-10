import copy
import csv
import glob
import os
from collections import deque

# TODO handle better the names since it will break for names with spaces in them
from threading import Lock, Thread
from time import sleep


class RollingDataBase:
    CSV_DELIMITER = ";"
    QUOTE_CHAR = "#"

    def __init__(self, path_db_folder, max_size=10000, auto_save_s=0):
        self._max_size = max_size
        self._db_folder = path_db_folder
        self._values = {}
        self._values_lock = Lock()
        self._stop = False
        if auto_save_s > 0:
            self._auto_save_thread = Thread(target=self._auto_save, args=(auto_save_s,))
            self._auto_save_thread.start()
        else:
            self._auto_save_thread = None

    def add(self, name, val):
        with self._values_lock:
            if name not in self._values:
                self._values[name] = deque(maxlen=self._max_size)

            self._values[name].append(val)

    def get_all(self):
        with self._values_lock:
            result = {}
            for name, queue in self._values.items():
                result[name] = copy.deepcopy(list(queue))
            return result

    def load(self):
        # Get all the values from the files
        matching_pattern = os.path.join(self._db_folder, "*.csv")
        file_paths = glob.glob(matching_pattern)
        with self._values_lock:
            for file_path in file_paths:
                self._load_file(file_path)

    def _load_file(self, file_path):
        filename = os.path.basename(file_path)
        name = filename.replace(".csv", "")

        values = deque(maxlen=self._max_size)
        with open(file_path, "r", newline='') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=self.CSV_DELIMITER, quotechar=self.QUOTE_CHAR)
            for row in csv_reader:
                if row:
                    values.append(row)

        self._values[name] = values

    def save(self):
        os.makedirs(self._db_folder, exist_ok=True)
        with self._values_lock:
            for name, values in self._values.items():
                self._save_name_params(name, values)

    def _save_name_params(self, name, values):
        file_path = os.path.join(self._db_folder, name + ".csv")
        with open(file_path, "w", newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=self.CSV_DELIMITER, quotechar=self.QUOTE_CHAR)
            for value in values:
                csv_writer.writerow(list(value))

    def _auto_save(self, auto_save_s):
        while not self._stop:
            self.save()
            sleep(1000 * auto_save_s)

    def stop_auto_save(self):
        self._stop = True
        if self._auto_save_thread:
            self._auto_save_thread.join()
            self._auto_save_thread = None

    def __del__(self):
        self.stop_auto_save()
