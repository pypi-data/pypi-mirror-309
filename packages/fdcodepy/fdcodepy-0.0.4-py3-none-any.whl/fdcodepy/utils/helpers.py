import pickle
import numpy as np
from datetime import datetime
import pandas as pd
import plotly
from collections import Counter
import plotly.graph_objects as go


THEME_COLOR = ['#549cf1', '#ec1346','#EC7063','#F1948A','#5DADE2','#85C1E9', 
               '#F4D03F', '#ffad22', '#A569BD', '#BB8FCE', '#de425b', '#31b08b','#ee8562',
              "#d75425", "#e6b532", "#7e2f8c", "#52bcec", "#a21d2f", "#73aa43", "#2b2a76" ]

def save2pickle(data, path_name = 'data.pickle'):
  with open(path_name,'wb') as pickle_file:
    pickle.dump(data, pickle_file)

def read_pickle(path_name = 'data.pickle'):
  with open(path_name,'rb') as pickle_file:
    return pickle.load(pickle_file)

## Scale based on average of values (energy profiles)
def normalize_series_average(series_ori, m):
    '''average normalizaiton but return averge value of the window (for energy reading purpose). 
    Series should be positive (close to zero sum with net demand lead to issues)'''
    sliding = series_ori.shape[0]//m
    sample_series = series_ori.reshape(sliding, m)
    scaler_average = np.average(sample_series, axis=1)
    scaler_average = scaler_average.repeat(m)
    old_err_state = np.seterr(divide='ignore')
    normalized_arr = np.divide(series_ori, scaler_average)
    # handle zero division
    normalized_arr = np.nan_to_num(normalized_arr, nan=0)
    np.seterr(**old_err_state) 
    return normalized_arr, scaler_average

def scaler_recoverary_sum(series_normalised, scaler_average):
    return series_normalised*scaler_average

## Scale based on max and min values
def scaler_normalization(series_ori, m):
  '''amplitude 10 normalizaiton'''
  sliding = series_ori.shape[0]//m
  sample_series = series_ori.reshape(sliding, m)
  scaler_max = np.max(sample_series, axis=1)
  scaler_min = np.min(sample_series, axis=1)
  scaler_10 = (scaler_max - scaler_min)/10
  scaler_10 = scaler_10.repeat(m)
  series_normalised = series_ori/scaler_10
  return series_normalised, scaler_10

def scaler_recoverary(series_normalised, scaler_10):
  return series_normalised*scaler_10

## Scale based on daily average and derivative (weather data)
def scaler_normalization(series_ori, m):
  '''waiting to be finished'''
  sliding = series_ori.shape[0]//m
  sample_series = series_ori.reshape(sliding, m)
  scaler_max = np.max(sample_series, axis=1)
  scaler_min = np.min(sample_series, axis=1)
  scaler_10 = (scaler_max - scaler_min)/10
  scaler_10 = scaler_10.repeat(m)
  series_normalised = series_ori/scaler_10
  return series_normalised, scaler_10

def scaler_recoverary(series_normalised, scaler_10):
  return series_normalised*scaler_10



## Generate ideal profile

def ideal_profile_generator(daily_consumption, additional_generation, tariff, *constraints):
    '''
    input the daily consumption, the shape to follow, tariff profile, regulation_profile and constraints as profile
    all input profiles should be in the same shape.
    Constraints should be a list of two profiles, the first one is the lower bound and the second one is the upper bound.
    output is the ideal profile considering the constraints, consumption, and other inputs
    regulation service can be considered as contraints or additional generation
    priority: constraints > additional_generation > tariff 
    '''
    if len(constraints) == 2:
        min_bound = constraints[0]
        max_bound = constraints[1]
    elif len(constraints) == 1:
        min_bound = constraints[0]
        max_bound = np.full((additional_generation.shape), np.inf)
    else:
        print('No constraints are given')
        min_bound = np.zeros((additional_generation.shape))
        max_bound = np.full((additional_generation.shape), np.inf)

    ideal_profile_naive = np.maximum(additional_generation, min_bound)
    residual = daily_consumption - np.sum(ideal_profile_naive)

    if residual <= 0:
        return ideal_profile_naive * daily_consumption / ideal_profile_naive.sum()

    else:
        # Group timestamps by tariff
        unique_tariffs, inverse_indices = np.unique(tariff, return_inverse=True)
        for tariff_level in unique_tariffs:
            indices_at_this_tariff = np.where(tariff == tariff_level)[0]
            remaining_slots = len(indices_at_this_tariff)

            # Evenly distribute the residual energy across timestamps with the same tariff
            for i in indices_at_this_tariff:
                adjust = max_bound[i] - ideal_profile_naive[i]
                share_of_residual = residual / remaining_slots

                if share_of_residual >= adjust:
                    ideal_profile_naive[i] += adjust
                    residual -= adjust
                else:
                    ideal_profile_naive[i] += share_of_residual
                    residual -= share_of_residual
                
                remaining_slots -= 1

            if residual <= 0:
                break

    return ideal_profile_naive


def ramping_swinging_door(time_series, capacity, window_size, up_thres = 0.05, down_thres = 0.03):
    '''ramping and swinging door algorithm to detect the ramping event and swinging event'''
    up_amp = capacity*up_thres
    down_amp = capacity*down_thres
    window_size = int(window_size)
    sliding_steps = int(len(time_series)-window_size)
    ### initialise state
    up_labels = np.zeros((len(time_series)))
    down_labels = np.zeros((len(time_series)))
    for i in range(sliding_steps):
        for j in range(i,i+window_size):
            if time_series[j]-time_series[i]>up_amp:
                up_labels[i:j+1]=1
                break
            if time_series[i]-time_series[j]>down_amp:
                down_labels[i:j+1]=1
                break
    return up_labels, down_labels

def code_book_processing_analysis(codebook_obj, time_index, report = False, export_dir = '.'):
    """
    This function will generate a report of the codebook processing results, including the compression rate, 
    the uploaded data vs original data, the number of codewords stored at users end, the top five repeated codewords, 
    and the reconstructed data vs original data.

    Parameters:
    codebook_obj (Code_book): the processed code book object
    time_index (list): the time index of the original time series
    report (bool): whether to export a report or not, default is False
    export_dir (str): the directory to export the report, default is '.'
    """
    original_series = codebook_obj.time_series
    recovered_series = codebook_obj.recovered_series
    representations = codebook_obj.labels
    upload_scalers = codebook_obj.scaler_average[::codebook_obj.m]
    time_resampled = time_index[::codebook_obj.m]
    upload_data = list(zip(representations, upload_scalers))
    codewords = codebook_obj.pattern_stack
    compression_rate = (original_series.shape[0]-len(representations)) /original_series.shape[0]
    top_5_Codewords = Counter(representations).most_common(5)
    top_5_indexs = [int(i[0].split('-')[1]) for i in top_5_Codewords]

    print(f"While original data has length {len(original_series)}")
    print(f"The data uploaded to clourd is (representations, series_codebook.scaler_average)")
    print(f"With length {len(representations)} and compression rate {compression_rate}")
    print(f"The number of codewords that user's end at: {len(codewords)}")
    print(f"The reconstructed data is  series_codebook.recovered_series")

    fig = go.Figure()
    fig.add_trace(
            go.Scatter(
                x=time_index, y=original_series, name = 'Original series',
                line_width=3, opacity=0.7, line_color=THEME_COLOR[16]
            )
        )
    
    fig.add_trace(
            go.Scatter(
                x=time_index, y=recovered_series, name = 'Reconstructed series',
                line_width=3, opacity=0.8, line_color=THEME_COLOR[-1]
            )
        )
    
    fig.update_layout(
        title="Reconstructed series vs Original series",
        xaxis_title="Time",
        yaxis_title="Power (kW)",
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Times New Roman", size=20),
        width=1200, 
        height=500,
        legend=dict(
            orientation="h",
            x=0.5,
            y=1.1,
            xanchor="left",
            yanchor="bottom"
        )
    )
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True,showgrid=False)
    ##, tickangle = 45 
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, showgrid=False)
    fig_html = plotly.io.to_html(fig, include_plotlyjs=False, full_html=False)
    fig.show()

    fig_2 = go.Figure()
    fig_2.add_trace(
        go.Scatter(
            x=time_index, y=series_codebook.time_series, name = 'Original data',
            line_width=3, opacity=0.7, line_color=THEME_COLOR[16]
        )
    )
    fig_2.add_trace(
            go.Scatter(
                x=time_resampled, y=upload_scalers, name = 'Uploaded data', customdata=representations, 
                hovertemplate='<b>Time:</b> %{x}<br>' +
                        '<b>Scaler:</b> %{y}<br>' +
                        '<b>Representation:</b> %{customdata}<extra></extra>',
                line_width=3, opacity=0.7, line_color=THEME_COLOR[13]
            )
        )
    fig_2.update_layout(
        title="Original series vs uploaded series",
        xaxis_title="Time",
        yaxis_title="Power (kW)",
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Times New Roman", size=20),
        width=1200, 
        height=500,
        legend=dict(
            orientation="h",
            x=0.6,
            y=1.1,
            xanchor="left",
            yanchor="bottom"
        )
    )
    fig_2.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True,showgrid=False)
    ##, tickangle = 45 
    fig_2.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, showgrid=False)
    fig_2_html = plotly.io.to_html(fig_2, include_plotlyjs=False, full_html=False)

    fig_3 = go.Figure()
    for num, i in enumerate(top_5_indexs):
        fig_3.add_trace(
            go.Scatter(
                x=time_index[:codebook_obj.m], y=codewords[i], name = f'Pattern_{i}: {top_5_Codewords[num][1]}',
                line_width=3, opacity=0.8, line_color=THEME_COLOR[num]
            )
        )
    fig_3.update_layout(
        title="Top 5 Codewords in disttributed storage",
        xaxis_title="Time",
        yaxis_title="Power (kW)",
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Times New Roman", size=20),
        width=1200, 
        height=500,
        legend=dict(
            orientation="h",
            x=0,
            y=0.85,
            xanchor="left",
            yanchor="bottom"
        )
    )
    fig_3.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True,showgrid=False)
    ##, tickangle = 45 
    fig_3.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, showgrid=False)
    fig_3_html = plotly.io.to_html(fig_3, include_plotlyjs=False, full_html=False)

    if report:
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Codebook Processing Report</title>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        </head>
        <body>
            <h1>Codebook Processing Report</h1>
            <h2>The given time series is processed and the compression rate is {compression_rate}</h2>
            <h2>The Uploded data VS Original data</h2>
            {fig_2_html}
            <h2>The number of Codewords stored at users end: {len(codewords)}</h2>
            <h2>The top five repeated codewords are:</h2>
            {fig_3_html}
            <h2>The Reconstructed data VS Original data</h2>
            {fig_html}
        </body>
        </html>
        """
        with open(f"{export_dir}//dispatch_results_daily.html", "w") as file:
            file.write(html_template)