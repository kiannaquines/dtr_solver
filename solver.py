import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

df = pd.read_csv('/content/drive/MyDrive/Kian_Jearard_Naquines_DTR - Kian_Jearard_Naquines-Final.csv')
df.head(50)

df['DateTime'] = pd.to_datetime(df['Time'], format='%d/%m/%Y %H:%M')
df[['Person ID','Name','DateTime','Attendance Status','Attendance Check Point','Custom Name','Data Source']]

df['Date'] = df['DateTime'].dt.date
transformed_df = df[['Person ID','Name','DateTime','Attendance Status','Attendance Check Point','Custom Name','Data Source','Date']]

def calculate_total_hours(group_data):
    person_id = group_data['Person ID'].iloc[0]
    name = group_data['Name'].iloc[0]
    department = group_data['Attendance Check Point'].iloc[0]

    checkins = group_data[group_data['Attendance Status'] == 'Check-in']['DateTime'].tolist()
    checkouts = group_data[group_data['Attendance Status'] == 'Check-out']['DateTime'].tolist()

    morning = afternoon = 0

    if len(checkins) >= 1 and len(checkouts) >= 1:
        try:
            morning = (checkouts[0] - checkins[0]).total_seconds() / 3600
        except:
            pass
        if len(checkins) > 1 and len(checkouts) > 1:
            try:
                afternoon = (checkouts[1] - checkins[1]).total_seconds() / 3600
            except:
                pass

    return pd.Series({
        'Person': person_id,
        'Name': name,
        'Department': department,
        'Morning Hours': round(morning, 2) if morning else None,
        'Afternoon Hours': round(afternoon, 2) if afternoon else None,
        'Total Hours': round(morning + afternoon, 2) if morning or afternoon else None
    })

result = transformed_df.groupby(['Date']).apply(calculate_total_hours).reset_index()
result['Total Hours'].plot(kind='line', figsize=(8, 4), title='Total Hours')
plt.gca().spines[['top', 'right']].set_visible(False)

result['Afternoon Hours'].plot(kind='line', figsize=(8, 4), title='Afternoon Hours')
plt.gca().spines[['top', 'right']].set_visible(False)

result['Morning Hours'].plot(kind='line', figsize=(8, 4), title='Morning Hours')
plt.gca().spines[['top', 'right']].set_visible(False)


def _plot_series(series, series_name, series_index=0):
  palette = list(sns.palettes.mpl_palette('Dark2'))
  xs = series['Date']
  ys = series['Afternoon Hours']

  plt.plot(xs, ys, label=series_name, color=palette[series_index % len(palette)])

fig, ax = plt.subplots(figsize=(10, 5.2), layout='constrained')
df_sorted = result.sort_values('Date', ascending=True)
_plot_series(df_sorted, '')
sns.despine(fig=fig, ax=ax)
plt.xlabel('Date')
_ = plt.ylabel('Afternoon Hours')


def _plot_series(series, series_name, series_index=0):
  palette = list(sns.palettes.mpl_palette('Dark2'))
  xs = series['Date']
  ys = series['Morning Hours']

  plt.plot(xs, ys, label=series_name, color=palette[series_index % len(palette)])

fig, ax = plt.subplots(figsize=(10, 5.2), layout='constrained')
df_sorted = result.sort_values('Date', ascending=True)
_plot_series(df_sorted, '')
sns.despine(fig=fig, ax=ax)
plt.xlabel('Date')
_ = plt.ylabel('Morning Hours')


total_hours_calculated = result['Total Hours'].sum()
print(f"OJT Total Hours: {total_hours_calculated} hours")
remaining_hours_calculated = 486 - total_hours_calculated
print(f"OJT Remaining Hours: {remaining_hours_calculated} hours")
