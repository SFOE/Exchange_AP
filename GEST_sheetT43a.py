import pandas as pd #version 2.1.4
import datetime as dt
from datetime import date # version 5.5


# %% read BIP data from "Schweizerische Gesamtenergiestatistik"

# url 2023
url = "https://www.bfe.admin.ch/bfe/de/home/versorgung/statistik-und-geodaten/energiestatistiken/gesamtenergiestatistik.exturl.html/aHR0cHM6Ly9wdWJkYi5iZmUuYWRtaW4uY2gvZGUvcHVibGljYX/Rpb24vZG93bmxvYWQvNzUxOQ==.html"

# read excel sheet T43(a)
# skip title rows of the excel table
df = pd.read_excel(url, sheet_name = 'T43a', header=[0, 1, 2, 3], skiprows = 3)

# %% clean df

# flatten multilevel df levels
names_new = []
for col in df.columns:
    if 'Unnamed' in str(col[1]):
        name = col[0]
    else:
        name = '_'.join((col[0], col[1])).replace(' ', '_')        
    names_new.append(name)

df.columns = names_new

# drop rel columns
cols_tot = df.columns[df.columns.str.contains('_in_%')]
df.drop(columns = cols_tot, inplace = True)

# drop duplicate columns, keep first
df = df.loc[:, ~df.columns.duplicated(keep='first')]

# clean col names
names_new = ['Jahr', 
             'Heizgradtage_Anzahl',
             'BIP_(Preise_2020)_M_CHF',
             'Bevoelkerung_k',
             'rel_Index_indust_Prod_2020',
             'Wohnungen_neue_Gebaeude',
             'Gesamtwohnungsbestand_Anzahl', 
             'Motorfahrzeugbestand_Anzahl']

df.columns = names_new

# select columns of interest
df = df[['Jahr', 'Heizgradtage_Anzahl', 'BIP_(Preise_2020)_M_CHF']]

# drop nan rows -> also removes footer of table
df.dropna(inplace = True)