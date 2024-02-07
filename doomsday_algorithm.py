import pandas as pd
import random
import time

class DateTracker:
    def __init__(self, date: str = None, start_date: pd.Timestamp = pd.Timestamp('1920-01-01'), end_date: pd.Timestamp = pd.Timestamp('today'), num_dates: int = 1):
        if date:
          self.date = pd.Timestamp(date)
        else:
          self.date = None
        self.doomsday_date = None
        self.doomsday_date_calculation = None
        self.doomsday_weekday = None
        self.doomsday_weekday_calculation = None
        self.century_doomsdays = {1500: 4, 1600: 3, 1700: 1, 1800: 6}
        self.month_doomsdays = {
        1: 3, 2: 7, 3: 7, 4: 4, 5: 9, 6: 6,
        7: 11, 8: 8, 9: 5, 10: 10, 11: 7, 12: 12
        }

    def generate_date(self, date: str, start_date: str, end_date: str):
        if not date:
          dates = pd.date_range(pd.Timestamp(start_date), pd.Timestamp(end_date)).to_list()
          sampled_dates = random.sample(dates, 1)
          self.date = sampled_dates[0]
        else:
          self.date = pd.Timestamp(date)

    def print_tracker(self, option: str = None):
        if option == 'date':
            print(f"Date: {self.date.strftime('%Y-%m-%d')}")
        elif option == 'weekday':
            print(f"Doomsday Weekday: {self.doomsday_weekday}")
        else:
            print(f"Doomsday Date: {self.doomsday_date_calculation}")
            print(f"Doomsday Weekday: {self.doomsday_weekday_calculation}")

    def get_century_doomsday(self):
        century = int(str(self.date.year)[:2] + '00')
        self.doomsday_date = century

        century_doomsdays = self.century_doomsdays
        century_ref = century % 1800 // 100 - 1
        self.doomsday_weekday = century_doomsdays[list(century_doomsdays.keys())[century_ref]]

        self.doomsday_weekday_calculation = f'{self.doomsday_weekday}'
        self.doomsday_date_calculation = f'{century}'

    def make_twelve_year_jump(self):
        starting_weekday = self.doomsday_weekday
        starting_date = self.doomsday_date

        century_year = int(str(self.date.year)[2:])
        twelve_year_jump = century_year // 12

        self.doomsday_weekday += twelve_year_jump
        self.doomsday_weekday = self.mod(self.doomsday_weekday)

        self.doomsday_weekday_calculation = f'({starting_weekday} + {century_year} // 12) mod7 = ({starting_weekday} + {twelve_year_jump}) mod7 = {self.doomsday_weekday}'
        self.doomsday_date += 12*twelve_year_jump
        self.doomsday_date_calculation = f'{starting_date} + 12 * {twelve_year_jump} = {self.doomsday_date}'

    def get_remaining_years(self):
        starting_weekday = self.doomsday_weekday
        starting_date = self.doomsday_date

        remaining_years = self.date.year - self.doomsday_date
        leap_year = remaining_years//4

        self.doomsday_weekday += remaining_years + leap_year
        self.doomsday_weekday = self.mod(self.doomsday_weekday)

        self.doomsday_weekday_calculation = f'({starting_weekday} + {remaining_years} + {leap_year}) mod7 = {self.doomsday_weekday}'
        self.doomsday_date_calculation = f'{starting_date} + {remaining_years} + {leap_year} = {self.date.year}'

    def get_weekday(self):
        starting_weekday = self.doomsday_weekday
        starting_date = self.doomsday_date

        month = self.date.month
        date_day = self.date.day
        doomsday_day = self.month_doomsdays[month]
        doomsday_day = self.add_leap_year_day(doomsday_day)
        days_difference = date_day - doomsday_day

        self.doomsday_weekday += days_difference + 14
        self.doomsday_weekday = self.mod(self.doomsday_weekday)
        self.doomsday_date = self.date.strftime('%Y-%m-%d')

        self.doomsday_weekday_calculation = f'({starting_weekday} + ({date_day} - {doomsday_day})) mod7 = {self.doomsday_weekday}'
        self.doomsday_date_calculation = f'{self.date.year}-{month}-{doomsday_day} + ({date_day} - {doomsday_day}) = {self.doomsday_date}'

    def add_leap_year_day(self, doomsday_day):
      year = tracker.date.year
      month = tracker.date.month
      century_leap = year % 400 == 0
      year_leap = int(str(year)[2:]) // 4 == int(str(year)[2:]) / 4
      month_leap = month in (1,2)
      if not century_leap:
        if year_leap:
          if month_leap:
            doomsday_day += 1
      return doomsday_day

    def mod(self, num: int) -> int:
        if num % 7 == 0:
          return 7
        else:
          return num % 7

    def practice(self, date: str = None, num_dates: int = 1, start_date: str = '1920-01-01', end_date: str = 'today'):
        for i in range(0,num_dates):
          self.generate_date(date, start_date, end_date)
          self.print_tracker('date')
          self.get_century_doomsday()
          input()
          self.print_tracker()
          self.make_twelve_year_jump()
          input()
          self.print_tracker()
          self.get_remaining_years()
          input()
          self.print_tracker()
          self.get_weekday()
          input()
          self.print_tracker()
          print('\n')

    def play(self, date: str = None, num_dates: int = 1, start_date: str = '1920-01-01', end_date: str = 'today', log_df: pd.DataFrame = pd.DataFrame()):
        start_time_total = time.perf_counter()
        total_tries = num_dates
        for i in range(0,num_dates):
          
          self.solve(date, start_date, end_date)
          self.print_tracker('date')
          answer = self.doomsday_weekday

          log_start = pd.Timestamp('today') - pd.Timedelta(hours=3)
          start_time = time.perf_counter()

          correct = False
          num_tries = 1

          while not correct:
            guess = input('Doomsday Weekday: ')
            if str(guess) == str(answer):
              print("\u2713")
              correct = True
            elif guess == 'break':
              break
            else:
              num_tries += 1
              total_tries += 1
              print("X")

          end_time = time.perf_counter()
          elapsed_time = end_time - start_time

          log_df['Start'] = log_start
          log_df['Duration'] = elapsed_time

          print(f'Number of tries: {num_tries}')
          print(f'\U0001F552 {round(elapsed_time,2)}s')
          print('\n')

        if num_dates > 1:
          end_time_total = time.perf_counter()
          elapsed_time_total = end_time_total - start_time_total
          print('Total')
          print(f'\U0001F552 {round(elapsed_time_total,2)}s')
          print(f'{round(elapsed_time_total/num_dates,2)}s per date')
          print(f'{round(total_tries/num_dates,2)} tries per date')
          print('\n')
        return log_df

    def solve(self, date: str, start_date: str, end_date: str):
        self.generate_date(date, start_date, end_date)
        self.get_century_doomsday()
        self.make_twelve_year_jump()
        self.get_remaining_years()
        self.get_weekday()
