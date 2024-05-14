import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np

#colors: https://plotly.com/python/discrete-color/


import plotly.io as pio
pio.kaleido.scope.mathjax = None

if __name__ == '__main__':

    data = pd.read_csv("../evaluation/results_R72/numbers_patterns.csv")
    threshold = -1
   # data_set_filter = data.query("amount > " + str(threshold) + " and set != 'B1' and set !='A'")
    #data_set_filter = data.query("amount > " + str(threshold) + " and set !='A'")
    #data_set_filter = data.query("set !='A' and exp.str.contains('i=2')")
    data_set_filter = data.query("set !='A'")


    grouped_data = data_set_filter.groupby('set')['amount'].agg(['mean', 'std', 'min', 'max', 'median']).reset_index()

    order = ['W1', 'W2', 'W3', 'W4', 'W5', 'W6', 'R1', 'R2', 'R3']
    for i in range(1,289):
        order.append('R24-'+ str(i))

    grouped_data = grouped_data[grouped_data['set'].isin(order)].sort_values(by='set', key=lambda x:x.map({val: i for i, val in enumerate(order)}))

    data2 = data.query("amount > " + str(threshold) + " and set !='A'")
    data2 = data2[data2['set'].isin(order)].sort_values(by='set', key=lambda x: x.map(
       {val: i for i, val in enumerate(order)}))

    print(grouped_data)

    extra_group = data_set_filter.groupby('set')['amount']
    iqr = extra_group.apply(lambda x: np.percentile(x,75) - np.percentile(x,25))
    mad = extra_group.apply(lambda x: np.mean(np.abs(x-np.median(x))))

    extra_df = pd.DataFrame(extra_group)
    upper = extra_group.apply(lambda x: np.percentile(x,75))
    lower = extra_group.apply(lambda x: np.percentile(x,25))

    df2 = pd.DataFrame({'set': iqr.index, 'IQR': iqr.values, 'MAD': mad.values, 'Q3': upper.values, 'Q1': lower.values})



    grouped_data = pd.merge(grouped_data, df2, on='set', how='left')

    print(grouped_data)

    x_4_text=[]
    x_4_text.append('W1')
    x_4_text.append('W5')
    x_4_text.append('R3')

    hour4 = 1
    for i in range(len(order)):
        set_name = order[i]
        if('R24-' in set_name):

            if i % 4 == 0:
                prefix=set_name.split('R24-')[1]
                new_text = "R-" + str(hour4)
                #new_text= "R" + str(hour4) + "-" + prefix
                x_4_text.append(new_text)
                hour4+=1

    x_text=[]
    x_text.append('W1')
    x_text.append('W2')
    x_text.append('W3')
    x_text.append('W4')
    x_text.append('W5')
    x_text.append('W6')
    x_text.append('R1')
    x_text.append('R2')
    x_text.append('R3')


    hour = 1
    for i in range(len(order)):
        set_name = order[i]
        if('R24-' in set_name):
            prefix=set_name.split('R24-')[1]
            new_text = "R-" + str(hour)
            x_text.append(new_text)
            if i % 4 == 0:
                hour+=1


    fig = px.line(grouped_data, x='set', y='mean', markers=True, line_shape='linear', log_y=False, color_discrete_sequence=['rgb(0,34,102)'])


    #Boxplot for IQR
    fig.add_trace(go.Box(
        x= data2['set'],
        y= data2['amount'],
        boxpoints='outliers',
        jitter=0.5,
        pointpos=0,
        name='IQR',
    ))


    fig.add_trace(go.Scatter(
        x=grouped_data['set'],
        y=grouped_data['mean'],
        marker=dict(color='rgba(0,100,80,0.8)', size=15, symbol='triangle-up'),
        name='Mean'
    ))


    fig.add_trace(go.Scatter(
        x=grouped_data['set'],
        y=grouped_data['median'],

        marker=dict(color='rgba(189,56,206,0.8)', size=12, symbol='square'),
        name='Median'
    ))


    fig.add_trace(go.Scatter(
        x=grouped_data['set'].tolist() + grouped_data['set'].tolist()[::-1],
        y=(grouped_data['mean'] + grouped_data['std']).tolist() + (grouped_data['mean'] - grouped_data['std']).tolist()[
                                                                  ::-1],
        fill='toself',
        fillcolor='rgba(0,100,80,0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='SD'
    ))

    fig.add_trace(go.Scatter(
        x=grouped_data['set'].tolist() + grouped_data['set'].tolist()[::-1],
        y=(grouped_data['median'] + grouped_data['MAD']).tolist() + (grouped_data['median'] - grouped_data['MAD']).tolist()[
                                                                  ::-1],
        fill='toself',
        fillcolor='rgba(189,56,206,0.2)',
        line=dict(color='rgba(189,56,206,0.2)', dash='dot', width=5),
        name='MAD'
    ))


    fig.add_trace(go.Scatter(
        x=grouped_data['set'].tolist(),
        y=[100000] * len(grouped_data['set']),
        mode='lines',
        line=dict(color='rgb(0,51,33)', width=4, dash='dash'),
        name="F"
    ))

    fig.add_annotation(
        go.layout.Annotation(
            x=grouped_data['set'].max(),
            y=100000,
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-30
        )
    )

    s10_position = (grouped_data['set'].eq('W6').idxmax() + grouped_data['set'].eq('R1').idxmax()) / 2
    fig.add_trace(go.Scatter(
        y=[100000, 100000],
        x=['R1', 'R1'],
        mode='lines',
        line=dict(color='red', width=4, dash='dash'),
        name="Reboot"
    ))

    fig.add_shape(
        go.layout.Shape(
            type='line',
            x0=s10_position,
            x1=s10_position,
            y0=0,  # Y-Koordinate des Linienanfangs (anpassen Sie dies nach Bedarf)
            y1=100000,  # Y-Koordinate des Linienendes (anpassen Sie dies nach Bedarf)
            line=dict(color='red', width=4, dash='dash'),
            name="Reboot",
            # Linienfarbe und -breite
        )
    )


    fig.update_layout(

        legend=dict(
            x=0.8,
            y=0.8,
            orientation="v",
            yanchor="top",
            xanchor="left",
            bordercolor='rgba(0,0,0,0.8)',
            borderwidth=2,
            font=dict(size=15)

        ),
        xaxis=dict(
            title='memory dump',
            gridcolor='rgb(25, 25, 112)',
            tickmode='array',
            griddash='dot',
            tickvals=list(range(0, len(grouped_data['set']), 4)),
            ticktext=x_4_text


        ),

        yaxis=dict(
            title='#patterns',
            gridcolor='rgb(25, 25, 112)',
            griddash='dot',
            range=[0, 105000],
        ),

        width=1500,
        height=800,
        paper_bgcolor='white',
        plot_bgcolor='white',
        bargap=0.9,

    )

    fig.show()

    fig.write_image("outputs/patterns_amounts_R72-3.pdf")








