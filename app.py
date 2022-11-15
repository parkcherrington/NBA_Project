from shiny import App, render, ui
import pandas as pd
import matplotlib.pyplot as plt

boxdf = pd.read_csv('boxScores.csv')
totals = boxdf.groupby(['PLAYER_NAME', 'TEAM_NAME'], as_index = False).sum()
means = boxdf.groupby(['PLAYER_NAME', 'TEAM_NAME'], as_index = False).mean()

app_ui = ui.page_fluid(
    ui.input_slider('n', 'Number of Players', 0, 25, 15),
    ui.input_checkbox('avg', 'Show League Average?'),
    ui.input_radio_buttons('stat', 'Statistical Category', 
    {'PTS': "Points", 'REB': "Rebounds", 'AST': "Assists", 'FANTASY': "Fantasy Points"}),
    ui.output_plot("plot"),
)

def server(input, output, session):
    @output
    @render.plot(alt = "a barchart")
    def plot():
        fig = plt.figure()
        ax = fig.add_subplot(111)
        data = means[input.stat()].sort_values(ascending = False).head(input.n())
        plt.title(f'NBA Top {input.n()} {input.stat()} Leaders Per Game')
        plt.xlabel(input.stat())
        plt.xlabel('Player Name')
        ax.barh(means.iloc[data.index]['PLAYER_NAME'], data)
        if input.avg():
            plt.axvline(means[input.stat()].mean(), color = 'red')
        return fig
    

app = App(app_ui, server, debug = True)