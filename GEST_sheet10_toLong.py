import pandas as pd #version 2.1.4
from datetime import date # version 5.5

# %% load "Schweizerische Gesamtenergiestatistik"

# url 2023
url = "https://www.bfe.admin.ch/bfe/de/home/versorgung/statistik-und-geodaten/energiestatistiken/gesamtenergiestatistik.exturl.html/aHR0cHM6Ly9wdWJkYi5iZmUuYWRtaW4uY2gvZGUvcHVibGljYX/Rpb24vZG93bmxvYWQvNzUxOQ==.html"

# read excel sheet T10
# skip title rows of the excel table
df = pd.read_excel(url, sheet_name = 'T10', header=[0, 1, 2], skiprows = 3)

# %% clean df

# flatten multilevel df levels
df.columns = ['_'.join((col[0], col[2])).replace(' ', '_') for col in df.columns]

# drop relative columns
cols_rel = df.columns[df.columns.str.contains('%')]
df.drop(columns = cols_rel, inplace = True)

# change here to keep more/other columns
# drop further unused columns
names = ['davon_Rohöl', 'davon_Erdölprodukte', 'Gesamter_Energieeinsatz', 'Elektrizität_Import/Export-Saldo', 'Inländischer_Brutto-energie-verbrauch_(100%)']
for name in names:
    df.drop(columns = df.columns[df.columns.str.contains(name, regex = False)], inplace = True)
    
# clean col names
df.rename(columns = lambda x: x.strip('_'), inplace=True)
df.rename(columns = {df.columns[0]: 'Jahr'}, inplace = True)
translation = str.maketrans({'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'Ä': 'Ae', 'Ö': 'Oe', 'Ü': 'Ue' })
# remove numbers and umlaute
df.columns = df.columns.str.replace('\\d+', '', regex = True).str.translate(translation)
# replace ' ' with '_' and remove _TJ
df.columns = df.columns.str.replace(' ', '_').str.replace('_TJ', '')

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
# Jahr - Technologie - Verbrauch_GWh

df_melt = df.melt(id_vars = ['Jahr'], var_name = 'Technologie', value_name = 'Verbrauch_GWh')