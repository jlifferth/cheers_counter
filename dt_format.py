from main import calculate_response_times
import plotly
print(plotly.__version__)

# space to practice datetime formatting for average response time outputs
# print(calculate_response_times()[0])
# print(calculate_response_times()[1])
# print(calculate_response_times()[2])

# mean1 = calculate_response_times()[0]


def format_time(input):
    input = str(input).split(' ')
    time_str = input[2].split(':')
    final = input[0] + ' ' + input[1] + ', ' + time_str[0] + ' hours, and ' + time_str[1] + ' minutes'
    return final


# print(format_time(mean1))
