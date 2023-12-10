import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
unique_ids = pd.unique(df[['id_start', 'id_end']].values.flatten())
distance_matrix = pd.DataFrame(index=unique_ids, columns=unique_ids, dtype=float)

distance_matrix.values[[range(len(unique_ids))]*2] = 0

for index, row in df.iterrows():
    id_start, id_end, distance = row['id_start'], row['id_end'], row['distance']
    distance_matrix.at[id_start, id_end] += distance
    distance_matrix.at[id_end, id_start] += distance


    return distance_matrix


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
result_matrix = df.reset_index()
unrolled_df = pd.melt(result_matrix, id_vars=['id_start'], var_name='id_end', value_name='distance')


    return unrolled_df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
reference_rows = df[(df['id_start'] == reference_id) | (df['id_end'] == reference_id)]
reference_average_distance = reference_rows['distance'].mean()
lower_bound = reference_average_distance * 0.9
upper_bound = reference_average_distance * 1.1
similar_ids_df = unrolled_df[
(unrolled_df['distance'] >= lower_bound) & (unrolled_df['distance'] <= upper_bound)
]


    return similar_ids_df


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
for vehicle_type, rate_coefficient in rate_coefficients.items():
    df[vehicle_type] = df['distance'] * rate_coefficient

    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
time_ranges = [(time(0, 0, 0), time(10, 0, 0), 0.8),
(time(10, 0, 0), time(18, 0, 0), 1.2),
(time(18, 0, 0), time(23, 59, 59), 0.8)]
weekend_discount_factor = 0.7

df['start_day'] = 'Monday'
df['end_day'] = 'Sunday'
df['start_time'] = time(0, 0, 0)
df['end_time'] = time(23, 59, 59)

for start_time, end_time, discount_factor in time_ranges:
    df.loc[(df['start_time'] >= start_time) & (df['end_time'] <= end_time) & 
           (df['start_day'].isin(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])), 
           ['moto', 'car', 'rv', 'bus', 'truck']] *= discount_factor
df.loc[df['start_day'].isin(['Saturday', 'Sunday']), 
       ['moto', 'car', 'rv', 'bus', 'truck']] *= weekend_discount_factor

    return df
