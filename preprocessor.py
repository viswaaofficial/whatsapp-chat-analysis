import re
import pandas as pd

def preprocess(data):
    # Define the regex pattern to match the date and time
    pattern = '(\d{1,2}/\d{1,2}/\d{2,4}, \d{1,2}:\d{2}) - '

    # Split the data into messages and dates
    splits = re.split(pattern, data)
    dates = [split for i, split in enumerate(splits) if i % 2 == 1]
    messages = [split for i, split in enumerate(splits) if i % 2 == 0][1:]

    # Create a DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert message_date to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M')

    # Extract user and message from user_message
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(':\s', message, maxsplit=1)
        if len(entry) > 1:
            users.append(entry[0])
            messages.append(entry[1])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Extract additional date and time information
    df['only_date'] = df['message_date'].dt.date
    df['year'] = df['message_date'].dt.year
    df['month_num'] = df['message_date'].dt.month
    df['month'] = df['message_date'].dt.strftime('%B')
    df['day'] = df['message_date'].dt.day
    df['day_name'] = df['message_date'].dt.strftime('%A')
    df['hour'] = df['message_date'].dt.hour
    df['minute'] = df['message_date'].dt.minute

    # Create a period column
    df['period'] = df['hour'].apply(lambda x: f"{x:02d}-{(x + 1) % 24:02d}")

    return df


