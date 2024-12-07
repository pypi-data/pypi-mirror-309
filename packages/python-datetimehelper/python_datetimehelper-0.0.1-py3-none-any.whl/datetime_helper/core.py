from datetime import datetime, date, timedelta
import re
import pytz

class DateUtils:

    @staticmethod
    def __parse_date(input_date):
        if isinstance(input_date, datetime):
            return input_date
        elif isinstance(input_date, date):
            return datetime.combine(input_date, datetime.min.time())
        elif isinstance(input_date, str):
            try:
                return datetime.fromisoformat(input_date)
            except ValueError:
                raise ValueError("Invalid date format. Use ISO 8601 format.")
        else:
            raise TypeError("Invalid input type. Provide datetime, date, or ISO 8601 string.")
        
    @staticmethod
    def __split_format(format_string):
        return re.split(r'([^\w])', format_string)
    
    @staticmethod
    def format_date(date_input, format_string):
        date_input = DateUtils.__parse_date(date_input)
        format_parts = DateUtils.__split_format(format_string)
        formatted = ""

        for part in format_parts:
            if part in ['dd', 'DD']:
                formatted += f"{date_input.day:02}"
            elif part in ['d', 'D']:
                formatted += str(date_input.day)
            elif part == 'MM':
                formatted += f"{date_input.month:02}"
            elif part == 'M':
                formatted += str(date_input.month)
            elif part in ['yyyy', 'YYYY']:
                formatted += str(date_input.year)
            elif part in ['yy', 'YY']:
                formatted += str(date_input.year)[-2:]
            elif part == 'MMMM':
                formatted += date_input.strftime('%B')
            elif part == 'MMM':
                formatted += date_input.strftime('%b')
            elif part == 'dddd':
                formatted += date_input.strftime('%A')
            elif part == 'ddd':
                formatted += date_input.strftime('%a')
            elif part == 'HH':
                formatted += f"{date_input.hour:02}"
            elif part == 'hh':
                formatted += f"{date_input.hour % 12 or 12:02}"
            elif part == 'mm':
                formatted += f"{date_input.minute:02}"
            elif part == 'ss':
                formatted += f"{date_input.second:02}"
            elif part == 'a':
                formatted += date_input.strftime('%p').lower()
            elif part == 'A':
                formatted += date_input.strftime('%p')
            else:
                formatted += part
        return formatted
    
    @staticmethod
    def convert_timezone(datetime_input, from_timezone, to_timezone):
        datetime_input = DateUtils.__parse_date(datetime_input)
        from_tz = pytz.timezone(from_timezone)
        to_tz = pytz.timezone(to_timezone)
        localized = from_tz.localize(datetime_input)
        return localized.astimezone(to_tz)
    
    @staticmethod
    def add_time(datetime_input, **time_delta):
        datetime_input = DateUtils.__parse_date(datetime_input)
        return datetime_input + timedelta(**time_delta)
