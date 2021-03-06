from DesignEntity import DesignEntity
from PIL import ImageDraw
from TextDesign import TextDesign
from WeatherColumnDesign import WeatherColumnDesign
from datetime import date, timedelta, datetime, timezone
from SingelDayEventListDesign import SingelDayEventListDesign
from Assets import fonts, colors, defaultfontsize
from settings import general_settings
from BoxDesign import BoxDesign

numberbox_ypos = 0.15
numberbox_height = 1 - 2 * numberbox_ypos
number_height = numberbox_height * 0.83
number_boxypos = 0.17
month_height = numberbox_height / 4
monthbox_xpadding = 0.013
monthbox_ypadding = -0.05
monthbox_width = 1 - numberbox_ypos - monthbox_xpadding
weathercolumn_y_size = (0.4, 1)
weekday_height = numberbox_height * 0.19
weekdaybox_height = (weekday_height / numberbox_height) * 1.5
eventlist_static_fontsize = defaultfontsize
eventlist_xpadding = monthbox_xpadding
eventlist_ypadding = 0.01

numberbox_font_color = colors["bg"]
numberbox_background_color = colors["hl"]
weekday_font = fonts["bold"]


class DayHeaderDesign (DesignEntity):
    """Detailed and big view of a given date."""

    def __init__(self, size, date):
        super(DayHeaderDesign, self).__init__(size)
        self.weather_column_width = 0
        self.date = date

    def add_weather(self, weather):
        if general_settings["weather-info"] == False:
            return

        forecast = weather.get_forecast_in_days(
            self.date.day - date.today().day)
        self.weather_column_width = weathercolumn_y_size[0] * self.size[1]
        size = (self.weather_column_width,
                weathercolumn_y_size[1] * self.size[1])
        pos = (self.size[0] - size[0], 0)

        design = WeatherColumnDesign(size, forecast)
        design.pos = pos
        self.draw_design(design)

    def add_calendar(self, calendar):
        local_tzinfo = datetime.now(timezone.utc).astimezone().tzinfo
        now = datetime.now(local_tzinfo)
        time_until_tomorrow = (datetime(
            now.year, now.month, now.day, 0, 0, 0, 0, local_tzinfo) + timedelta(1)) - now
        self.__draw_event_list__(
            calendar.get_upcoming_events(time_until_tomorrow, now))

    def add_events(self, events):
        self.__draw_event_list__(events)

    def add_rssfeed(self, rss):
        pass

    def add_crypto(self, crypto):
        pass

    def __finish_image__(self):
        self.__draw_number_square__()
        self.__draw_month__()

    def __draw_event_list__(self, events):
        box_ypos = numberbox_ypos * self.size[1]
        box_xpos = numberbox_ypos * self.size[1]
        box_height = numberbox_height * self.size[1]
        xpadding = eventlist_xpadding * self.size[0]
        ypadding = eventlist_ypadding * self.size[1]
        monthbox_height = (monthbox_ypadding + month_height) * self.size[1]
        pos = (box_xpos + box_height + xpadding,
               box_ypos + monthbox_height + ypadding)
        size = (self.size[0] - pos[0] - self.weather_column_width,
                self.size[1] - pos[1] - box_ypos)
        fontsize = eventlist_static_fontsize

        rel_dates = [self.date for _ in range(len(events))]
        event_list = SingelDayEventListDesign(
            size, events, fontsize, event_prefix_rel_dates=rel_dates)
        event_list.pos = pos
        self.draw_design(event_list)

    def __draw_month__(self):
        font_size = int(month_height * self.size[1])
        xpadding = int(monthbox_xpadding * self.size[0])
        ypadding = int(monthbox_ypadding * self.size[1])
        box_ypos = int(numberbox_ypos * self.size[1])
        box_height = int(numberbox_height * self.size[1])
        box_pos = (box_ypos + box_height + xpadding, box_ypos + ypadding)
        box_size = (int(monthbox_width * self.size[0]), box_height)

        month_name = self.date.strftime("%B")
        month = TextDesign(box_size, text=month_name, fontsize=font_size)
        month.pos = box_pos
        self.draw_design(month)

    def __draw_number_square__(self):
        box_height = numberbox_height * self.size[1]
        box_ypos = numberbox_ypos * self.size[1]
        box_pos = (box_ypos, box_ypos)
        box_size = (box_height, box_height)

        box = BoxDesign(box_size, fill=numberbox_background_color)
        box.pos = box_pos
        self.draw_design(box)

        self.__draw_today_number__()
        self.__draw_weekday__()

    def __draw_today_number__(self):
        font_size = number_height * self.size[1]
        box_height = numberbox_height * self.size[1]
        box_ypos = numberbox_ypos * self.size[1]
        ypadding = number_boxypos * box_height
        size = (box_height, box_height - ypadding)
        pos = (box_ypos, box_ypos + ypadding)

        day_text = self.__get_day_text__()
        number = TextDesign(size, text=day_text, background_color=numberbox_background_color,
                            color=numberbox_font_color, fontsize=font_size, horizontalalignment="center", verticalalignment="center")
        number.pos = pos
        number.mask = False
        self.draw_design(number)

    def __draw_weekday__(self):
        font_size = weekday_height * self.size[1]
        box_height = numberbox_height * self.size[1]
        size = (box_height, weekdaybox_height * box_height)
        box_ypos = numberbox_ypos * self.size[1]
        pos = (box_ypos, box_ypos)

        week_day_name = self.date.strftime("%A")
        week_day = TextDesign(size, text=week_day_name, background_color=numberbox_background_color, color=numberbox_font_color,
                              fontsize=font_size, horizontalalignment="center", verticalalignment="center", font=weekday_font)
        week_day.pos = pos
        week_day.mask = False
        self.draw_design(week_day)

    def __abs_co__(self, coordinates):
        return (int(coordinates[0] * self.size[0]), int(coordinates[1] * self.size[1]))

    def __get_day_text__(self):
        return str(self.date.day)
