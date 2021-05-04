"""
Script to analyze data from Netflix ViewingActivity.csv:
    - total time viewing: movies, TV shows/series, trailers
    - longest period of viewing: number of days in rows services was used and start and end date of this period
    - number of watched movies and TV shows/series
    - sum of time spend of watching each title

By default:
    - input data file name is ViewingActivity.csv and is in the same directory as netflix_viewing_activity_analyzer.py
    - output file name is report.txt and is created in the same file as netflix_viewing_activity_analyzer.py

"""
import csv
from datetime import timedelta, date

# Activity types
MOVIE = "Movie"
TVSHOW = "TVShow"
TRAILER = "Trailer"  # Also teaser


class ViewingActivityAnalyzer:

    def __init__(self, viewing_file="ViewingActivity.csv"):
        self.viewing_file = viewing_file
        self.parsed_viewing_data = []
        self.viewing_dates = []
        self.viewing_data_from = None
        self.viewing_data_to = None
        self.viewing_duration = None
        self.total_time = timedelta()
        self.total_movies_time = timedelta()
        self.total_tv_shows_time = timedelta()
        self.total_trailer_time = timedelta()
        self.movies_data = {}
        self.tv_shows_data = {}
        self.max_viewing_period = {
            'Length': None,
            'From': None,
            'To': None
        }

    @staticmethod
    def format_date(d):
        return d.strftime("%d %b, %Y")

    @staticmethod
    def get_date(src_date):
        year, month, day = src_date.split("-")
        return date(year=int(year), month=int(month), day=int(day))

    @staticmethod
    def get_duration(src_duration):
        """ Get duration of the movie, TV show as timedelta for calculations.
        :param src_duration: str, duration from viewing activity data file
        :return: timedelta
        """
        hours, minutes, seconds = src_duration.split(":")
        return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))

    @staticmethod
    def get_activity_type(src_sup_video_type, src_title):
        if src_sup_video_type:  # Trailer
            return TRAILER
        if src_title:
            if ("Season" in src_title or "Series" in src_title) and ("Episode" in src_title or "Pilot" in src_title) \
                    or "Limited Series" in src_title:
                return TVSHOW
            else:
                return MOVIE

    @staticmethod
    def parse_data_row(row):
        activity_data = dict()
        activity_data["start_date"] = ViewingActivityAnalyzer.get_date(row["Start Time"].split()[0])
        activity_data["duration"] = ViewingActivityAnalyzer.get_duration(row["Duration"])
        activity_data["title"] = row["Title"].strip()
        activity_data["type"] = ViewingActivityAnalyzer.get_activity_type(row["Supplemental Video Type"].strip(),
                                                                          row["Title"].strip())
        return activity_data

    def read_data_file(self):
        with open(self.viewing_file, 'r', encoding="utf-8") as data_file:
            reader = csv.DictReader(data_file, delimiter=',')
            while True:
                try:
                    row = next(reader)
                    parsed_data = ViewingActivityAnalyzer.parse_data_row(row)
                    self.parsed_viewing_data.append(parsed_data)
                except StopIteration:
                    break

    def set_viewing_period_data(self):
        self.viewing_data_from = min(self.viewing_dates)
        self.viewing_data_to = max(self.viewing_dates)
        delta = self.viewing_data_to - self.viewing_data_from
        self.viewing_duration = delta.days

    def append_viewing_date(self, viewing_date):
        """ Append viewing date - when the service was used.
        :param viewing_date: date
        """
        if viewing_date not in self.viewing_dates:
            self.viewing_dates.append(viewing_date)

    @staticmethod
    def get_tv_show_title(title):
        """ Return TV Show title - without information related to Season, Episode.
        :param title: str
        :return: str
        """
        return title.split(":")[0]

    def append_movie_watching_time(self, title, duration):
        """ Append movie watching data related to movie.
        :param title: str
        :param duration: timedelta
        """
        norm_title = ViewingActivityAnalyzer.get_tv_show_title(title)
        if norm_title not in self.movies_data:
            self.movies_data[norm_title] = duration
        else:
            self.movies_data[norm_title] += timedelta() + duration

    def append_tv_show_watching_time(self, title, duration):
        """ Append TV Show watching data related to movie.
        :param title: str
        :param duration: timedelta
        """
        norm_title = ViewingActivityAnalyzer.get_tv_show_title(title)
        if norm_title not in self.tv_shows_data:
            self.tv_shows_data[norm_title] = duration
        else:
            self.tv_shows_data[norm_title] += timedelta() + duration

    def get_viewing_periods(self):
        periods = []
        period = []
        try:
            for i, viewing_date in enumerate(self.viewing_dates):
                if not period:  # Start new watching period
                    period.append(self.viewing_dates[i])

                delta = self.viewing_dates[i + 1] - self.viewing_dates[i]
                if delta.days != -1:  # End watching period
                    period.append(self.viewing_dates[i])
                    periods.append(period)
                    period = []
        except IndexError:
            return periods

    def get_max_viewing_period(self):
        viewing_periods = self.get_viewing_periods()
        max_period = None
        max_period_length = 1
        for period in viewing_periods:
            delta = period[0] - period[1]
            period_length = delta.days
            if period_length > max_period_length:
                max_period_length = period_length
                max_period = period

        if max_period:
            self.max_viewing_period["Length"] = max_period_length
            self.max_viewing_period["From"] = ViewingActivityAnalyzer.format_date(max_period[1])
            self.max_viewing_period["To"] = ViewingActivityAnalyzer.format_date(max_period[0])

    def analyze_parsed_data(self):
        for activity_data in self.parsed_viewing_data:
            self.append_viewing_date(activity_data["start_date"])
            if activity_data["type"] == MOVIE:
                self.append_movie_watching_time(activity_data["title"],
                                                activity_data["duration"])
                self.total_movies_time += activity_data["duration"]
            if activity_data["type"] == TVSHOW:
                self.append_tv_show_watching_time(activity_data["title"],
                                                  activity_data["duration"])
                self.total_tv_shows_time += activity_data["duration"]
            elif activity_data["type"] == TRAILER:
                self.total_trailer_time += activity_data["duration"]
        self.total_time = self.total_tv_shows_time + self.total_movies_time + self.total_trailer_time
        self.set_activity_data_dates()
        self.get_max_viewing_period()

    def set_activity_data_dates(self):
        """ Set first and last date from viewing data activity file. """
        self.viewing_data_from = min(self.viewing_dates)
        self.viewing_data_to = max(self.viewing_dates)
        delta = self.viewing_data_to - self.viewing_data_from
        self.viewing_duration = delta.days

    @staticmethod
    def save_chapter_section(f, number, title):
        """ Save chapter header section to report file.
        :param f: file object, report file
        :param number: str, chapter number
        :param title: str, chapter title
        """
        f.write(75 * "*" + "\n")
        f.write("Chapter {}. {}\n".format(number, title))
        f.write(75 * "*" + "\n")

    def save_viewing_activity_period_data(self, f):
        from_formatted = ViewingActivityAnalyzer.format_date(self.viewing_data_from)
        to_formatted = ViewingActivityAnalyzer.format_date(self.viewing_data_to)

        ViewingActivityAnalyzer.save_chapter_section(f, "1", "Viewing activity period")
        f.write("{:^20}|{:^20}|{:^20}\n".format("From", "To", "Period (days)"))
        f.write("{:^20}|{:^20}|{:^20}\n".format(from_formatted, to_formatted, str(self.viewing_duration)))
        f.write("\n")

    def save_general_statistics(self, f):
        viewing_days = len(self.viewing_dates)
        viewing_percentage = round((viewing_days / 336) * 100, 1)
        movies_percentage = round((self.total_movies_time / self.total_time) * 100, 1)
        tvshows_percentage = round((self.total_tv_shows_time / self.total_time) * 100, 1)
        trailer_percentage = round((self.total_trailer_time / self.total_time) * 100, 1)

        ViewingActivityAnalyzer.save_chapter_section(f, "2", "General statistics")
        f.write("Days with Netflix activity: {} ({}%)\n".format(viewing_days, viewing_percentage))
        f.write("Total time watching: {}\n".format(self.total_time))
        f.write("Total TV shows time watching: {} ({}%)\n".format(self.total_tv_shows_time, tvshows_percentage))
        f.write("Total movies  time watching: {} ({}%)\n".format(self.total_movies_time, movies_percentage))
        f.write("Total trailers time watching: {} ({}%)\n".format(self.total_trailer_time, trailer_percentage))
        f.write("Number of TV shows: {}\n".format(len(self.tv_shows_data)))
        f.write("Number of Movies: {}\n".format(len(self.movies_data)))
        f.write("Max watching period in row: {} days (from {} to {})\n".format(self.max_viewing_period["Length"],
                                                                               self.max_viewing_period["From"],
                                                                               self.max_viewing_period["To"]))
        f.write("\n")

    def save_tv_shows_time_statistics(self, f):
        ViewingActivityAnalyzer.save_chapter_section(f, "3", "TV Shows/Series watching time")
        for title, time in self.tv_shows_data.items():
            f.write("{} : {}\n".format(title, time))
        f.write("\n")

    def save_movie_time_statistics(self, f):
        ViewingActivityAnalyzer.save_chapter_section(f, "4", "Movies watching time")
        for title, time in self.movies_data.items():
            f.write("{} : {}\n".format(title, time))
        f.write("\n")

    def save_report(self):
        with open("report.txt", 'w', encoding="utf-8") as f:
            self.save_viewing_activity_period_data(f)
            self.save_general_statistics(f)
            self.save_tv_shows_time_statistics(f)
            self.save_movie_time_statistics(f)


if __name__ == "__main__":
    activity = ViewingActivityAnalyzer()
    activity.read_data_file()
    activity.analyze_parsed_data()
    activity.save_report()
