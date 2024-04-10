from typing import Tuple


def get_color(class_name: str) -> Tuple[str, str]:
    """
    This function returns the color of the class and the color of the text.
    Now it will work for semester 1 only.
    """
    if "אלגוריתמים" in class_name:
        return "#B2EBF2", "#80DEEA"  # Light Blue Lagoon & Medium Turquoise
    elif class_name.startswith("אוטומטים"):
        return "#D1C4E9", "#B39DDB"  # Bright Gray & Light Pastel Purple
    elif class_name.startswith("הסתברות"):
        return "#F8BBD0", "#F48FB1"  # Light Thulian Pink & English Lavender
    elif class_name.startswith("תכנות מערכות"):
        return "#C8E6C9", "#A5D6A7"  # Tea Green & Light Moss Green
    elif class_name.startswith("מערכות הפעלה"):
        return "#FFECB3", "#FFE082"  # Very Pale Orange & Light Gold
    elif class_name.startswith("מסדי נתונים"):
        return "#CD5C5C", "#BC8F8F"
    elif class_name.startswith("ראייה ממוחשבת"):
        return "#FFCCBC", "#FFAB91"  # Light Apricot & Light Salmon
    elif class_name.startswith("הגנת פרוטו"):
        return "#FFD54F", "#FFC107"  # Light Goldenrod Yellow & Golden Yellow
    elif class_name.startswith("מעבדת סייבר"):
        return "#FFCC80", "#FFB74D"  # Light Orange & Light Orange
    return "#FFFFFF", "#FFFFFF"  # White & White
