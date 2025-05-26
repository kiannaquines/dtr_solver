import pandas as pd

df = pd.read_csv('Attendance.csv')
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
        # 'Person': person_id,
        'Name': name,
        # 'Department': department,
        'Morning Hours': round(morning, 2) if morning else None,
        'Afternoon Hours': round(afternoon, 2) if afternoon else None,
        'Total Hours': round(morning + afternoon, 2) if morning or afternoon else None
    })

result = transformed_df.groupby(['Date']).apply(calculate_total_hours).reset_index()
result.to_csv('final_hours_of_ojt.csv', index=False)
total_hours_calculated = result['Total Hours'].sum()
print(f"OJT Total Hours: {total_hours_calculated:.2f} hours")
