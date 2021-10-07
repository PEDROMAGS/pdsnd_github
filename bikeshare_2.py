import time 
import pandas as pd
import math


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('There is data available for the cities of Chicago, New York City and Washington.\nPlease type the name of the city you want to filter by. \n').lower()
    while city not in CITY_DATA:
        city = input('Please type the name a valid city (Chicago, New York City or Washington)\n').lower()

    # get user input for month (all, january, february, ... , june)
    month=input('There is data available for the year of 2017 between January and June.\nPlease type either a specific month (January to June) or type the word "all" for all the available months data. \n').lower()
    months=['january', 'february', 'march', 'april', 'may', 'june','all']
    while month not in months:
        month=input('Please type a valid month (January to June) or type the word "all" for all the available months data.\n').lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please type the day of the week that you want to filter by (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday), \nor type the word "all" for all available days of the week.\n').lower()
    days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']
    while day not in days:
        day = input('Please type a valid day you want to filter by (Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday) or type the word "all"  for all available days of the week\n').lower()

    print('-'*140)
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

    print("Loading File(s) based on your selections: \n")
    print("Selected City : ", city)
    print("Selected Month: ", month)
    print("Selected Day  : ", day)

    df=pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday
    df['desc_month'] = df['Start Time'].dt.strftime("%B")
    df['desc_day'] = df['Start Time'].dt.strftime("%A")
    df['hour'] = df['Start Time'].dt.hour
    df['Start_End_Stations'] = 'From: ' + df['Start Station'] + ' To: ' + df['End Station']


    # filter by month if applicable
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]



    if day != 'all':
        df = df[df['desc_day'].str.lower() == day]


    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['desc_month'].mode()[0]
    print('The most common month is :', common_month)


    # display the most common day of week
    common_day = df['desc_day'].mode()[0]
    print('The most common day is :', common_day)

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('The most common hour is :', common_hour ,'o clock.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*140)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most common Start station is :', common_start_station )

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most common End station is :', common_end_station )

    # display most frequent combination of start station and end station trip
    common_end_station = df['Start_End_Stations'].mode()[0]
    print('The most frequent combination of Start/End station trip is:\n',common_end_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*140)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()

    print('The Total Travel Time is:', total_travel_time, 'seconds which is close to',math.floor(round((total_travel_time/60)/60,2)), 'hours',
          math.floor((round(total_travel_time/60/60,2) - math.floor(total_travel_time/60/60))*60), 'minutes and',
          math.floor((((round(total_travel_time/60/60,2) - math.floor(total_travel_time/60/60))*60)-(round((round(total_travel_time/60/60,2) - math.floor(total_travel_time/60/60))*60)))*60),'seconds' )

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The Mean Travel Time is:', mean_travel_time, 'seconds which is close to',
          math.floor((round(mean_travel_time/60/60,2) - math.floor(mean_travel_time/60/60))*60), 'minutes and',
          math.floor(((mean_travel_time/60)-math.floor(mean_travel_time/60))*60), 'seconds')


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*140)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    ut_counts = df['User Type'].value_counts()
    print('These are the User Type Counts:\n', ut_counts)

    # Display counts of gender

    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print('\nThese are the Gender Counts:\n', gender_counts)
    else:
        print('\nThere is no Gender Data available for the selected city')

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        most_common_year = df['Birth Year'].mode()[0]
        print('\nThe Most Common Year is :', int(most_common_year))
        most_recent_year = df['Birth Year'].max()
        print('The Most Recent Birth Year is :', int(most_recent_year))
        earliest_year = df['Birth Year'].min()
        print('The Earliest Birth Year is :', int(earliest_year))
    else:
        print('\nThere is no Birth Year Data available for selected city')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*140)

def display_rows(df):
    start_loc = 0
    while True:
        response = ['yes', 'no']
        choice = input("Are you interested in looking at the data? Type 'yes' or 'no'\n").lower()
        if choice in response:
            if choice == 'yes':
                end_loc = start_loc + 5
                data = df.iloc[start_loc:end_loc]
                start_loc += 5
                print(data)
            break
        else:
            print("Please enter a valid response")
    if choice == 'yes':
        while True:
            choice_inc = input("Are you interested in looking at more of the data? Type 'yes' or 'no'\n").lower()
            if choice_inc in response:
                if choice_inc == 'yes':
                    end_loc = start_loc + 5
                    data = df.iloc[start_loc:end_loc]
                    start_loc += 5
                    print(data)
                else:
                    break
            else:
                print("Please enter a valid response")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)


        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_rows(df)

        restart = input('Would you like to restart? Enter yes or no.')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()