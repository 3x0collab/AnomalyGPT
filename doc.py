
import math
import os
import random
from datetime import datetime as dt

import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from jinja2 import Environment, FileSystemLoader
from matplotlib.patches import Patch

from AnomalyPromptGRP.mailer import send_html_mail
from AnomalyPromptGRP.func import get_sqlite_con_dir


template_path = os.path.join(get_sqlite_con_dir(),"bots", "AnomalyPromptGRP","templates")
images_path = os.path.join(get_sqlite_con_dir(),"bots", "AnomalyPromptGRP","images")
now = dt.now()
date = now.strftime('%d-%b-%y %H:%M:%S %p').upper()

me_and_boss = ['adexadexdede@gmail.com', 'princetoka@hotmail.com']
# me_ahmed= ['adexadexdede@gmail.com', 'boboahmedino@gmail.com']
# me_tunde = [ 'oluwamotunde@gmail.com']
me = ['adexadexdede@gmail.com', 'xasdxasd926@gmail.com']
# ['adexadexdede@gmail.com', 'princetoka@hotmail.com', 'xasdxasd926@gmail.com']
all = ['oluwamotunde@gmail.com']

font = font_manager.FontProperties(
    weight='ultralight',
    style='normal', size=10)

location = ['best', 'upper right', 'upper left', 'lower left', 'lower right',
            'right', 'center left', 'center right', 'lower center', 'upper center', 'center']


def format_int(x: int, bin=False):
    """ This function checks if the variable passed in the function is none and return 0 else it returns back the same variable unchanged """
    res = int(0 if x is None else int(x))
    res = int(1 if bin and res < 1 else res)
    return res


def roundup(x: int or float):
    return int(int(math.ceil(x / 10.0)) * 10)


def gen_str(string):
    return str(string) if len(str(string)) > 1 else '0{}'.format(string)


def gen_color(len=0):
    data = []
    for x in list(range(len)):
        hexadecimal = "#" + \
            ''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        data.append(hexadecimal)
    return data


def get_date():
    now = dt.now()
    ricaRecordDate = '{}{}{}'.format(
        now.year, gen_str(now.month), gen_str(now.day))
    ricaRecordTime = '{}:{}:{}'.format(
        gen_str(now.hour), gen_str(now.minute), gen_str(now.second))
    date_time = "{}-{}".format(ricaRecordDate, ricaRecordTime)
    return date_time


def highlight_cols(): 
    return 'text-align: right'


def highlight_last_row(s):
    return ['background-color: #eee; font-weight:bold' if i == len(s)-1 else '' for i in range(len(s))]


def create_pivot(data: list):
    columns = list(data.get('columns').keys())
    order_column = ["code", "description"]
    for x in columns:
        if x not in ['code', 'description', 'found', 'percentage', 'total']:
            order_column.append(x)

    order_column.append('found')
    order_column.append('percentage')
    order_column.append('total')

    df = pd.DataFrame(data=data.get('data'), index=list(
        range(len(data.get('data'))+1))[1:], columns=order_column)
    print('df', df)
    print('columns', columns, order_column)

    df.columns.name = 'SN'
    df['percentage'] = df['percentage'].apply('{:,.1f}%'.format)

    df = df.copy().rename(columns={'code': 'category'})

    for x in list(df.columns):
        if x not in ['category', 'description', 'percentage']:
            df[x] = df[x].apply("{:>10,d}".format)

    subset = [x for x in df.columns if x not in ['category', 'description']]

    df = df.style.set_properties(subset=subset, **{'text-align': 'right'})

    df.set_table_styles(
        [dict(selector='th', props=[('text-align', 'center')])])

    return df


def create_single_pie_chart(value: int, name: str, filename="chart"):
    value = value
    label = name
    values = []
    values.append(value)
    values.append(0)
    labels = []
    labels.append(label)

    wedgeprops = {'width': 0.7, 'edgecolor': 'white', 'linewidth': 2}
    plt.pie(values, colors=["#bd66ff", "white"],
            wedgeprops=wedgeprops, startangle=90, radius=1.2)
    plt.text(0, .15, "Total", ha='center', va='center',
             fontsize=27, fontfamily='Cambria')
    plt.text(0, -.15, f'{value}', ha='center',
             va='center', fontsize=18, fontfamily='Cambria')
    plt.text(-.1, -.85, f"{value}", fontsize=10,
             fontweight='ultralight', color="#757575")
    legend = plt.legend(labels, loc=location[2], edgecolor="white", prop=font)
    legend.get_frame().set_alpha(None)
    legend.get_frame().set_facecolor((0, 0, 0, 0))

    plt.title('Pie chart', fontsize=9, fontweight='bold')
    p = plt.gcf()
    plt.savefig('{}.png'.format(filename), dpi=1200)
    plt.clf()


def create_single_bar(value: int, name: str, filename="bar"):

    plt.style.use('seaborn')
    x = ['']
    y = [value]
    z = [name]
    plt.bar(x, y)
    legend = plt.legend(z, loc="upper center", edgecolor="white", prop=font)
    legend.get_frame().set_alpha(None)
    legend.get_frame().set_facecolor((0, 0, 0, 0))

    plt.xlim([-.5, .5])
    plt.title('Bar chart', fontsize=9, fontweight='bold')
    plt.xlabel(name)
    rounded = roundup(value)
    plt.ylim([0, rounded + int(rounded / 9)])

    plt.savefig('{}.png'.format(filename), dpi=1200)
    plt.clf()


def create_single_pivot(df, index=1,columns=[]):
    # lst = list(map(lambda e: e.replace("RICA",""),columns))
    df = pd.DataFrame(data=df, index=list(range(index, index+len(df))),columns=columns)
    # df.columns = lst
    df.columns.name = 'SN'
    try:
        df['amount'] = df['amount'].map('{:,.2f}'.format)
    except Exception as e:
        pass
    # df = df.style.apply(highlight_last_row)

    return df

 

def create_pie_chart(data: list,columns=["special_date", 'total_count'],title="TRANSACTION TYPES",filename=None):

    if columns[1]:
        df = pd.DataFrame(data=data, index=list(
            range(len(data)+1))[1:], columns=columns) 
    else:
        df = pd.DataFrame(data)
        if len(df.columns):
            count = df[columns[0]].value_counts().sort_index()
            df = pd.DataFrame({columns[0]: count.index,
                          columns[1]: count.values})

    
    size  = df.shape[0]
    
    # plt styling parameters
    plt.style.use('seaborn')
    if len(df.columns) and (df[columns[1]] != 0).all() :
        colors = gen_color(size)
        sub = df.head(size)
        x = sub[columns[0]]
        y = sub[columns[1]]
        percent = 100.*y/y.sum()  

        df[columns[1]] = df[columns[1]].astype(str)

        # print(df)

        patches, texts = plt.pie(y, colors=colors, startangle=90, radius=1.2)

        if len(columns) > 2:
            z = sub[columns[2]]
            labels = [f'{z}-{i}: {j} ({1:1.2f})%'.format(y) for i, j,y,z in zip(x, percent,y,z)]
        else:
            labels = ['{0}: {2} ({1:1.2f})%'.format(i, j,y) for i, j,y in zip(x, percent,y)]
    # labels = ['{0} - {1:1.2f} %'.format(i, j) for i, j in zip(x, percent)]

        sort_legend = False
        if sort_legend:
            patches, labels, dummy = zip(*sorted(zip(patches, labels, y),
                                                 key=lambda x: x[2],
                                                 reverse=True))

        plt.legend(patches, labels, loc='best', bbox_to_anchor=(-0.1, 1.),
                   fontsize=12)
    plt.title("", fontsize=9, fontweight='bold')
    plt. ylabel('')

    plt.tight_layout()
    filename = filename if filename else  os.path.join(images_path,title.replace(" ",""))
    plt.savefig('{}.png'.format(filename), bbox_inches='tight', dpi=1200)
    plt.cla()
    return filename+".png"


 

def create_line_chart(data: dict = {},key="RICADATETYPE",title="TRANSACTION TYPES"):

    df = pd.DataFrame(data=data)
    f=plt.figure(figsize=(8,4))
    plt.rcParams.update({'font.size': 6}) # must set in top
    plt.rcParams["figure.figsize"] = (8, 4)
    plt.rcParams["xtick.labelsize"] = 6
    plt.ticklabel_format(useOffset=False, style='plain')

    if len(df.columns) > 1:
        df.plot.line(x=key, title=title,ax=f.gca())

    plt.style.use('seaborn')
    plt.title("", fontsize=9, fontweight='bold')
    plt. ylabel('')
    filename = os.path.join(images_path,title.replace(" ",""))
    plt.savefig('{}.png'.format(filename), dpi=1200)
    plt.cla()
        
    return filename+".png"

def create_bar_chart(data: dict = {},key="RICADATETYPE",title="TRANSACTION TYPES",filename=None):

    df = pd.DataFrame(data=data)
    plt.ticklabel_format(useOffset=False, style='plain')
    f=plt.figure()
    plt.ticklabel_format(useOffset=False, style='plain')

    if len(df.columns) > 1:
        df.plot.bar(x=key, title=title, fontsize='9',ax=f.gca());
    plt.style.use('seaborn')
    plt.title("", fontsize=9, fontweight='bold')
    plt. ylabel('')

    filename = filename if filename else os.path.join(images_path,title.replace(" ",""))
    plt.savefig('{}.png'.format(filename), bbox_inches='tight', dpi=1200)
    plt.cla()
    return filename+".png"




def create_bar_chart2(data: list,columns=["special_date", 'total_count'],title="TRANSACTION TYPES",size=20):

    df = pd.DataFrame(data=data, index=list(
            range(len(data)+1))[1:], columns=columns) 

    # def datefunc_new(column):
    #     return str(df[column])

    # df['special_date'] = pd.to_datetime(df["special_date"], format='%Y-%m-%d')
    # df['special_date'] = df['special_date'].dt.date
    # print('====================>',  df['special_date']  )
    # df['special_date'] = df['special_date'].dt.strftime('yyyy-mm-dd')

    # count = df[columns[0]].value_counts().sort_index()
    # df = pd.DataFrame({columns[0]: count.index,
    #                   columns[1]: count.values})

    plt.style.use('seaborn')

    # chose a color map with enough colors for the number of bars
    colors = gen_color(size)

    sub = df.head(size)
    print(df)
    sub.groupby(columns[0])[columns[2]].sum().plot(kind='bar', legend=True, color=colors)

    cmap = dict(zip(sub[columns[0]], colors))

    patches = [Patch(color=v, label=k) for k, v in cmap.items()]

    plt.title(title, fontsize=9, fontweight='bold')

    plt.legend(handles=patches, loc='best',
               fontsize=8)
    plt.tight_layout()
    filename = os.path.join(images_path,title.replace(" ",""))
    plt.savefig('{}.png'.format(filename), bbox_inches='tight', dpi=1200)
    plt.clf()


columns = ["Inflow/Time Bucket", "1 Day", "2-7 Days", "8-14 Days", "15-28 Days", "29 Days - 3 months",
       "3 months - 6 months", "6 months - 1 year", "1 year - 3 years", "3 years - 5 years", "Over 5 years"]

def create_trans_bar_chart(data: list,columns=columns,title="AMOUNT INFLOW / OUTFLOW", filename="default", file_location='./images/'):
    filename = file_location + filename
    print(data)

    a = data[0]
    b = data[1]


    X = [arg.lower() for arg in columns[1:]]
    f = np.array([a[1:], b[1:]])
    c = np.amax(f)

    try:
        minval = np.min(f[np.nonzero(f)]) or np.amin(f)
        maxval = format_int(np.max(f[np.nonzero(f)])) or np.amax(f)
    except:
        minval = np.amin(f)
        maxval = format_int(np.amax(f), bin=True)

    X_axis = np.arange(len(X))
    colors = gen_color(2)

    plt.style.use('seaborn')

    plt.bar(X_axis - 0.2, f[0], 0.4, edgecolor='black',
            color=colors[0], label=a[0])
    plt.bar(X_axis + 0.2, f[1], 0.4, edgecolor='black',
            color=colors[1], label=b[0])
    plt.xticks(X_axis, X, rotation=90)

    plt.ylim([0, maxval + minval])

    plt.title(title)
    plt.legend(loc=location[0])

    plt.ticklabel_format(style='plain', axis='y')

    plt.tight_layout()

    plt.savefig('{}.png'.format(filename), bbox_inches='tight')
    plt.clf()
    print('==========================', data)

    # a = data[0]
    # b = data[1]

    # X = [arg.lower() for arg in columns[1:]]
    # f = np.array([a[1:], b[1:]])
    # c = np.amax(f)

    # X_axis = np.arange(len(X))
    # colors = gen_color(2)

    # plt.style.use('seaborn')
    # plt.plot(f[0], marker='*', color=colors[0], label=a[0])
    # plt.plot(f[1], marker='*', color=colors[1], label=b[0])
    # plt.xticks(X_axis, X, rotation=90)
    # plt.ylim([0, roundup(c + 1)])
    # plt.title("AMOUNT INFLOW / OUTFLOW")
    # plt.legend(loc=location[0])
    # plt.tight_layout()

    # plt.savefig('{}_freq.png'.format(filename), bbox_inches='tight')
    # plt.clf()

    plt.close('all')


def create_trans_pie_chart(data: dict = {},columns=["first", 'total_count'],title="TRANSACTION TYPES", filename="default", sort_legend=False, head_text="INFLOWS", file_location='./images/'
    ):
    try:
        filename = file_location + filename

        item = data.items()
        b = list(item)
        df = pd.DataFrame(b, columns=columns)

        size = df.shape[0]

        plt.style.use('seaborn')
        plt.rcParams["font.family"] = "Cambria"

        colors = gen_color(size)
        wedgeprops = {'width': 0.7, 'edgecolor': 'white', 'linewidth': 1}

        x = df[columns[0]]
        y = df[columns[1]]

        y_total = y.sum()

        percent = 100.*y / y_total

        patches, texts = plt.pie(
            y, wedgeprops=wedgeprops, colors=colors, startangle=270, radius=1.2)
        labels = ['{0}: {1} ({2:1.2f})%'.format(i, j, k)
                  for i, j, k in zip(x, y, percent)]

        if sort_legend:
            patches, labels, dummy = zip(*sorted(zip(patches, labels, y),
                                                 key=lambda x: x[2],
                                                 reverse=True))
        plt.legend(patches, labels, bbox_to_anchor=[
                   0.97, 0.5], loc=location[6], fontsize=8)
        plt.title("{title} ({})".format(title,head_text), fontweight='bold')

        plt.text(0, .15, "Total", ha='center', va='center',
                 fontsize=27, fontfamily='Cambria')
        plt.text(0, -.15, f'{y.sum()}', ha='center',
                 va='center', fontsize=18, fontfamily='Cambria')

        plt.tight_layout()
        plt.savefig('{}.png'.format(filename), bbox_inches='tight')
        plt.clf()
    except Exception as e:
        print('create_trans_pie_chart', e)
    finally:
        plt.close('all')


def create_timeseries_bar(data: list, filename: list = ['time', 'amount'], file_location='./images/'):
    try:
        filename = [file_location + x for x in filename]

        [i.set_index('Time', inplace=True) for i in data]
        data1 = data[0]
        data2 = data[1]
        a = data1['Frequency'].to_list()
        b = data2['Time Count'].to_list()
        columns = data1.index.to_list() or data1['Time'].to_list()
        X = [arg.lower() for arg in columns]
        f = np.array([a, b])
        minval = np.min(f[np.nonzero(f)]) or np.amin(f)
        maxval = np.max(f[np.nonzero(f)]) or np.amax(f)
        X_axis = np.arange(len(X))
        colors = gen_color(2)

        plt.style.use('seaborn')
        plt.plot(f[0], marker='*', color=colors[0], label='Inflow')
        plt.xticks(X_axis, X, rotation=90)
        plt.ylim([0, int(maxval) + int(maxval + minval)])
        plt.title("FREQUENCY INFLOWS")
        plt.legend(loc=location[0])
        plt.tight_layout()
        plt.savefig('{}_in.png'.format(filename[0]), bbox_inches='tight')
        plt.clf()

        plt.style.use('seaborn')
        plt.plot(f[1], marker='*', color=colors[1], label='Outflow')
        plt.xticks(X_axis, X, rotation=90)
        plt.ylim([0, int(maxval) + int(maxval + minval)])
        plt.title("FREQUENCY OUTFLOW")
        plt.legend(loc=location[0])
        plt.tight_layout()
        plt.savefig('{}_out.png'.format(filename[0]), bbox_inches='tight')
        plt.clf()

        # Amount
        a = data1['Amount'].to_list()
        b = data2['Amount'].to_list()
        f = np.array([a, b])
        minval = np.min(f[np.nonzero(f)]) or np.amin(f)
        maxval = np.max(f[np.nonzero(f)]) or np.amax(f)

        plt.style.use('seaborn')
        plt.bar(X_axis, f[0], 0.4, edgecolor='black',
                color=colors[0], label='Inflow')
        plt.xticks(X_axis, X, rotation=90)
        plt.ylim([0, int(maxval) + int(maxval / 5)])
        plt.ticklabel_format(style='plain', axis='y')
        plt.title("AMOUNT INFLOW")
        plt.legend(loc=location[0])
        plt.tight_layout()
        plt.savefig('{}_in.png'.format(filename[1]), bbox_inches='tight')
        plt.clf()

        plt.style.use('seaborn')
        plt.bar(X_axis, f[1], 0.4, edgecolor='black',
                color=colors[1], label='Outflow')
        plt.xticks(X_axis, X, rotation=90)
        plt.ylim([0, int(maxval) + int(maxval / 5)])
        plt.ticklabel_format(style='plain', axis='y')
        plt.title("AMOUNT OUTFLOW")
        plt.legend(loc=location[0])
        plt.tight_layout()
        plt.savefig('{}_out.png'.format(filename[1]), bbox_inches='tight')
        plt.clf()
    except Exception as e:
        print('create_timeseries_bar', e)
    finally:
        plt.close('all')


def create_comparison_bar(data, filename: list = ['ex_amount', 'ex_count'], file_location='./images/'):
    try:
        filename = [file_location + x for x in filename]

        df = pd.DataFrame(data)
        brt = []

        a = df['In Amount'].to_list()
        b = df['Expected In Amount'].to_list()
        c = df['Out Amount'].to_list()
        d = df['Expected Out Amount'].to_list()

        columns = ["1 Day", "2-7 Days", "8-14 Days", "15-28 Days", "29 Days - 3 months",
                   "3 months - 6 months", "6 months - 1 year", "1 year - 3 years", "3 years - 5 years", "Over 5 years"]

        X = [arg.lower() for arg in columns]
        f = np.array([a, b, c, d])

        minval = np.min(f[np.nonzero(f)]) or np.amin(f)
        maxval = np.max(f[np.nonzero(f)]) or np.amax(f)

        X_axis = np.arange(len(X))
        colors = gen_color(4)

        plt.style.use('seaborn')

        width = 0.2  # the width of the bars

        label_list = ['Inflow', 'Expected Inflow',
                      'Outflow', 'Expected Outflow']

        plt.bar(X_axis - width, f[0], width, edgecolor='black',
                color=colors[0], label=label_list[0])
        plt.bar(X_axis, f[1], width, edgecolor='black',
                color=colors[1], label=label_list[1])
        plt.xticks(X_axis, X, rotation=90)

        plt.ylim([0, int(maxval) + int(maxval / 4)])
        plt.ticklabel_format(style='plain', axis='y')

        plt.title("INFLOW AMOUNT")
        plt.legend(loc='best')
        plt.tight_layout()
        plt.savefig('{}_in.png'.format(filename[0]), bbox_inches='tight')
        plt.clf()

        plt.bar(X_axis - width, f[2], width, edgecolor='black',
                color=colors[2], label=label_list[2])
        plt.bar(X_axis, f[3], width, edgecolor='black',
                color=colors[3], label=label_list[3])

        plt.xticks(X_axis, X, rotation=90)

        plt.ylim([0, int(maxval) + int(maxval / 4)])
        plt.ticklabel_format(style='plain', axis='y')
        # This is to keep this shit from exploding like if you want the chart to be 75% of the maximum stuff

        plt.title("OUTFLOW AMOUNT")
        plt.legend(loc='best')
        plt.tight_layout()
        plt.savefig('{}_out.png'.format(filename[0]), bbox_inches='tight')
        plt.clf()

        a = df['In Frequency'].to_list()
        b = df['Expected In Frequency'].to_list()
        c = df['Out Frequency'].to_list()
        d = df['Expected Out Frequency'].to_list()

        columns = ["1 Day", "2-7 Days", "8-14 Days", "15-28 Days", "29 Days - 3 months",
                   "3 months - 6 months", "6 months - 1 year", "1 year - 3 years", "3 years - 5 years", "Over 5 years"]
        label_list = ['Inflow Frequency', 'Expected Inflow Frequency',
                      'Outflow Frequency', 'Expected Outflow Frequency']

        X = [arg.lower() for arg in columns]
        f = np.array([a, b, c, d])

        minval = np.min(f[np.nonzero(f)]) or np.amin(f)
        maxval = np.max(f[np.nonzero(f)]) or np.amax(f)

        X_axis = np.arange(len(X))

        plt.style.use('seaborn')

        plt.plot(f[0], marker='*', color=colors[0], label=label_list[0])
        plt.plot(f[1], marker='*', color=colors[1], label=label_list[1])

        plt.xticks(X_axis, X, rotation=90)

        plt.ylim([0, int(maxval) + int(maxval / 4)])

        plt.title("INFLOWS FREQUENCY")
        plt.legend(loc='best')
        plt.tight_layout()
        plt.savefig('{}_in.png'.format(filename[1]), bbox_inches='tight')
        plt.clf()

        plt.plot(f[2], marker='*', color=colors[2], label=label_list[2])
        plt.plot(f[3], marker='*', color=colors[3], label=label_list[3])

        plt.xticks(X_axis, X, rotation=90)

        plt.ylim([0, int(maxval) + int(maxval / 4)])

        plt.title("OUTFLOW FREQUENCY")
        plt.legend(loc='best')
        plt.tight_layout()
        # plt.show()
        plt.savefig('{}_out.png'.format(filename[1]), bbox_inches='tight')
        plt.clf()
    except Exception as e:
        print('all comp_chart', e)
    finally:
        plt.close('all')


def create_comparison_bar_inflow(data: list, columns: list, filename: list = ['ex_amount_s', 'ex_count_s'], file_location='./images/'):

    try:
        filename = [file_location + x for x in filename]

        a = data[0]
        b = data[1]
        c = data[2]
        d = data[3]

        label_list = columns
        columns = ["1 Day", "2-7 Days", "8-14 Days", "15-28 Days", "29 Days - 3 months",
                   "3 months - 6 months", "6 months - 1 year", "1 year - 3 years", "3 years - 5 years", "Over 5 years"]

        X = [arg.lower() for arg in columns]
        f = np.array([a, b])
        minval = np.min(f[np.nonzero(f)]) or np.amin(f)
        maxval = np.max(f[np.nonzero(f)]) or np.amax(f)
        X_axis = np.arange(len(X))
        colors = gen_color(2)
        colors = ['green', 'purple', 'yellow', 'red']

        plt.style.use('seaborn')
        width = 0.2  # the width of the bars
        plt.bar(X_axis - width, f[0], width, edgecolor='black',
                color=colors[0], label=label_list[0])
        plt.bar(X_axis, f[1], width, edgecolor='black',
                color=colors[1], label=label_list[1])
        plt.xticks(X_axis, X, rotation=90)
        plt.ylim([0, int(maxval) + int(maxval / 4)])
        plt.ticklabel_format(style='plain', axis='y')
        plt.title("INFLOW AMOUNT")
        plt.legend(loc='best')
        plt.tight_layout()
        plt.savefig('{}_in.png'.format(filename[0]), bbox_inches='tight')
        plt.clf()

        X = [arg.lower() for arg in columns]
        f = np.array([a, b, c, d])
        minval = np.min(f[np.nonzero(f)]) or np.amin(f)
        maxval = np.max(f[np.nonzero(f)]) or np.amax(f)
        X_axis = np.arange(len(X))

        plt.style.use('seaborn')
        f = np.array([c, d])
        minval = np.min(f[np.nonzero(f)]) or np.amin(f)
        maxval = np.max(f[np.nonzero(f)]) or np.amax(f)
        plt.plot(f[0], marker='*', color=colors[0], label=label_list[2])
        plt.plot(f[1], marker='*', color=colors[1], label=label_list[3])
        plt.xticks(X_axis, X, rotation=90)
        plt.ylim([0, int(maxval) + int(maxval / 4)])
        plt.title("INFLOW FREQUENCY")
        plt.legend(loc='best')
        plt.tight_layout()
        plt.savefig('{}_freq.png'.format(filename[1]), bbox_inches='tight')
        plt.clf()
    except Exception as e:
        print('Exception', e)
    finally:
        plt.close('all')


def create_comparison_bar_outflow(data: list, columns: list, filename: list = ['ex_amount_s', 'ex_count_s'], file_location='./images/'):
    try:
        filename = [file_location + x for x in filename]

        a = data[0]
        b = data[1]
        c = data[2]
        d = data[3]

        label_list = columns
        columns = ["1 Day", "2-7 Days", "8-14 Days", "15-28 Days", "29 Days - 3 months",
                   "3 months - 6 months", "6 months - 1 year", "1 year - 3 years", "3 years - 5 years", "Over 5 years"]

        X = [arg.lower() for arg in columns]
        f = np.array([a, b])
        minval = np.min(f[np.nonzero(f)]) or np.amin(f)
        maxval = np.max(f[np.nonzero(f)]) or np.amax(f)

        X_axis = np.arange(len(X))
        colors = gen_color(2)

        plt.style.use('seaborn')
        width = 0.2  # the width of the bars

        plt.bar(X_axis - width, f[0], width, edgecolor='black',
                color=colors[0], label=label_list[0])
        plt.bar(X_axis, f[1], width, edgecolor='black',
                color=colors[1], label=label_list[1])
        plt.xticks(X_axis, X, rotation=90)
        plt.ylim([0, int(maxval) + int(maxval / 4)])
        plt.ticklabel_format(style='plain', axis='y')

        plt.title("OUTFLOW AMOUNT")
        plt.legend(loc='best')
        plt.tight_layout()
        plt.savefig('{}_out.png'.format(filename[0]), bbox_inches='tight')
        plt.clf()

        X = [arg.lower() for arg in columns]
        f = np.array([a, b, c, d])
        minval = np.min(f[np.nonzero(f)]) or np.amin(f)
        maxval = np.max(f[np.nonzero(f)]) or np.amax(f)
        X_axis = np.arange(len(X))

        plt.style.use('seaborn')
        f = np.array([c, d])
        minval = np.min(f[np.nonzero(f)]) or np.amin(f)
        maxval = np.max(f[np.nonzero(f)]) or np.amax(f)

        plt.plot(f[0], marker='*', color=colors[0], label=label_list[2])
        plt.plot(f[1], marker='*', color=colors[1], label=label_list[3])
        plt.xticks(X_axis, X, rotation=90)
        plt.ylim([0, int(maxval) + int(maxval / 4)])

        plt.title("OUTFLOW FREQUENCY")
        plt.legend(loc='best')
        plt.tight_layout()
        plt.savefig('{}_freq_out.png'.format(filename[1]), bbox_inches='tight')
        plt.clf()
    except Exception as e:
        print('Exception', e)
    finally:
        plt.close('all')

def create_pie_chart_full(data: list, filename="chart", config = {}):
    
    columns = ['special_date','amount']
    if columns[1]:
        df = pd.DataFrame(data=data, index=list(
            range(len(data)+1))[1:], columns=columns) 
    else:
        df = pd.DataFrame(data)
        if len(df.columns):
            count = df[columns[0]].value_counts().sort_index()
            df = pd.DataFrame({columns[0]: count.index,
                          columns[1]: count.values})

    
    size  = df.shape[0]
    
    # plt styling parameters
    plt.style.use('seaborn')
    if len(df.columns) and (df[columns[1]] != 0).all() :
        colors = gen_color(size)
        sub = df.head(size)
        x = sub[columns[0]]
        y = sub[columns[1]]
        percent = 100.*y/y.sum()  

        df[columns[1]] = df[columns[1]].astype(str)



    patches, texts = plt.pie(y, colors=colors, startangle=90, radius=1.2)
    labels = ['{0} - {1:1.2f} %'.format(i,j) for i,j in zip(x, percent)]

    sort_legend = False
    if sort_legend:
        patches, labels, dummy =  zip(*sorted(zip(patches, labels, y),
                                            key=lambda x: x[2],
                                            reverse=True))

    plt.legend(patches, labels, loc='best', bbox_to_anchor=(-0.1, 1.),
            fontsize=8)
    plt.title('Pie chart', fontsize=9, fontweight='bold')
    plt. ylabel('') 

    plt.tight_layout() 
    plt.savefig('{}.png'.format(filename), bbox_inches='tight', dpi=100)
    plt.cla()

def create_bar_chart_full(data: list, filename="bar", size = 20, config = {}):
    
    columns = ['special_date','trans_type',"amount"]
    if columns[1]:
        df = pd.DataFrame(data=data, index=list(
            range(len(data)+1))[1:], columns=columns) 
    else:
        df = pd.DataFrame(data)
        if len(df.columns):
            count = df[columns[0]].value_counts().sort_index()
            df = pd.DataFrame({columns[0]: count.index,
                          columns[1]: count.values})

    plt.style.use('seaborn')

    # chose a color map with enough colors for the number of bars
    colors = gen_color(size)

    sub = df.head(size)
    sub.groupby('special_date')['amount'].sum().plot(kind='bar', legend=True, color=colors)

    cmap = dict(zip(sub.trans_type, colors))

    patches = [Patch(color=v, label=k) for k, v in cmap.items()]

    plt.title('Bar chart', fontsize=9, fontweight='bold')

    plt.legend(handles=patches, loc='best',
                fontsize=8)
    plt.tight_layout() 
    plt.savefig('{}.png'.format(filename), bbox_inches='tight', dpi=100)
    plt.cla()

formatters = {
                'amount': lambda x: '<div style="text-align:right;margin:0px;" >' + x + '</div>',
                'details': lambda x: '<div style="white-space:nowrap;margin:0px;" >' + x + '</div>',
                'account_name': lambda x: '<div style="white-space:nowrap;margin:0px;" >' + x + '</div>'
                }

def make_doc(df, chart_data, results, name='', branch=[], current_branch='', 
    template_var={}, spf={}, xlsx=[],columns=[],group_field=None ):

    total = 0
    entries = 10
    _results = []
    search_results = []
    # print('entries,',entries)

    # print('GROUPSHDJFJ','group',branch,current_branch,columns)
    # print('template_var',template_var)


    if entries > 0:
        while total < len(results):
            new_data = results[total:(total+entries)]
            html_ = create_single_pivot(new_data, total+1,columns)
            try:
                html_ = html_.to_html(formatters=formatters, escape=False).replace('<table', '<table  role="presentation" cellpadding="2" cellspacing="2" ').replace(
                   '<td', '<td style="padding:1px !important;" ' ) 

            except Exception as e:
                html_ = html_.to_html().replace('<table', '<table  role="presentation" cellpadding="2" cellspacing="2" ').replace(
                   '<td', '<td style="padding:1px !important;" ' ) 

            _results.append((html_, len(new_data)))
            total = total+entries

    else:
        search_results = create_single_pivot(results,columns)
    # print(_results)

    scenario = template_var['scenario'] 
    scenario_id = template_var['scenario_id'] 
    c = template_var.get('exceptions',[])
    alertid = ", ".join([x['url'].split('args=')[1] for x in c if x.get('url')] )

    template_vars = {
        "scenario": "{}".format(scenario).upper(),
        "head": "{}".format(current_branch),
        # "chart_url": "cid:chart.png",
        # "bar_url": "cid:bar.png"
    }

    if group_field == 'branch':
        template_vars["reason"] =  "{} GENERATED FOR CUSTOMERS IN BRANCH {}".format(scenario, current_branch).upper() if current_branch else "{}".format(scenario).upper()
    else:
        template_vars["reason"] =  "{} GENERATED FOR {} : {}".format(scenario,group_field,current_branch).upper()


    if entries > 0:
        template_vars['results_pivot_tables'] = _results
        template_vars['entries'] = entries
    else:
        
        try:
            search_results = search_results.to_html(formatters=formatters, escape=False).replace('<table', '<table  role="presentation" cellpadding="2" cellspacing="2" ').replace(
               '<td', '<td style="padding:1px !important;" ' ) 

        except Exception as e:
            search_results = search_results.to_html().replace('<table', '<table  role="presentation" cellpadding="2" cellspacing="2" ').replace(
               '<td', '<td style="padding:1px !important;" ' ) 

        template_vars['results_pivot_table']  =  search_results




    html_out = gen_template(
        "myreport2.html", {**template_vars, **template_var})

    # print(html_out)
    print('template works',xlsx)
    send_html_mail("{}: {} ALERT ID: {}".format(scenario_id.upper(),scenario,alertid).upper(), html_out, template_var['emails'], images=[], spf=spf, xlsx=xlsx,scenario_id=scenario_id)


def gen_template(name, template_vars={}):
    print('TEMPLATE PATH',template_path)
    env = Environment(loader=FileSystemLoader(template_path, encoding='utf8'))
    template = env.get_template(name)
    html_out = template.render(template_vars)
    return html_out
