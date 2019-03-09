from PIL import ImageDraw, Image
from TextDesign import TextDesign
from settings import week_starts_on
from DesignEntity import DesignEntity
from datetime import datetime
from Assets import weathericons, wpath

daynumber_y_size = (1, 0.65)
weekday_y_size = (daynumber_y_size[0], 1 - daynumber_y_size[1])
weekday_ypos = daynumber_y_size[1]
daynumber_fontsize = daynumber_y_size[1] * 0.8
weekday_fontsize = weekday_y_size[1] * 0.75
weathericon_ypos = 0.1
weathericon_height = 1 - 2 * weathericon_ypos

general_text_color = "black"
highlight_text_color = "red"
background_color = "white"

class DayRowDesign (DesignEntity):
    """Detailed view of a given date."""
    def __init__ (self, size, date):
        super(DayRowDesign, self).__init__(size)
        self.__init_image__(color=background_color)
        self.date = date

    def add_weather (self, weather):
        if weather.is_available is False:
            return
        self.__draw_forecast__(weather)

    def add_calendar (self, calendar):
        pass

    def add_rssfeed (self, rss):
        pass

    def __draw_forecast__ (self, weather):
        forecast = weather.get_forecast_in_days(self.date.day - datetime.today().day)
        
        if forecast is None:
            return

        height = int(weathericon_height * self.size[1])
        size = (height, height)
        ypos = weathericon_ypos * self.size[1]
        pos = (self.size[0] - ypos - size[0], ypos)
        icon = Image.open(wpath + weathericons[forecast.icon] + ".jpeg")
        resized_icon = icon.resize(size, resample=Image.LANCZOS)
        self.draw(resized_icon, pos)

    def __finish_image__ (self):
        self.__draw_day_number__()
        self.__draw_weekday__()

    def __draw_weekday__ (self):
        font_size = int(weekday_fontsize * self.size[1])
        size = (weekday_y_size[0] * self.size[1], weekday_y_size[1] * self.size[1])
        ypos = weekday_ypos * self.size[1]
        pos = (0, ypos)

        color = self.__get_day_color__()
        week_day_name = self.date.strftime("%a")
        
        week_day = TextDesign(size, text=week_day_name, background_color=background_color, color=color, fontsize=font_size, horizontalalignment="center", verticalalignment="top")
        week_day.pos = pos
        self.draw_design(week_day)

    def __draw_day_number__ (self):
        font_size = int(daynumber_fontsize * self.size[1])
        size = (daynumber_y_size[0] * self.size[1], daynumber_y_size[1] * self.size[1])
        pos = (0, 0)

        day_text = self.__get_day_text__()
        color = self.__get_day_color__()

        number = TextDesign(size, text=day_text, background_color=background_color, color=color, fontsize=font_size, horizontalalignment="center", verticalalignment="bottom")
        number.pos = pos
        self.draw_design(number)

    def __abs_co__ (self, coordinates):
        return (int(coordinates[0] * self.size[0]),int(coordinates[1] * self.size[1]))

    def __get_day_text__ (self):
        return str(self.date.day)

    def __get_day_color__ (self):
        """Depending on week_starts_on"""
        if week_starts_on == "Monday" and self.date.strftime("%w") == "0":
            return highlight_text_color
        elif week_starts_on == "Sunday" and self.date.strftime("%w") == "6":
            return highlight_text_color
        else:
            return general_text_color