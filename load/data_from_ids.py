from typing import List

from base_loader import BaseLoader


class DataFromIds(BaseLoader):
    """
    UNFINISHED:
    A loader that takes a list of file names and loads them from the raw data source.
    """

    def __init__(self, ids: List(str)) -> None:
        super.__init__()

        self.all_runs = ids
