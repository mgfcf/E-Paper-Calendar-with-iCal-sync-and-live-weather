from settings import hours

first_occurrence_char = '['
middle_occurrence_char = '|'
last_occurrence_char = ']'

def time_str (dt):
    if hours is "12":
        return dt.strftime("%I:%M %p")
    elif hours is "24":
        return dt.strftime("%H:%M")
    else:
        return str(dt)

def event_prefix_str (event, relative_date=None):
    if relative_date is None:
        relative_date = event.begin_datetime.date()

    #Is multiday event
    if event.begin_datetime.day is not event.end_datetime.day or \
        event.begin_datetime.month is not event.end_datetime.month:
        return event_time_summary(event)
    
    #Relative to
    #First day
    if event.begin_datetime.day is relative_date.day and \
        event.begin_datetime.month is relative_date.month:
        return event_time_summary(event) + first_occurrence_char

    #Last day
    elif event.end_datetime.day is relative_date.day and \
        event.end_datetime.month is relative_date.month:
        event.begin_datetime = event.end_datetime
        return event_time_summary(event) + last_occurrence_char

    #Some day
    else:
        event.allday = True
        return event_time_summary(event)

def event_time_summary (event):
    if event.allday:
        return "•"
    else:
        return time_str(event.begin_datetime)

def date_str(dt):
    return self.__remove_leading_zero__(dt.strftime('%d %b'))

def remove_leading_zero (text):
        while text[0] is '0':
            text = text[1:]
        return text