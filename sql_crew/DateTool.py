from langchain_community.tools import tool
from datetime import datetime


@tool("Today's Date & Time Getter")
def get_date_time():
    """ Useful for retrieving the current date and time """
    now = datetime.now()
    return f"""Current Date and Time: {now.strftime("%Y-%m-%d %H:%M:%S")}"""
