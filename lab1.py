import urllib.request
import pandas as pd
from datetime import datetime

df_region_list = []
region_id_fixed = {1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21, 11: 9, 12: 9.1, 13: 10, 14: 11,
                   15: 12, 16: 13, 17: 14, 18: 15, 19: 16, 20: 25.1, 21: 17, 22: 18, 23: 6, 24: 1, 25: 2, 26: 7, 27: 5}

response = input('Завантажити інформацію з сайту? (Так/Ні) : ')
if response == 'Так':
    for i in range (1, 28):
        url = f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={i}&year1=1981&year2=2023&type=Mean'
        text = urllib.request.urlopen(url).read()
        text = text.replace(b'<tt><pre>', b'')
        text = text.replace(b'</pre></tt>', b'')
        current_time = datetime.now()
        current_date_time = current_time.strftime("%d%m%Y%H%M%S")
        filename = 'Region'+str(i)+'_'+current_date_time+'.csv'
        with open(filename, 'wb') as out :
            out.write(text)
            out.close
        headers = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty']
        df = pd.read_csv(filename,header=1,names=headers)
        df = df.drop(df.loc[df['VHI'] == -1].index)
        df = df.drop('empty', axis=1)

        df['old index'] = i
        df['new index'] = region_id_fixed[i]

        df_region_list.append(df)

    merged_df = pd.concat(df_region_list, axis=0, ignore_index=True)
    merged_df.to_csv("merged_file.csv", index=False)
else:
    file_path = "D:\KPI\Засоби підготовки та аналізу даних\AD_lab\merged_file.csv"
    merged_df = pd.read_csv(file_path)

print(merged_df.head())
print(merged_df.tail())
print('Індекси областей: \n1 Вінницька\n2 Волинська\n3 Дніпропетровська \n4 Донецька\n5 Житомирська\n6 Закарпатська\n7 Запорізька\n8 Івано-Франківська\n9 Київська\n10 Кіровоградська\n11 Луганська\n12 Львівська\n13 Миколаївська\n14 Одеська\n15 Полтавська\n16 Рівенська\n17 Сумська\n18 Тернопільська\n19 Харківська\n20 Херсонська\n21 Хмельницька\n22 Черкаська\n23 Чернівецька\n24 Чернігівська\n25 Республіка Крим')

region=float(input("Введіть індекс: "))
year=int(input("Введіть рік: "))
vhi_data = merged_df[(merged_df['new index'] == region) & (merged_df["Year"] == year)][["VHI", 'Week']]
print(vhi_data)
print("Мінімальне значення VHI: ", vhi_data.min()[0],"week:",vhi_data[(vhi_data["VHI"]==vhi_data.min()[0])]['Week'].values[0])
print("Максимальне значення VHI: ", vhi_data.max()[0],"week:",vhi_data[(vhi_data["VHI"]==vhi_data.max()[0])]['Week'].values[0])
vhi_data_severe=merged_df[(merged_df['new index'] == region) & (merged_df["VHI"] <= 15)][["VHI", 'Year']]["Year"].unique()
print("Роки з екстримальними посухами (менше 15%): ", vhi_data_severe)
vhi_data_moderate = merged_df[(merged_df['new index'] == region) & (merged_df["VHI"] <= 35) & (merged_df["VHI"] >= 15)][["VHI", 'Year']]["Year"].unique()
print("Роки з помірними посухами (менше 35% та більше 15%): ", vhi_data_moderate)