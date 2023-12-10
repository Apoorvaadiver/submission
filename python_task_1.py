import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
  df=pd.read_csv("Downloads\dataset-1.csv")
       matrix = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
       matrix

    return matrix

    


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
 Create a new column 'car_type' based on 'car' column values
conditions = [
    (df['car'] <= 15),
    (df['car'] > 15) & (df['car'] <= 25),
    (df['car'] > 25)
]
choices = ['low', 'medium', 'high']
df['car_type'] = pd.Series(
    np.select(conditions, choices, default='Undefined'), index=df.index
)

# Calculate count of occurrences for each 'car_type'
type_count = df['car_type'].value_counts().to_dict()
# Sort the dictionary alphabetically based on keys
type_count_sorted = dict(sorted(type_count.items()))




    return type_count_sorted


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
bus_mean = df['bus'].mean()
bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
bus_indexes.sort()


    return bus_indexes
    return list()


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
route_avg_truck = df.groupby('route')['truck'].mean()
filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
filtered_routes.sort()


    return filtered_routes


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
modified= matrix.copy()
modified = modified.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
modified= modified.round(1)


    return modified


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
df['timestamp'] = pd.to_datetime(df['timestamp'])
time_duration = df.groupby(['id', 'id_2'])['timestamp'].agg(lambda x: x.max() - x.min())
time_check_list = (time_duration >= pd.Timedelta(days=7) - pd.Timedelta(hours=24))
filtered_df = df[df.set_index(['id', 'id_2']).index.isin(time_check_list[time_check_list].index)]


    return filtered_df
