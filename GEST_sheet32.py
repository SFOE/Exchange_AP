import pandas as pd #version 2.1.4
from datetime import date # version 5.5


# %% load "Schweizerische Gesamtenergiestatistik"

# url 2023
url = "https://www.bfe.admin.ch/bfe/de/home/versorgung/statistik-und-geodaten/energiestatistiken/gesamtenergiestatistik.exturl.html/aHR0cHM6Ly9wdWJkYi5iZmUuYWRtaW4uY2gvZGUvcHVibGljYX/Rpb24vZG93bmxvYWQvNzUxOQ==.html"

# read excel sheet T32
# skip title rows of the excel table
df = pd.read_excel(url, sheet_name = 'T32', header=[0, 1, 2, 3], skiprows = 3)

# %% clean df

# flatten multilevel df levels
df.columns = ['_'.join(col).replace(' ', '_') for col in df.columns]

# change to select desired columns #
# select columns of interest
col_year = df.columns[df.columns.str.contains('Jahr')]
col_pv_tot = df.columns[df.columns.str.contains('Elektrizitätsproduktion_(GWh)_Total', regex = False)]
cols = col_year.tolist() + col_pv_tot.tolist()

df = df[cols]

# rename columns
col_names = ['Jahr', 'Elektrizitaetsproduktion_Total_GWh']
df.columns = col_names

# drop nan to remove bottom rows of text
df.dropna(inplace = True)