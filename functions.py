import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import dates as mpl_dates

# this setting silences the SettingWithCopyWarning
pd.options.mode.chained_assignment = None

df = pd.read_csv('assets/messages-3.csv', usecols=['DATE', 'FROM', 'CONTENT'])

# create df only with 'Cheers' messages
cheers_df = df[df.CONTENT == 'Cheers']

# convert to datetime and sort by date
cheers_df['DATETIME'] = pd.to_datetime(cheers_df['DATE'])
cheers_df = cheers_df.drop(columns=['DATE'])

cheers_df.sort_values(by='DATETIME', key=pd.to_datetime, inplace=True, ascending=True)
cheers_df.reset_index(level=0, inplace=True)
cheers_df = cheers_df.drop(columns='index')

# create count column
cheers_df.insert(3, 'COUNT', 1)

# re-order columns with DATETIME first
cheers_df = cheers_df[['DATETIME', 'FROM', 'CONTENT', 'COUNT']]
# print(cheers_df)

# group by day
by_day = cheers_df.groupby(pd.Grouper(key='DATETIME', axis=0,
                                      freq='D', sort=True)).sum()
by_day.reset_index(level=0, inplace=True)
# print(by_day)

# create function to filter by date


def filter_by_date(input_df, start_date, end_date):
    output_df = input_df[(input_df['DATETIME'] > start_date) & (input_df['DATETIME'] < end_date)]
    return output_df


# define date filter
filter_start = "2021-01-01"
filter_end = "2021-12-01"

filtered_df = filter_by_date(input_df=by_day, start_date=filter_start, end_date=filter_end)

# assign date and count series
date = filtered_df['DATETIME']
count = filtered_df['COUNT']
date = np.array(pd.Series(date))
count = np.array(pd.Series(count))
# print(date)
# print(count)

plot_df = pd.DataFrame(columns=['DATE', 'COUNT'])
plot_df['DATE'] = date
plot_df['COUNT'] = count
# print(plot_df)
# plt.plot(plot_df)
# plt.show()


def plot_cheers(x, y):
    plt.style.use('fivethirtyeight')
    fig, ax = plt.subplots()
    ax.plot_date(x, y, '', '-')
    fig.suptitle('Daily Cheers Count')
    plt.xticks(fontsize=10)
    plt.xlabel('Date')
    plt.ylabel('Cheers / day')
    fig.autofmt_xdate()
    date_format = mpl_dates.DateFormatter('%b, %Y')
    plt.gca().xaxis.set_major_formatter(date_format)
    plt.rcParams["figure.figsize"] = (20, 8)
    plt.show()
    # st.line_chart(fig, ax)


# plot_cheers(date, count)



