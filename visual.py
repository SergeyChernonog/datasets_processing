import collections

import bokeh
import bokeh.plotting
import numpy as np
import pandas as pd


def plot_guitar_sequence(sequence):
    """Creates an interactive pianoroll for a NoteSequence.
    Args:
       sequence: A NoteSequence.
       show_figure: A boolean indicating whether or not to show the figure.
    """

    def _sequence_to_pandas_dataframe(sequence):
        """Generates a pandas dataframe from a sequence."""
        pd_dict = collections.defaultdict(list)
        for note in sequence.notes:
            pd_dict['start_time'].append(note.start)
            pd_dict['end_time'].append(note.end)
            pd_dict['duration'].append(note.end - note.start)
            pd_dict['pitch'].append(note.pitch)
            pd_dict['bottom'].append(note.pitch - 0.4)
            pd_dict['top'].append(note.pitch + 0.4)
            pd_dict['velocity'].append(note.velocity)
            pd_dict['fill_alpha'].append(note.velocity / 128.0)

        # If no velocity differences are found, set alpha to 1.0.
        if np.max(pd_dict['velocity']) == np.min(pd_dict['velocity']):
            pd_dict['fill_alpha'] = [1.0] * len(pd_dict['fill_alpha'])

        return pd.DataFrame(pd_dict)

    # These are hard-coded reasonable values, but the user can override them
    # by updating the figure if need be.
    fig = bokeh.plotting.figure(
        tools='hover,pan,box_zoom,reset,save')
    fig.plot_width = 800
    fig.plot_height = 400
    fig.xaxis.axis_label = 'time (sec)'
    fig.yaxis.axis_label = 'pitch (MIDI)'
    fig.yaxis.ticker = bokeh.models.SingleIntervalTicker(interval=12)
    fig.ygrid.ticker = bokeh.models.SingleIntervalTicker(interval=12)
    # Pick indexes that are maximally different in Spectral8 colormap.
    spectral_color_indexes = [7, 0, 6, 1, 5, 2, 3]

    # Create a Pandas dataframe and group it by instrument.
    dataframe = _sequence_to_pandas_dataframe(sequence)
    instruments = sorted(set(dataframe['instrument']))
    grouped_dataframe = dataframe.groupby('instrument')
    for counter, instrument in enumerate(instruments):
        instrument_df = grouped_dataframe.get_group(instrument)
        color_idx = spectral_color_indexes[counter % len(spectral_color_indexes)]
        color = bokeh.palettes.Spectral8[color_idx]
        source = bokeh.plotting.ColumnDataSource(instrument_df)
        fig.quad(top='top', bottom='bottom', left='start_time', right='end_time',
                 line_color='black', fill_color=color,
                 fill_alpha='fill_alpha', source=source)
    fig.select(dict(type=bokeh.models.HoverTool)).tooltips = (
        {'pitch': '@pitch',
         'duration': '@duration',
         'start_time': '@start_time',
         'end_time': '@end_time',
         'velocity': '@velocity',
         'fill_alpha': '@fill_alpha',
         'style': '@style'
         })

    bokeh.plotting.output_notebook()
    bokeh.plotting.show(fig)
    return fig

new_name = '/home/moby/PycharmProjects/data//IDMT-SMT-GUITAR_V2/dataset2/audio/AR_Lick1_FVSDN.wav'
