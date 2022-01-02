import streamlit as st
import datetime
import plotly.graph_objects as go
from functions import *

# set css style
with open("style.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)

# define date filter
filter_start = "2016-01-01"
filter_end = "2021-12-01"
filtered_df = filter_by_date(input_df=by_day, start_date=filter_start, end_date=filter_end)

# center title
col1, col2, col3 = st.columns([2, 6, 2])
with col1:
    st.write("")
with col2:
    st.title('🎅 Cheers Counter  🥂')
with col3:
    st.write("")

st.info('This web app tracks and displays data regarding the use of the term "Cheers" '
        'in LinkedIn conversations between Ben and Jonathan')


# create dashboard functions
# total count, average response times


def calculate_total_count():
    total_count_df = df[df['CONTENT'] == 'Cheers']
    total_count = total_count_df.shape[0]
    total_count = 'Total count : ' + str(total_count)
    return total_count


def calculate_maximums():
    # calculate max day
    max_day = by_day.loc[by_day['COUNT'].idxmax()]
    max_day_count = str(max_day[1])
    max_day_date = str(max_day[0])
    max_day_date = max_day_date.split(' ')
    max_day_date = max_day_date[0]
    max_day_out = 'Our busiest day was ' + max_day_date + ' when we said "Cheers" ' + max_day_count + ' times!'
    # calculate max week
    by_week = cheers_df.groupby(pd.Grouper(key='DATETIME', axis=0,
                                           freq='7D', sort=True)).sum()
    by_week.reset_index(level=0, inplace=True)

    max_week = by_week.loc[by_week['COUNT'].idxmax()]
    max_week_date = str(max_week[0])
    max_week_count = str(max_week[1])

    max_week_date = max_week_date.split(' ')
    max_week_date = max_week_date[0]
    max_week_out = '\nOur busiest week was the week of ' + max_week_date + \
                   ' when we said "Cheers" ' + max_week_count + ' times! Wow! 🤩 '

    return max_day_out, max_week_out


# display dashboard
st.text('How many times has "Cheers" been said?')
st.text(calculate_total_count())
st.text(calculate_maximums()[0])
st.text(calculate_maximums()[1])

# date selector
today = datetime.date.today()
start_date = datetime.date(2021, 1, 1)
st.info('Select dates to view on graph')
slider_range = st.slider('Date selector',
                         value=[start_date, today])
new_start = str(slider_range[0])
new_end = str(slider_range[1])
# st.write(new_start)
# st.write(new_end)

# update df with new date values
filtered_df = filter_by_date(input_df=by_day, start_date=new_start, end_date=new_end)
# st.dataframe(filtered_df)
date = filtered_df['DATETIME']
count = filtered_df['COUNT']
date = np.array(date)
count = np.array(count)


# calculate response times


def calculate_response_times():
    def format_time(time_in):
        time_in = str(time_in).split(' ')
        time_str = time_in[2].split(':')
        final = time_in[0] + ' ' + time_in[1] + ', ' + time_str[0] + ' hours, and ' + time_str[1] + ' minutes'
        return final

    response_df = cheers_df  # this needs to be replaced with a time filtered df
    # st.dataframe(filtered_df)
    datetime_series = response_df['DATETIME']
    response_times = []
    for i in range(len(datetime_series)):
        try:
            delta = datetime_series[i + 1] - datetime_series[i]
            response_times.append(delta)
        except:
            pass
    response_times = pd.Series(response_times)
    response_df['DELTA'] = response_times

    # format these dates so they read more naturally
    response_df = filter_by_date(input_df=response_df, start_date=new_start, end_date=new_end)
    delta_mean = response_df['DELTA'].mean()
    delta_mean = format_time(delta_mean)
    delta_mean_out = 'Our average response time is : ' + str(delta_mean)

    # jonathan mean
    is_jonathan = response_df.loc[(response_df['FROM'] == 'Jonathan Lifferth')]
    jonathan_mean = is_jonathan['DELTA'].mean()
    jonathan_mean = format_time(jonathan_mean)
    jonathan_mean_out = "Jonathan's average response time is : " + str(jonathan_mean)

    # ben mean
    is_ben = response_df.loc[(response_df['FROM'] == 'Ben Darger')]
    ben_mean = is_ben['DELTA'].mean()
    ben_mean = format_time(ben_mean)
    ben_mean_out = "Ben's average response time is : " + str(ben_mean)

    return delta_mean_out, jonathan_mean_out, ben_mean_out


# display response times
st.text(calculate_response_times()[0])
st.text(calculate_response_times()[1])
st.text(calculate_response_times()[2])


def cheers_graph():
    fig2 = go.Figure(data=[go.Scatter(x=date, y=count)])
    fig2.update_layout(title_text="Daily Cheers Count", title_x=0.5,
                       title_font_size=30)
    fig2.update_layout(xaxis_title="Date",
                       yaxis_title="Daily Count")
    fig2.update_layout(
        autosize=False,
        width=750,
        height=500,
        margin=dict(l=50, r=50, b=100, t=100, pad=4)
    )
    #     paper_bgcolor="Grey"
    # other paper_bgcolors: "LightSteelBlue"
    st.plotly_chart(fig2)


cheers_graph()
if st.checkbox("Toggle balloons"):
    pass
else:
    st.balloons()

# display most recent update
last_update = cheers_df['DATETIME'].iloc[-1]
last_update = str(last_update).split(' ')
last_update = last_update[0]
last_update_message = 'Data was last updated from LinkedIn on ' + str(last_update)
col31, col32, col33 = st.columns([3, 8, 2])
with col31:
    st.write('')
with col32:
    st.write(last_update_message)
with col33:
    st.write('')
