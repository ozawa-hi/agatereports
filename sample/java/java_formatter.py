from jnius import autoclass
import datetime


def format_date(date, output_pattern, input_pattern='yyyy-MM-dd HH:mm:ss.n'):
    DateTimeFormatter = autoclass('java.time.format.DateTimeFormatter')
    formatter = DateTimeFormatter.ofPattern(input_pattern)

    LocalDateTime = autoclass('java.time.LocalDateTime')
    String = autoclass('java.lang.String')
    string = String('2019-02-24T10:15:30')

    # string = String('2019-02-25 13:21:00.885079')
    string = String(str(date))
    local_date = LocalDateTime.parse(string, formatter)

    date_formatter = DateTimeFormatter.ofPattern(output_pattern)

    return local_date.format(date_formatter)
    # formatted_date = local_date.format(date_formatter)
    # print(formatted_date)


if __name__ == '__main__':
    format_date(datetime.datetime.now(), 'yyyy/MM/dd HH:mm')
