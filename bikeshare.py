import time
import pandas as pd

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}

INPUT_MONTHS = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
DISPLAY_MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']
DAYS = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_city():
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid
    # inputs
    city = input('Please specify a city to analyze (chicago, new york city, washington)')
    # Checking if input is empty
    if len(city) > 0:
        city = city.lower()
        while not city.isalpha() or city not in CITY_DATA:
            print(f"The input '{city}' is invalid, please input one from the list above!")
            city = get_city()
    else:
        print("This field cannot be empty, please select a city from the example list above.")
        city = get_city()
    return city


def get_month():
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Please specify a month to analyze (all, january, february, ... , june)')
    if len(month) > 0:
        month = month.lower()
        while not month.isalpha() or month not in INPUT_MONTHS:
            month = get_month()
    else:
        print("This field cannot be empty, please select a month from January - June.")
        month = get_month()
    return month.capitalize()


def get_day():
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please specify a weekDay to analyze (all, monday, tuesday, ... sunday)')
    if len(day) > 0:
        day = day.lower()
        while not day.isalpha() or day not in DAYS:
            day = get_day()
    else:
        print("This field cannot be empty, please input a day of the week.")
        day = get_day()
    return day.capitalize()


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    city = get_city()
    month = get_month()
    day = get_day()

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month_name()
    df['day_name'] = df['Start Time'].dt.day_name()
    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    if day != 'all':
        # filter by day to create the new dataframe
        df = df[df['day_name'] == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    print(f"Most common month: {DISPLAY_MONTHS[df['Start Time'].dt.month.mode()[0]-1].capitalize()}")

    # TO DO: display the most common day of week

    # TO DO: display the most common start hour
    print(f"Most common start hour: {pd.to_datetime(df['Start Time']).dt.hour.mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print(f"Most commonly used Start Station: {df['Start Station'].mode()[0]}")

    # TO DO: display most commonly used end station
    print(f"Most commonly used End Station: {df['End Station'].mode()[0]}")

    # TO DO: display most frequent combination of start station and end station trip
    start_and_end_combination = df.groupby(
        ['Start Station', 'End Station']).size().idxmax()
    print(
        f'The most frequently travelled route starts at the station on {start_and_end_combination[0]}\nand end at the station on {start_and_end_combination[1]}.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print(f"Total travel time: {df['Trip Duration'].sum()}")

    # TO DO: display mean travel time
    print(f"Mean travel time: {df['Trip Duration'].mean()}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print(df['User Type'].value_counts())

    if 'Gender' in df:
        # TO DO: Display counts of gender
        print(df['Gender'].value_counts())

    if 'Birth Year' in df:
        # TO DO: Display earliest, most recent, and most common year of birth
        print(f"Earliest year: {pd.to_datetime(df['Start Time']).index.min()}")
        print(f"Most Recent year: {pd.to_datetime(df['Start Time']).index.max()}")
        print(f"Most Common year: {pd.to_datetime(df['Start Time']).mode()[0]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while view_data == 'yes':
      print(df.iloc[start_loc:start_loc+5])
      start_loc += 5
      view_data = input("Do you wish to continue? Enter yes or no: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        # print(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
