import pandas as pd #version 2.1.4
from datetime import date # version 5.5

# %% load "Schweizerische Gesamtenergiestatistik"

# url 2023
url = "https://www.bfe.admin.ch/bfe/de/home/versorgung/statistik-und-geodaten/energiestatistiken/gesamtenergiestatistik.exturl.html/aHR0cHM6Ly9wdWJkYi5iZmUuYWRtaW4uY2gvZGUvcHVibGljYX/Rpb24vZG93bmxvYWQvNzUxOQ==.html"

# read excel sheet T14
# skip title rows of the excel table
df = pd.read_excel(url, sheet_name = 'T14', header=[0, 1, 2, 3], skiprows = 3)

# %% clean df

# flatten multilevel df levels
names_new = []
for col in df.columns:
    if 'Unnamed' in str(col[1]):
        name = col[0].replace(' ', '_')
    else:
        name = '_'.join((col[0], col[1])).replace(' ', '_')        
    names_new.append(name)

df.columns = names_new

# drop total columns, except for last column 'Total'
cols_tot = df.columns[df.columns.str.contains('_Total')]
df.drop(columns = cols_tot, inplace = True)

# clean col names
df.rename(columns = lambda x: x.strip('_'), inplace=True)
translation = str.maketrans({'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue' })
# remove numbers and umlaute
df.columns = df.columns.str.replace('\\d+', '', regex = True).str.translate(translation)

# drop nan rows -> also removes footer of table
df.dropna(inplace = True)

# replace '-' entries with pd.nan
df[df.columns[1:]] = df[df.columns[1:]].applymap(lambda x: pd.NA if x == '-' else x)

# %% change units from TJ to GWh

cols = df.columns

df[cols[1:]] = df[cols[1:]].apply(lambda x: x/3600 * 10**3)

# round to 0 digits
df[cols[1:]] = df[cols[1:]].applymap(lambda x: round(x, 0) if pd.notna(x) else x)

# %% melt df
# Jahr - Technologie - Endverbrauch_GWh

df_melt = df.melt(id_vars = ['Jahr'], var_name = 'Technologie', value_name = 'Endverbrauch_GWh')