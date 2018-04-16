import numpy as np
import pandas as pd
# plotly
import plotly
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.tools as tls

# dash
import dash
import dash_core_components as dcc
import dash_html_components as html

# helper
from helper_fig import *


# define widgets
def createIntSliderForYear(id):
    return html.Div([
        html.Label('Year'),
        dcc.Slider(
            id=id,
            value=2017,
            min=2013,
            max=2017,
            step=1,
            marks={"2013": 2013, "2014": 2014, "2015": 2015, "2016": 2016, "2017": 2017},
            #labelStyle={'display': 'inline-block'}
        )]
    )


def createTextBoxForDep(id, v="Mathematics"):
    return html.Div([
    html.Label('Department:\t'),
    dcc.Input(
        id=id, 
        value=v, 
        type='text',
        #labelStyle={'display': 'inline-block'}
        )]
    )

def createDropDownForCampus(id):
    return html.Div([
        html.Label('Campus:\t'),
        dcc.Dropdown(
            id=id,
            options=[{'label': i, 'value': i} for i in ["Chicago", "Springfield", "Urbana-Champaign"]],
            value='Urbana-Champaign',
            #labelStyle={'display': 'inline-block'}
        )]
    )

"""
def createBundle(v="Mathematics"):
    return [ createDropDownForCampus(), createTextBoxForDep(v), createIntSliderForYear()]
# for job select widget
def createDropDownForJobs():
    jobs = ['PROF', 'ASSOC PROF', 'ASST PROF', 'LECTURER', 'ASSOC DIR',
    'CLIN ASST PROF', 'SR LECTURER', 'RES SCI', 'RES ASST PROF',
    'SR RES SCI', 'POSTDOC RES ASSOC', 'CLIN PROF',
    'ASSOC PROF UNIV LIBRARY', 'ASST PROF UNIV LIBRARY', 'DEAN',
    'JL DOOB RES ASST PROF', 'CLIN ASSOC PROF', 'VST ASST PROF',
    'RES ASSOC PROF', 'ASST DEAN', 'RES PROF', 'PROF (RT)']
    return widgets.Dropdown(
        options=jobs,
        value='ASST PROF',
        description='Job Title:',
    )
def createIntTop():
    return widgets.IntText(
        value=10,
        description='Top X:',
        disabled=False
    )
"""


# start up Dash app
app = dash.Dash('')

# bootstrap
external_css = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css", ]
for css in external_css:
    app.css.append_css({"external_url": css})


# import fig
salaryHist_url = "https://plot.ly/~wangqiwen/22/salary-range-of-faculty-in-information-sciences/"
# Assign an emptry graph widget with two traces
salaryHist = py.get_figure(salaryHist_url, raw=True)

app.layout = html.Div([
        html.Div([
            html.Div([
            createDropDownForCampus(id="salary_dist_campus_dropdown")],
            className="col-md-4"),
            html.Div([
            createTextBoxForDep(id="salary_dist_department_one_textbox")],
            className="col-md-4"),
            html.Div([
            createIntSliderForYear(id="salary_dist_year_container")], 
            className="col-md-4")

        ], className="row"),
    dcc.Graph(
        id='salaryHist',
        figure=salaryHist)
], className="container", style={"padding": "10%"}
)

# app callback
@app.callback(
    dash.dependencies.Output('salaryHist', 'figure'),
    [dash.dependencies.Input('salary_dist_campus_dropdown', 'value'),
    dash.dependencies.Input('salary_dist_department_one_textbox', 'value'),
    dash.dependencies.Input('salary_dist_year_container', 'value')],
    [dash.dependencies.State('salaryHist', 'figure')])
def update_graph(dropdown_val, textbox_val, year_val, fig):
    year = year_val
    department = [textbox_val]
    campus = [dropdown_val]
    print(year, department, campus)
    print(fig)
    new_fig = createFigHist(department, campus=campus, year=year)
    if len(new_fig.data[0].x) > 0:
        fig = new_fig
    return fig


if __name__ == '__main__':
    app.run_server()
