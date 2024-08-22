

import pandas as pd
# from sqlalchemy import true
import xlsxwriter
import os
import datetime
# from django.core.files.storage import default_storage
path = os.getcwd()


def set_up(dataframe, style='default'):
    '''  The default is .title as in Dataframe

        Others are :
        -- lower, upper,' ' and nothing
    '''
    if style == 'lower':
        dataframe.columns = [x.lower() for x in dataframe.columns]
    elif style == 'upper':
        dataframe.columns = [x.upper() for x in dataframe.columns]
    elif style == 'nothing':
        dataframe.columns = [x for x in dataframe.columns]
    else:
        dataframe.columns = [x.title() for x in dataframe.columns]

    for colname in dataframe.columns:
        try:
            dataframe[colname] = dataframe[colname].astype('float')
            # print(f"{colname} converted")
        except ValueError:
            # print(f"{colname} failed")
            _ = 1
            pass


def format_img(x='', out=False, custom=''):

    if out:
        out = '_out'
    elif custom != '':
        out = custom
    else:
        out = '_in'

    l = x.strip('.png') + out + '.png'

    return l



REGULAR_SIZE = 11
REGULAR_FONT = 'Cambria'


def default_format(workbook):
    default = workbook.add_format({
        'font_name': REGULAR_FONT,
        'font_size': REGULAR_SIZE,
        'valign': 'top',
        'align': 'left'
    })
    return default


def text_box_wrap_format(workbook):
    text_box_wrap = workbook.add_format({
        'font_name': REGULAR_FONT,
        'font_size': REGULAR_SIZE,
        'align': 'justify',
        'valign': 'vcenter',
        'border': True,
        'text_wrap': True
    })
    return text_box_wrap


def text_box_no_wrap_format(workbook):
    text_box_center_wrap = workbook.add_format({
        'font_name': "Cambria Bold",
        'font_size': REGULAR_SIZE,
        'align': 'center',
        'valign': 'vcenter',
        "bg_color": '#6d9bc3',
    })
    return text_box_center_wrap


def text_box_center_wrap_format(workbook):
    text_box_center_wrap = workbook.add_format({
        'font_name': "Cambria Bold",
        'font_size': REGULAR_SIZE,
        'align': 'center',
        'valign': 'vcenter',
        "bg_color": '#2196F3',
        "color": '#fffff',
    })
    return text_box_center_wrap


def no_format(workbook):
    text_box_center_wrap = workbook.add_format({
        'font_name': REGULAR_FONT,
        'font_size': REGULAR_SIZE,
        'align': 'center',
        'valign': 'vcenter',
        'border': True,
        'text_wrap': True
    })
    return text_box_center_wrap


def yellow_highlighting_format(workbook):
    text_box_center_wrap = workbook.add_format({
        'font_name': REGULAR_FONT,
        'font_size': REGULAR_SIZE,
        'align': 'left',
        'bold': True,
        'color':'white',
        'bg_color':"gray"
    })
    return text_box_center_wrap

def blue_highlighting_format(workbook):
    text_box_center_wrap = workbook.add_format({
        'font_name': REGULAR_FONT,
        'font_size': REGULAR_SIZE,
        'align': 'left',
        'bold': True,
        'color':'white',
        'bg_color':"blue"
    })
    return text_box_center_wrap

def bold_highlighting_format(workbook):
    text_box_center_wrap = workbook.add_format({
        'font_name': REGULAR_FONT,
        'font_size': REGULAR_SIZE,
        'align': 'left',
        'bold': True,
    })
    return text_box_center_wrap


def cumm_format(workbook):
    text_box_center_wrap = workbook.add_format({
        'font_name': REGULAR_FONT,
        'font_size': REGULAR_SIZE,
        'align': 'left',
    })
    return text_box_center_wrap


def header_format(workbook,extra={}):
    default = workbook.add_format({
        'font_name': REGULAR_FONT,
        'font_size': 13,
        'align': 'center',
        'valign': 'vcenter',
        'color':'white',
        **extra
    })
    return default


def sub_header_format(workbook):
    default = workbook.add_format({
        'font_name': 'Calibri Light',
        'font_size': 12,
        'valign': 'top',
        'color':'white',
        'align': 'left',
    })
    return default


def create_excel(scenario='',  branchId=111, accountId=1111, 
    sheet1: tuple = (), 
    sheet2: tuple = (), 
    sheet3: list = [], 
    sheet4: list = [], 
    sheet5: list = [],  
    sheet6: list = [],  
    sheet7: list = [],  
    sheet8: list = [],  
    sheet9: list = [],  
    sheet10: list = [],  
    pretiffy=False, 
    charts: dict = {"in_pie": "pie.png", "bar": "bars.png", "out_pie": "out.png", "time": "time.png", "amount": "amount.png", "comp_amount": 'ex_amount.png', "comp_count": 'ex_count.png'}):
    

    locn =  os.path.abspath(os.path.dirname(__file__))
    date = datetime.datetime.now().strftime('%d%b%Y%H%M%S%f') 
    file_n = '{}-{}-{}.xlsx'.format(branchId, accountId,date)

    filename = os.path.join(locn,'analytics',file_n)
    print('EXCEL LOCATION',filename)
    workbook = xlsxwriter.workbook.Workbook(filename)
    header = "{} for Customer Account: {} in Branch: {}".format(scenario, accountId, branchId).upper()

    df = pd.DataFrame(
        data=sheet1['data'],
        columns=sheet1['columns'] )

    set_up(df)

    sheet_1 = 'Inflow - Outflow Analytics'
    worksheet = workbook.add_worksheet(sheet_1.upper())

    worksheet.merge_range("A2:K2", header, header_format(workbook,{'bold':True,'color':"white",'bg_color':'blue'}))

    row = 0
    col = 0

    space = 3

    values = df.values.tolist()
    columns = df.columns.tolist()

    if pretiffy:
        for i, column in enumerate(columns):
            column_width = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            worksheet.set_column(col_idx + space, col_idx, 25) 
    
        # col_idx = df.columns.get_loc('Today')
        # worksheet.set_column(col_idx + space, col_idx, 15) 

        # col_idx = df.columns.get_loc('Above 6 Months - 1 Year')
        # worksheet.set_column(col_idx + space, col_idx, 25) 


    for col, data in enumerate(columns):
        worksheet.write(space, col, data,text_box_center_wrap_format(workbook))

    for row_num, row_data in enumerate(values):
        row_num += space + 1
        for col_num, col_data in enumerate(row_data):
            if col_num ==0:
                worksheet.write(row_num, 0, col_data,
                                bold_highlighting_format(workbook))

            if row_data[0].count("Total Inflow") > 0 or row_data[0].count("Total Outflow") > 0 or row_data[0].count("Frequency Count") > 0:
                worksheet.write(row_num, col_num, col_data,
                                yellow_highlighting_format(workbook))
            elif row_data[0].count("Metric") > 0 :
                worksheet.write(row_num, col_num, col_data,
                                blue_highlighting_format(workbook))
            elif row_data[0].count("Cummulative") > 0 or row_data[0].count("Cummulative") > 0:
                worksheet.write(row_num, col_num, col_data,
                                cumm_format(workbook))
            else:
                worksheet.write(row_num, col_num, col_data,
                                default_format(workbook))





    sheet_2 = "Dashboard IN-OUT Flow Amount"
    worksheet = workbook.add_worksheet(sheet_2.upper())

    worksheet.merge_range("A2:J2", 'Amount Transaction Types (Inflow)' , header_format(workbook,{ "bg_color": '#2196F3',"color": '#fffff'}))
    worksheet.merge_range("L2:U2", 'Amount Transaction Types (Outflow)' , header_format(workbook,{ "bg_color": 'purple',"color": '#fffff'}))
    worksheet.merge_range("A23:U23", 'IN-OUT Flow Amount' , header_format(workbook,{ "bg_color": 'brown',"color": '#fffff'}))

    worksheet.insert_image(2,0, sheet2[0], {'x_scale': 0.8, 'y_scale': 0.7})
    worksheet.insert_image(2,11, sheet2[1], {'x_scale': 0.8, 'y_scale': 0.7})
    worksheet.insert_image(23,0, sheet2[2], {'x_scale': 1.7 })


    sheet_3 = "Dashboard IN-OUT Flow Freq."
    worksheet = workbook.add_worksheet(sheet_3.upper())

    worksheet.merge_range("A2:J2", 'Freq. Transaction Types (Inflow)' , header_format(workbook,{ "bg_color": '#2196F3',"color": '#fffff'}))
    worksheet.merge_range("L2:U2", 'Freq. Transaction Types (Outflow)' , header_format(workbook,{ "bg_color": 'purple',"color": '#fffff'}))
    worksheet.merge_range("A23:U23", 'IN-OUT Flow Freq.' , header_format(workbook,{ "bg_color": 'brown',"color": '#fffff'}))

    worksheet.insert_image(2,0, sheet3[0], {'x_scale': 0.8, 'y_scale': 0.7})
    worksheet.insert_image(2,11, sheet3[1], {'x_scale': 0.8, 'y_scale': 0.7})
    worksheet.insert_image(23,0, sheet3[2], {'x_scale': 1.7 })


    

    sheet_4 = 'Inflow Exceptions'
    worksheet = workbook.add_worksheet(sheet_4.upper())

    df = pd.DataFrame(data=sheet4[0]["data"],columns=sheet4[0]["columns"] )
    set_up(df) 
    worksheet.merge_range("A2:I2", header, header_format(workbook,{'bold':True,'color':"white",'bg_color':'blue'}))

    row = 0
    col = 0

    space = 3

    values = df.values.tolist()
    columns = df.columns.tolist()

    if pretiffy:
        

        for i, column in enumerate(columns):
            column_width = max(df[column].astype(
                str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            worksheet.set_column(col_idx + space, col_idx, column_width)

        col_idx = df.columns.get_loc('Expected')
        worksheet.set_column(col_idx + space, col_idx, 25) 
       
        

    for col, data in enumerate(columns):
        worksheet.write(space, col, data,text_box_center_wrap_format(workbook))

    for row_num, row_data in enumerate(values):
        row_num += space + 1
        for col_num, col_data in enumerate(row_data):
            if col_num ==0:
                worksheet.write(row_num, 0, col_data,
                                bold_highlighting_format(workbook))

            if row_data[0].count("Total No. of Records"):
                worksheet.write(row_num, col_num, col_data,
                                yellow_highlighting_format(workbook)) 
            elif row_data[0].count("Metric") > 0 :
                worksheet.write(row_num, col_num, col_data,
                                blue_highlighting_format(workbook))
            else:
                worksheet.write(row_num, col_num, col_data,
                                default_format(workbook))


    worksheet.merge_range("A18:C18", 'Inflow (Amount Involved)' , header_format(workbook,{ "bg_color": 'brown',"color": '#fffff'}))
    worksheet.merge_range("D18:I18", 'Inflow Risk Assessment' , header_format(workbook,{ "bg_color": 'green',"color": '#fffff'}))
    worksheet.merge_range("A37:I37", '3 - Month Inflow Analysis' , header_format(workbook,{ "bg_color": 'purple',"color": '#fffff'}))

    worksheet.insert_image(18,0, sheet4[1], {'x_scale': 0.55, 'y_scale': 0.6})
    worksheet.insert_image(18,3, sheet4[3], {'x_scale': 0.6, 'y_scale': 0.6})
    worksheet.insert_image(39,0, sheet4[2], {'x_scale': 1.4}) 





    sheet_5 = 'Outflow Exceptions'
    worksheet = workbook.add_worksheet(sheet_5.upper())

    df = pd.DataFrame(data=sheet5[0]["data"],columns=sheet5[0]["columns"] )
    set_up(df) 
    worksheet.merge_range("A2:I2", header, header_format(workbook,{'bold':True,'color':"white",'bg_color':'blue'}))

    row = 0
    col = 0

    space = 3

    values = df.values.tolist()
    columns = df.columns.tolist()

    if pretiffy:
        for i, column in enumerate(columns):
            column_width = max(df[column].astype(
                str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            worksheet.set_column(col_idx + space, col_idx, column_width)

        col_idx = df.columns.get_loc('Expected')
        worksheet.set_column(col_idx + space, col_idx, 25) 

    for col, data in enumerate(columns):
        worksheet.write(space, col, data,
                        text_box_center_wrap_format(workbook))

    for row_num, row_data in enumerate(values):
        row_num += space + 1
        for col_num, col_data in enumerate(row_data):
            if col_num ==0:
                worksheet.write(row_num, 0, col_data,
                                bold_highlighting_format(workbook))

            if row_data[0].count("Total No. of Records"):
                worksheet.write(row_num, col_num, col_data,
                                yellow_highlighting_format(workbook)) 
            elif row_data[0].count("Metric") > 0 :
                worksheet.write(row_num, col_num, col_data,
                                blue_highlighting_format(workbook))
            else:
                worksheet.write(row_num, col_num, col_data,
                                default_format(workbook))
            



    worksheet.merge_range("A18:C18", 'Outflow (Amount Involved)' ,header_format(workbook,{ "bg_color": 'brown',"color": '#fffff'}))
    worksheet.merge_range("D18:I18", 'Outflow Risk Assessment' , header_format(workbook,{ "bg_color": 'green',"color": '#fffff'}))
    worksheet.merge_range("A37:I37", '3 - Month Outflow Analysis' , header_format(workbook,{ "bg_color": 'purple',"color": '#fffff'}))

    worksheet.insert_image(18,0, sheet5[1], {'x_scale': 0.55, 'y_scale': 0.6})
    worksheet.insert_image(18,3, sheet5[3], {'x_scale': 0.55, 'y_scale': 0.6})
    worksheet.insert_image(39,0, sheet5[2], {'x_scale': 1.4})


 







    sheet_6 = 'Time Series Inflow (Amount)'
    worksheet = workbook.add_worksheet(sheet_6.upper()) 

    df = pd.DataFrame(data=sheet6[0]["data"],columns=sheet6[0]["columns"] )
    set_up(df) 
    worksheet.merge_range("A2:Z2", header, header_format(workbook,{'bold':True,'color':"white",'bg_color':'blue'}))

    row = 0
    col = 0

    space = 3

    values = df.values.tolist()
    columns = df.columns.tolist()

    if pretiffy:
        for i, column in enumerate(columns):
            column_width = max(df[column].astype(
                str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            worksheet.set_column(col_idx + space, col_idx, 12 )

        # col_idx = df.columns.get_loc('Metric')
        # worksheet.set_column(col_idx + space, col_idx, 17) 

        # col_idx = df.columns.get_loc('12Am')
        # worksheet.set_column(col_idx + space, col_idx, 8) 



    for col, data in enumerate(columns):
        worksheet.write(space, col, data,
                        text_box_center_wrap_format(workbook))

    for row_num, row_data in enumerate(values):
        row_num += space + 1
        for col_num, col_data in enumerate(row_data):
            if col_num ==0:
                worksheet.write(row_num, 0, col_data,
                                bold_highlighting_format(workbook))

            if row_data[0].count("Total"):
                worksheet.write(row_num, col_num, col_data,
                                yellow_highlighting_format(workbook)) 
            elif row_data[0].count("Metric") > 0 :
                worksheet.write(row_num, col_num, col_data,
                                blue_highlighting_format(workbook))
            else:
                worksheet.write(row_num, col_num, col_data,
                                default_format(workbook))


    worksheet.merge_range("A13:O13", '3 - Month Inflow Time Series (Amount)' , header_format(workbook,{'color':"white",'bg_color':'purple'}))
    worksheet.insert_image(13,0, sheet6[1], {'x_scale': 1.6})

    
    sheet_7 = 'Time Series Outflow (Amount)'
    worksheet = workbook.add_worksheet(sheet_7.upper()) 

    df = pd.DataFrame(data=sheet7[0]["data"],columns=sheet7[0]["columns"] )
    set_up(df) 
    worksheet.merge_range("A2:Z2", header, header_format(workbook,{'bold':True,'color':"white",'bg_color':'blue'}))

    row = 0
    col = 0

    space = 3

    values = df.values.tolist()
    columns = df.columns.tolist()

    if pretiffy:
        for i, column in enumerate(columns):
            column_width = max(df[column].astype(
                str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            worksheet.set_column(col_idx + space, col_idx, 12)

    for col, data in enumerate(columns):
        worksheet.write(space, col, data,
                        text_box_center_wrap_format(workbook))

    for row_num, row_data in enumerate(values):
        row_num += space + 1
        for col_num, col_data in enumerate(row_data):
            if col_num ==0:
                worksheet.write(row_num, 0, col_data,
                                bold_highlighting_format(workbook))

            if row_data[0].count("Total"):
                worksheet.write(row_num, col_num, col_data,
                                yellow_highlighting_format(workbook)) 
            elif row_data[0].count("Metric") > 0 :
                worksheet.write(row_num, col_num, col_data,
                                blue_highlighting_format(workbook))
            else:
                worksheet.write(row_num, col_num, col_data,
                                default_format(workbook))

    worksheet.merge_range("A13:O13", '3 - Month Outflow Time Series (Amount)' ,header_format(workbook,{'color':"white",'bg_color':'purple'}))
    worksheet.insert_image(13,0, sheet7[1], {'x_scale': 1.07})


    sheet_8 = 'Time Series Inflow (Frequency)'
    worksheet = workbook.add_worksheet(sheet_8.upper())

    df = pd.DataFrame(data=sheet8[0]["data"],columns=sheet8[0]["columns"] )
    set_up(df) 
    worksheet.merge_range("A2:Z2", header, header_format(workbook,{'bold':True,'color':"white",'bg_color':'blue'}))

    row = 0
    col = 0

    space = 3

    values = df.values.tolist()
    columns = df.columns.tolist()

    if pretiffy:
        for i, column in enumerate(columns):
            column_width = max(df[column].astype(
                str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            worksheet.set_column(col_idx + space, col_idx, 10)

    for col, data in enumerate(columns):
        worksheet.write(space, col, data,
                        text_box_center_wrap_format(workbook))

    for row_num, row_data in enumerate(values):
        row_num += space + 1
        for col_num, col_data in enumerate(row_data):
            if col_num ==0:
                worksheet.write(row_num, 0, col_data,
                                bold_highlighting_format(workbook))

            if row_data[0].count("Total"):
                worksheet.write(row_num, col_num, col_data,
                                yellow_highlighting_format(workbook)) 
            elif row_data[0].count("Metric") > 0 :
                worksheet.write(row_num, col_num, col_data,
                                blue_highlighting_format(workbook))
            else:
                worksheet.write(row_num, col_num, col_data,
                                default_format(workbook))


    worksheet.merge_range("A13:O13", '3 - Month Inflow Time Series (Frequency)' ,header_format(workbook,{'color':"white",'bg_color':'purple'}))
    worksheet.insert_image(13,0, sheet8[1], {'x_scale': 1.4})

    
    sheet_9 = 'Time Series Outflow (Frequency)'
    worksheet = workbook.add_worksheet(sheet_9.upper()) 

    df = pd.DataFrame(data=sheet9[0]["data"],columns=sheet9[0]["columns"] )
    set_up(df) 
    worksheet.merge_range("A2:Z2", header, header_format(workbook,{'bold':True,'color':"white",'bg_color':'blue'}))

    row = 0
    col = 0

    space = 3

    values = df.values.tolist()
    columns = df.columns.tolist()

    if pretiffy:
        for i, column in enumerate(columns):
            column_width = max(df[column].astype(
                str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            worksheet.set_column(col_idx + space, col_idx, 10)

    for col, data in enumerate(columns):
        worksheet.write(space, col, data,
                        text_box_center_wrap_format(workbook))

    for row_num, row_data in enumerate(values):
        row_num += space + 1
        for col_num, col_data in enumerate(row_data):

            if col_num ==0:
                worksheet.write(row_num, 0, col_data,
                                bold_highlighting_format(workbook))

            if row_data[0].count("Total"):
                worksheet.write(row_num, col_num, col_data,
                                yellow_highlighting_format(workbook)) 
            elif row_data[0].count("Metric") > 0 :
                worksheet.write(row_num, col_num, col_data,
                                blue_highlighting_format(workbook))
            else:
                worksheet.write(row_num, col_num, col_data,
                                default_format(workbook))

    worksheet.merge_range("A13:O13", '3 - Month Outflow Time Series (Frequency)' ,header_format(workbook,{'color':"white",'bg_color':'purple'}))
    worksheet.insert_image(13,0, sheet9[1], {'x_scale': 1.4})   

    sheet_10 = 'Alerts & Cases Details'
    worksheet = workbook.add_worksheet(sheet_10.upper()) 

    df = pd.DataFrame(data=sheet10[0]["data"],columns=sheet10[0]["columns"] )
    set_up(df) 
    worksheet.merge_range("A2:H2", header, header_format(workbook,{'bold':True,'color':"white",'bg_color':'blue'}))

    row = 0
    col = 0

    space = 3

    values = df.values.tolist()
    columns = df.columns.tolist()

    if pretiffy:
        for i, column in enumerate(columns):
            column_width = max(df[column].astype(
                str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            worksheet.set_column(col_idx + space, col_idx, 20) 

            # col_idx = df.columns.get_loc('Total Alerts')
            # worksheet.set_column(col_idx + space, col_idx, 20)

    for col, data in enumerate(columns):
        worksheet.write(space, col, data,
                        text_box_center_wrap_format(workbook))

    for row_num, row_data in enumerate(values):
        row_num += space + 1
        for col_num, col_data in enumerate(row_data):
            # print('col_data',col_num, col_data)

            if col_num ==0:
                worksheet.write(row_num, 0, col_data,
                                bold_highlighting_format(workbook))

            if row_data[0].count("Metric") > 0 :
                worksheet.write(row_num, col_num, col_data,
                                blue_highlighting_format(workbook))
            else:
                worksheet.write(row_num, col_num, col_data,default_format(workbook))

    table_len = len(df.values.tolist())+7
    worksheet.merge_range(f"A{table_len}:D{table_len}", 'Analysis' , header_format(workbook,{ "bg_color": 'green',"color": '#fffff'}))
    worksheet.merge_range(F"E{table_len}:H{table_len}", ' Risk Assessment' , header_format(workbook,{ "bg_color": 'purple',"color": '#fffff'}))

    worksheet.insert_image(table_len+1,0, sheet10[1], {'x_scale':0.8,'y_scale': 0.7})
    worksheet.insert_image(table_len+1,4, sheet10[2], {'x_scale': 0.7,'y_scale': 0.7})

    workbook.close()

    return file_n



   

def create_lite_excel(scenario='',rule="",  branchId="", accountId="", 
    data: list = [],
    columns: list = [],
    pretiffy=False):

    locn = os.path.join(path,'services', scenario,'excel')    
    date = datetime.datetime.now().strftime('%d%b%Y%H%M%S%f') 
    file_n = '{}-{}-{}.xlsx'.format(branchId, accountId,date) if accountId else  '{}-{}.xlsx'.format(branchId,date)
    filename = os.path.join(locn,file_n)
    print('EXCEL LOCATION',filename)
    workbook = xlsxwriter.workbook.Workbook(filename)
    header = "{} for Customer Account: {} in Branch: {}".format(rule, accountId, branchId) if accountId else  "{} for Customer in Branch: {}".format(scenario, branchId)
    header = header.upper()

    df = pd.DataFrame(
        data=data,
        columns=columns)

    set_up(df)

    sheet_1 = 'RESULTS {} - {} entries'.format(1,2)
    worksheet = workbook.add_worksheet(sheet_1.upper())

    worksheet.merge_range(f"A2:{chr(len(columns)+64)}2", header, header_format(workbook,{'bold':True,'color':"white",'bg_color':'blue'}))

    row = 0
    col = 0

    space = 3

    values = df.values.tolist()
    columns = df.columns.tolist()

    if pretiffy:
        for i, column in enumerate(columns):
            column_width = max(df[column].astype(str).map(len).max(), len(column))
            col_idx = df.columns.get_loc(column)
            worksheet.set_column(col_idx + space, col_idx, 25) 
    
        # col_idx = df.columns.get_loc('Today')
        # worksheet.set_column(col_idx + space, col_idx, 15) 

        # col_idx = df.columns.get_loc('Above 6 Months - 1 Year')
        # worksheet.set_column(col_idx + space, col_idx, 25) 


    for col, data in enumerate(columns):
        worksheet.write(space, col, data,text_box_center_wrap_format(workbook))

    for row_num, row_data in enumerate(values):
        row_num += space + 1
        for col_num, col_data in enumerate(row_data):
            try:
                if col_num ==0:
                    worksheet.write(row_num, 0, col_data,
                                    bold_highlighting_format(workbook))

                if row_data[0].count("SN") > 0 :
                    worksheet.write(row_num, col_num, col_data,
                                    yellow_highlighting_format(workbook))
                # elif row_data[0].count("Metric") > 0 :
                #     worksheet.write(row_num, col_num, col_data,
                #                     blue_highlighting_format(workbook))
                # elif row_data[0].count("Cummulative") > 0 or row_data[0].count("Cummulative") > 0:
                #     worksheet.write(row_num, col_num, col_data,
                #                     cumm_format(workbook))
                else:
                    worksheet.write(row_num, col_num, col_data,
                                    default_format(workbook))
            except Exception as e:
                print(e)


    workbook.close()

    return [(filename,file_n) ]
