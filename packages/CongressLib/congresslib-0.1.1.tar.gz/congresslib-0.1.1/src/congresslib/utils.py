from datetime import datetime
from typing import Union

def format_date(date_input: Union[str, datetime]) -> str:
    """
    Convert input to "YYYY-MM-DDT00:00:00Z" format.

    Args:
        date_input (Union[str, datetime]): The date input to convert. It can be a string or a datetime object.

    Returns:
        str: The date in "YYYY-MM-DDT00:00:00Z" format.

    Raises:
        ValueError: If the input string cannot be parsed into a valid date.
    """
    if isinstance(date_input, datetime):
        return date_input.strftime("%Y-%m-%dT00:00:00Z")
    elif isinstance(date_input, str):
        try:
            parsed_date = datetime.fromisoformat(date_input)
            return parsed_date.strftime("%Y-%m-%dT00:00:00Z")
        except ValueError:
            raise ValueError("Invalid date string format. Please use ISO 8601 or provide a datetime object.")
    else:
        raise TypeError("date_input must be a string or a datetime object.")
