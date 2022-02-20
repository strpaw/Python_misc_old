"""
Generate climate charts (diagrams) with average monthly temperature and precipitation.
Note:
    precipitation:
        - in mm,
        - range always from 0 to maximum monthly precipitation rounded up to nearest hundreds of mm respective to the
          maximum monthly precipitation in the whole data set, example:
          max monthly precipitation: 188 -> maximum range will be 200 mm
    temperature:
        - in Celsius degrees
        - range:
            - maximum always rounded up to nearest 5th of degrees respective to the maximum average monthly temperature
            in the whole data set, example:
             max monthly average temperature 21.2, max temperature range: 25 degrees
            - if minimum of average monthly temperature is >= O degrees in the whole data set: minimum range
            of temperature is 0
            - if minimum of average monthly temperature is < O degrees in the whole data set: minimum range
            of temperature is rounded down to nearest 5 degrees, example:
            - minimum average temperature in the whole data set is -11.5, minimum range on chart will be -15

Input data is CSV file with ';' delimiter, example:

Place;Element;Jan;Feb;Mar;Apr;May;Jun;Jul;Aug;Sep;Oct;Nov;Dec
Sydney;Temperature;23.5;23.4;22.1;19.5;16.6;14.2;13.4;14.5;17;18.9;20.4;22.1
Sydney;Precipitation;91.1;131.5;117.5;114.1;100.8;142;80.3;75.1;63.4;67.7;90.6;73
"""
from math import ceil, floor
from typing import Tuple
from sys import argv, exit
import numpy as np
import pandas
import pandas as pd
import matplotlib.pyplot as plt


def round_up(src_value: float, value: int) -> int:
    return ceil(src_value / value) * value


def round_down(src_value: float, value: int) -> int:
    return floor(src_value / value) * value


def get_max_monthly_precip(df: pandas.DataFrame) -> int:
    precip_df = df[df.index.get_level_values('Element') == 'Precipitation']
    return round_up(precip_df.to_numpy().max(), 100)


def get_temperature_range(df: pandas.DataFrame) -> Tuple[int, int]:
    temp_df = df[df.index.get_level_values('Element') == 'Temperature']
    temp_array = temp_df.to_numpy()

    t_min, t_max = temp_array.min(), temp_array.max()

    if t_min >= 0:
        t_min = 0
    else:
        t_min = round_down(t_min, 5)

    t_max = 5 * ceil(t_max / 5)

    return t_min, t_max


def usage():
    print('Usage:\nclimate_diagram_generator.py <climate_data.csv>')


if __name__ == "__main__":
    if len(argv) != 2:
        usage()
        exit(0)

    climate_data = pd.read_csv(argv[1], sep=';', index_col=['Place', 'Element'])
    places = set(climate_data.index.get_level_values(0))

    num_places = len(places)
    print(f'Found {num_places} places with climate data in source file')

    precip_max = get_max_monthly_precip(climate_data)
    temp_min, temp_max = get_temperature_range(climate_data)

    for i, place in enumerate(places, start=1):
        print(f'Creating diagram for {place}  [{i}/{num_places}]')
        place_data = climate_data.loc[place]
        temp_data = place_data.loc['Temperature']
        precip_data = place_data.loc['Precipitation']
        climate_diagram = plt.figure(dpi=600)

        temp_ax = climate_diagram.add_axes([0.1, 0.1, 0.4, 0.8])
        temp_ax.set_ylim(temp_min, temp_max)
        temp_ax.set_ylabel('°C')

        precip_ax = temp_ax.twinx()
        precip_ax.yaxis.tick_right()
        precip_ax.set_ylim(0, precip_max)
        precip_ax.yaxis.set_label_position('right')
        precip_ax.set_ylabel('mm')

        precip_ax.bar(np.arange(1, 13).astype(str), precip_data, color='b')
        temp_ax.plot(np.arange(1, 13).astype(str), temp_data, 'r')

        plt.savefig(f'{place}.jpg', bbox_inches='tight')
