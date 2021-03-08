import dash_table
import dataPreprocess
import pandas as pd
from datetime import timedelta

tmp_df = dataPreprocess.data_load()


df9 = tmp_df[3][['CustomerID', 'Country']]
df11 = tmp_df[1][['CustomerID', 'RFM_Score', 'RFM_Level']]
df9.drop_duplicates(subset = ['CustomerID'], inplace=True)
df12 = pd.merge(df11, df9, on='CustomerID', how='left')


def tbl_layout():    
    tbl_score = dash_table.DataTable(
        id='id_score',
        columns=[{"name": i, "id": i} for i in tmp_df[0].columns],
        data=tmp_df[0].to_dict('records'),

        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },

        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        row_deletable=True,
        selected_columns=[],
        selected_rows=[],
        page_action="native",
        page_current= 0,
        page_size= 10,
    )

    tbl_RFMVal = dash_table.DataTable(
        id='id_RFMVal',
        #columns=[{"name": i, "id": i} for i in tmp_df[1].columns],
        columns=[{"name": i, "id": i} for i in df12.columns],
        #data=tmp_df[1].to_dict('records'),
        data = df12.to_dict('records'),
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold',
            #'border': '1px solid black'
        },

        # editable=True,
        filter_action="native",
        sort_action="native",
        # sort_mode="multi",
        # column_selectable="single",
        #row_selectable="multi",
        # row_deletable=True,
        # selected_columns=[],
        # selected_rows=[],
        # page_action="native",
        page_current= 0,
        page_size= 6,
    )

    tbl_RFMAggregate = dash_table.DataTable(
        id='id_RFMAggregate',
        columns=[{"name": i, "id": i} for i in tmp_df[2].columns],
        data=tmp_df[2].to_dict('records'),

        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }

        # editable=True,
        # filter_action="native",
        # sort_action="native",
        # sort_mode="multi",
        # column_selectable="single",
        # row_selectable="multi",
        # row_deletable=True,
        # selected_columns=[],
        # selected_rows=[],
        # page_action="native",
        # page_current= 0,
        # page_size= 10,
    )

    return [tbl_score, tbl_RFMVal, tbl_RFMAggregate]


