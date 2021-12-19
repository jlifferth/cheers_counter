import pandas as pd
import plotly.graph_objects as go

from functions import *

st.title('Cheers Counter')

# define date filter
filter_start = "2021-05-01"
filter_end = "2021-12-01"

filtered_df = filter_by_date(input_df=by_day, start_date=filter_start, end_date=filter_end)
st.dataframe(filtered_df)
date = filtered_df['DATETIME']
count = filtered_df['COUNT']
date = np.array(date)
count = np.array(count)
st.write(count)

fig1 = plt.figure(figsize=(10, 7))
plt.plot(date, count)
plt.style.use('fivethirtyeight')
st.pyplot(fig1)

fig2 = go.Figure(
    data=[go.Scatter(x=date, y=count)]
)
fig2.update_layout(title_text="Daily Cheers Count",
                   title_font_size=30)
fig2.update_layout(
    autosize=False,
    width=700,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    )
)
#
#     paper_bgcolor="Grey"
# other paper_bgcolors: "LightSteelBlue"

st.plotly_chart(fig2)


def line_plot():
    # Create numpy array for the visualisation
    x = np.array([5, 7, 8, 7, 2, 17, 2, 9, 4, 11, 12, 9, 6])
    y = np.array([99, 86, 87, 88, 111, 86, 103, 87, 94, 78, 77, 85, 86])

    fig = plt.figure(figsize=(10, 4))
    plt.plot(x, y)

    st.balloons()
    st.pyplot(fig)


st.info('This is a purely informational message')
# line_plot()

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=['a', 'b', 'c'])

st.balloons()
