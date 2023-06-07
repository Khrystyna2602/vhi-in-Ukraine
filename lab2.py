import pandas as pd
from spyre import server

merged_df = pd.read_csv("D:\KPI\AD_lab\merged_file.csv")
class MyWebApp(server.App):
    title = "VHI in Ukraine"
    inputs = [
        {
            "type": "dropdown",
            "label": "Time series",
            "options":[
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"},
                {"label": "VHI", "value": "VHI"}
            ],
            "key": "time_series",
            "action_id": "update_data"
        },
        {
            "type": "dropdown",
            "label": "Region",
            "options": [
                {"label": "Vinnytska", "value": "1"},
                {"label": "Volynska", "value": "2"},
                {"label": "Dnipropetrovska", "value": "3"},
                {"label": "Donetska", "value": "4"},
                {"label": "Zhytomyrska", "value": "5"},
                {"label": "Zakarpatska", "value": "6"},
                {"label": "Zaporizka", "value": "7"},
                {"label": "Ivano-Frankivska", "value": "8"},
                {"label": "Kyivska", "value": "9"},
                {"label": "Kirovohradska", "value": "10"},
                {"label": "Luhanska", "value": "11"},
                {"label": "Lvivska", "value": "12"},
                {"label": "Mykolaivska", "value": "13"},
                {"label": "Odeska", "value": "14"},
                {"label": "Poltavska", "value": "15"},
                {"label": "Rivenska", "value": "16"},
                {"label": "Sumska", "value": "17"},
                {"label": "Ternopilska", "value": "18"},
                {"label": "Kharkivska", "value": "19"},
                {"label": "Khersonska", "value": "20"},
                {"label": "Khmelnytska", "value": "21"},
                {"label": "Cherkaska", "value": "22"},
                {"label": "Chernivetska", "value": "23"},
                {"label": "Chernihivska", "value": "24"},
                {"label": "Republic of Crimea", "value": "25"}
            ],
            "key": "region",
            "action_id": "update_data"
        },
        {
            "type": "text",
            "label": "Start week",
            "value": "1",
            "key": "start_week",
            "action_id": "update_data"
        },
        {
            "type": "text",
            "label": "End week",
            "value": "52",
            "key": "end_week",
            "action_id": "update_data"
        }
    ]
    tabs = ["Plot", "Table"]
    controls = [{
        "type": "button",
        "id": "update_data",
        "label": "Get information"
    }]

    outputs = [
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        },
        {
            "type": "plot",
            "id": "plot_id",
            "control_id": "update_data",
            "tab": "Plot"
        }
    ]

    def getData(self, params):
        time_series = params['time_series']
        region = params['region']
        start_week = int(params['start_week'])
        end_week = int(params['end_week'])

        data = merged_df[(merged_df['new index'] == int(region))][['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'new index']]
        if time_series == 'VCI':
            data = data[['Year', 'Week', 'VCI']]
        elif time_series == 'TCI':
            data = data[['Year', 'Week', 'TCI']]
        else:
            data = data[['Year', 'Week', 'VHI']]
        data = data[(data['Week'] >= start_week) & (data['Week'] <= end_week)]
        return data

    def getPlot(self, params):
        df = self.getData(params)
        plt_obj = df.plot(y=params['time_series'], x='Year')
        plt_obj.set_ylabel(params['time_series'])
        plt_obj.set_xlabel("Year")
        return plt_obj.get_figure()

app = MyWebApp()
app.launch()
