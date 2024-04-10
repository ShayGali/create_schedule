from dataclasses import dataclass
from typing import List, Optional, Union

import pandas as pd
import math
import re

pattern = r"\d{2}:\d{2}- \d{2}:\d{2}"


@dataclass
class Lecture:
    """A class to represent a lecture"""

    class_name: str
    lecturer: str
    day: str
    hours: str
    room: Union[str, float]
    start_time: str = None
    end_time: str = None
    start_hour: int = None
    end_hour: int = None

    def __post_init__(self):
        """Calculate the start and end times of the lecture"""
        if not re.search(pattern, self.hours):
            raise ValueError(f"Invalid hours format. the format should be: 'hh:mm - hh:mm', instead got: {self.hours}")

        self.end_time, self.start_time = self.hours.split("- ")
        self.start_hour = int(self.start_time.split(":")[0])
        self.end_hour = int(self.end_time.split(":")[0])

        if type(self.room) == float and math.isnan(self.room):
            self.room = "חדר לא ידוע"

    def __str__(self):
        """Return a string representation of the lecture"""
        return f"{self.class_name}\n{self.lecturer}\n{self.hours}\n{self.room}"


def create_lectures_list(df: pd.DataFrame) -> List[Lecture]:
    """given a DataFrame, create a list of Lecture objects"""
    lectures_list = []
    for index, row in df.iterrows():
        lectures_list.append(
            Lecture(
                row["שם שעור"],
                row["מורה"],
                row["יום"],
                row["שעות"],
                row["חדר"],
            )
        )
    return lectures_list
