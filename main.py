import tkinter as tk
from tkinter import messagebox
from typing import List
import pandas as pd

from lecture import create_lectures_list, Lecture
from utils import get_color

START_HOUR = 9  # 9:00 AM
END_HOUR = 22  # 10:00 PM

NUMBER_OF_COLUMNS = 10

HOURLY_INTERVAL = 30

LECTURE_BG_COLOR = "#89CFF0"
PRACTICE_BG_COLOR = "#FFCC99"
EMPTY_BG_COLOR = "#F5F5F5"

# days = ["ו", "ה", "ד", "ג", "ב", "א"]
days = ["ה", "ד", "ג", "ב", "א"]

day_to_full_name = {
    "א": "ראשון",
    "ב": "שני",
    "ג": "שלישי",
    "ד": "רביעי",
    "ה": "חמישי",
    "ו": "שישי",
}

times = [
    f"{hour:02d}:{minute:02d}"
    for hour in range(START_HOUR, END_HOUR)
    for minute in range(0, 60, HOURLY_INTERVAL)
]


def create_frame(root):
    """Create a new Frame widget to hold the Canvas and the vertical and horizontal Scrollbars"""

    # Create a PanedWindow widget
    panedwindow = tk.PanedWindow(root, orient="horizontal")

    # Create a new Frame widget to hold the Canvas and the vertical Scrollbar
    frame_with_scrollbar = tk.Frame(panedwindow)
    frame_with_scrollbar.pack(fill="both", expand=True)

    # Create a new Canvas widget
    canvas = tk.Canvas(frame_with_scrollbar)
    canvas.pack(side="left", fill="both", expand=True)

    # Create horizontal and vertical Scrollbar widgets
    x_scrollbar = tk.Scrollbar(panedwindow, orient="horizontal", command=canvas.xview)
    x_scrollbar.pack(side="bottom", fill="x")

    y_scrollbar = tk.Scrollbar(
        frame_with_scrollbar, orient="vertical", command=canvas.yview
    )
    y_scrollbar.pack(side="right", fill="y")

    # Configure the canvas to use the scrollbars
    canvas.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)

    # Create a Frame widget to hold the grid of Label widgets
    frame = tk.Frame(canvas)

    # Add the frame to the canvas
    canvas.create_window((0, 0), window=frame, anchor="nw")

    # Update the scroll-region of the canvas to match the size of the frame
    frame.bind(
        "<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Add the Frame to the PanedWindow
    panedwindow.add(frame_with_scrollbar)

    # Pack the PanedWindow
    panedwindow.pack(fill="both", expand=True)
    return frame


def create_schedule(frame):
    """Create a grid of PanedWindow widgets to hold the lecture labels"""

    # Create a grid of PanedWindow widgets to hold the lecture labels
    cells = [
        [
            [
                tk.PanedWindow(
                    frame,
                    borderwidth=1,
                    relief="solid",
                    bg=EMPTY_BG_COLOR,
                )
                for _ in range(NUMBER_OF_COLUMNS)
            ]  # NUMBER_OF_COLUMNS columns for each day
            for _ in days
        ]
        for _ in times
    ]

    # Add the paned windows to the grid
    for i in range(
            (END_HOUR - START_HOUR) * (60 // HOURLY_INTERVAL)
    ):  # For each HOURLY_INTERVAL-minute interval between START_HOUR and END_HOUR
        for j in range(len(days)):  # For each day
            for k in range(NUMBER_OF_COLUMNS):  # For each column in the day
                cells[i][j][k].grid(
                    row=i + 1, column=j * NUMBER_OF_COLUMNS + k + 1, sticky="nsew"
                )

    # Create headers for the rows and columns
    for i, time in enumerate(times):
        tk.Label(frame, text=time, borderwidth=1, relief="solid").grid(
            row=i + 1,
            column=len(days) * NUMBER_OF_COLUMNS + 1,
            sticky="nsew",  # Move to the right side
        )

    for j, day in enumerate(days):
        tk.Label(frame, text=day_to_full_name[day], borderwidth=1, relief="solid").grid(
            row=0,
            column=j * NUMBER_OF_COLUMNS + 1,
            columnspan=NUMBER_OF_COLUMNS,
            sticky="nsew",  # Span across 4 columns
        )

    # Make each column expand to fill the available space
    for i in range(
            len(days) * NUMBER_OF_COLUMNS + 2
    ):  # Adjust for the moved hour column
        frame.columnconfigure(i, weight=1)


def get_lectures_from_csv():
    """Create a list of Lecture objects from the csv file"""
    # read the csv file
    df = pd.read_csv("data/table.csv", encoding="utf-8")
    # df = pd.read_csv("data/clean_data.csv")

    # Create a list of Lecture objects
    lectures = create_lectures_list(df)

    return lectures


def add_lectures(frame: tk.Frame, lectures: List[Lecture]):
    """Add the lectures to the schedule"""
    # Sort the lectures by day and start time
    lectures = sorted(lectures, key=lambda lec: (lec.day, lec.start_time))

    # Keep track of the last lecture for each day and column
    last_lecture = {
        day: {last_col: None for last_col in range(1, NUMBER_OF_COLUMNS + 1)}
        for day in days
    }

    # Iterate over the lectures
    for lecture in lectures:
        # Get the background color for the lecture
        bg_color = (
            get_color(lecture.class_name)[0]
            if "תרגיל" in lecture.class_name
            else get_color(lecture.class_name)[1]
        )

        # Find the index of the day and time
        day_index = days.index(lecture.day)
        start_time_index = times.index(lecture.start_time)
        end_time_index = times.index(lecture.end_time)

        # Calculate the number of time slots the lecture spans
        duration = end_time_index - start_time_index

        # Create a new Frame widget for the lecture
        lecture_frame = tk.Frame(frame, borderwidth=1, relief="solid", bg=bg_color)

        # Create a new Label widget for the lecture
        lecture_label = tk.Label(lecture_frame, text=str(lecture), bg=bg_color)

        # Add the lecture label to the lecture frame
        lecture_label.pack()

        # calculate the columns for the lecture
        # Initialize column to -1
        column = -1

        # Iterate over the columns for the given day
        for col in reversed(
                range(1, NUMBER_OF_COLUMNS + 1)
        ):  # start from the right column to the left
            # If there is no lecture in the column or
            # the current lecture's start time is later than the end time of the last lecture in the column
            if (
                    last_lecture[lecture.day][col] is None
                    or lecture.start_time >= last_lecture[lecture.day][col].end_time
            ):
                # Set column to the current column and break the loop
                column = col
                break

        # If no available column was found
        if column == -1:
            messagebox.showinfo(
                "אין מספיק מקום עבור הקורס",
                "עבור הקורס "
                + lecture.class_name
                + " אין מספיק מקום במערכת השעות"
                + ".\n !הקורס לא הוסף למערכת",
                icon="warning",
            )
            continue

        # Add the lecture frame to the grid
        lecture_frame.grid(
            row=start_time_index + 1,
            column=day_index * NUMBER_OF_COLUMNS + column,
            rowspan=duration,
            sticky="nsew",
        )

        # Update the last lecture and its column
        lecture.column = column
        last_lecture[lecture.day][column] = lecture


def main():
    # Create a new Tkinter window
    root = tk.Tk()
    root.title("מערכת שעות")

    # Make the window full screen
    root.state("zoomed")

    frame = create_frame(root)
    create_schedule(frame)
    lectures = get_lectures_from_csv()
    add_lectures(frame, lectures)
    root.mainloop()


if __name__ == "__main__":
    main()
