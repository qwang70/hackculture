import os
import numpy as np
import pandas as pd

from textwrap import dedent as d

# plotly
import plotly
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.tools as tls

# dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html

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
    html.Br(),
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
        )]
    )

def createDropDownForDeparmentInAllCampus(id):
    departments = [ 'Information Sciences', 'Chemistry', "Communication","Computer Science",\
        "History","LAS Administration","Philosophy","Political Science","Psychology"]

    return html.Div([
        html.Label('Department:\t'),
        dcc.Dropdown(
            id=id,
            options=[{'label': i, 'value': i} for i in departments],
            value='Information Sciences',
    )])

# for job select widget
def createDropDownForJobs(id):
    jobs = ['PROF', 'ASSOC PROF', 'ASST PROF', 'LECTURER', 'ASSOC DIR',
    'CLIN ASST PROF', 'SR LECTURER', 'RES SCI', 'RES ASST PROF',
    'SR RES SCI', 'POSTDOC RES ASSOC', 'CLIN PROF',
    'ASSOC PROF UNIV LIBRARY', 'ASST PROF UNIV LIBRARY', 'DEAN',
    'JL DOOB RES ASST PROF', 'CLIN ASSOC PROF', 'VST ASST PROF',
    'RES ASSOC PROF', 'ASST DEAN', 'RES PROF', 'PROF (RT)']
    return html.Div([
        html.Label('Job Title:\t'),
        dcc.Dropdown(
            id=id,
            options=[{'label': i, 'value': i} for i in jobs],
            value='ASST PROF',
    )])

def createIntTop(id):
    return html.Div([
        html.Label('List Top \t'),
        html.Br(),
        dcc.Input(
        id=id,
        type='number',
        value=10
    )])


# start up Dash app
app = dash.Dash(__name__)
server = app.server

# bootstrap
external_css = ["https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css", ]
for css in external_css:
    app.css.append_css({"external_url": css})

external_js = ['https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js', 
                "https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"]
for js in external_js:
    app.scripts.append_script({
        "external_url": js
    })


# import fig
salary_hist_url = "https://plot.ly/~wangqiwen/22/salary-range-of-faculty-in-information-sciences/"
salary_hist = py.get_figure(salary_hist_url, raw=True)
salary_compare_url = "https://plot.ly/~wangqiwen/8/salary-range-of-faculty-in-mathematics-information-sciences/"
salary_compare = py.get_figure(salary_compare_url, raw=True)
salary_population_is_url = "https://plot.ly/~wangqiwen/24"
salary_population_is = py.get_figure(salary_population_is_url, raw=True)
list_dep_salary_url = "https://plot.ly/~wangqiwen/18/median-salary-median-salary-median-salary/"
list_dep_salary = py.get_figure(list_dep_salary_url, raw=True)
list_dep_job_salary_url = "https://plot.ly/~wangqiwen/20/median-salary-median-salary-median-salary/"
list_dep_job_salary = py.get_figure(list_dep_job_salary_url, raw=True)
salary_boxplot_url = "https://plot.ly/~wangqiwen/44/box-plot-for-faculties-in-computer-science-over-5-years/"
salary_boxplot = py.get_figure(salary_boxplot_url, raw=True)

app.layout = html.Div([

    html.Div([
    html.Div([

    # navigation bar
    dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
    <ul class="nav nav-tabs flex-column">
        <li class="active"><a data-toggle="tab" href="#home">Home</a></li>
        <li><a data-toggle="tab" href="#menu1">Give it an awesome name (distribution)</a></li>
        <li><a data-toggle="tab" href="#menu2">Give it an awesome name (comparation)</a></li>
        <li><a data-toggle="tab" href="#menu3">Give it an awesome name (population + salary)</a></li>
        <li><a data-toggle="tab" href="#menu4">Give it an awesome name (list salary)</a></li>
        <li><a data-toggle="tab" href="#menu5">Give it an awesome name (dep over years)</a></li>
    </ul>
    '''),
    # tab content
    html.Div([
            # Project description
            html.Div([
                dcc.Markdown(d("""
                        ## Project description

                        ### Some desciptions..........please add....
                    """)),
            ], id="home", className="tab-pane fade in active"),

            # show distribution of the salary
            # div for each widget + graph
            html.Div([
                dcc.Markdown(d("""
                        ## Please add some explanation to the graph here.
                    """)),
                # div for each widget
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

                # div for each graph
                dcc.Graph(
                    id='salary_hist',
                    figure=salary_hist)
            ], id="menu1", className="tab-pane fade"),
            
            # compare 2 department salaries
            # div for each widget + graph
            html.Div([
                dcc.Markdown(d("""
                        ## Please add some explanation to the graph here.
                """)),
                # div for each widget
                # first row
                dcc.Markdown(d("""
                    #### Main Department
                """)),
                html.Div([
                    html.Div([
                    
                    createDropDownForCampus(id="salary_compare_campus_dropdown1")],
                    className="col-md-4"),
                    html.Div([
                    createTextBoxForDep(id="salary_compare_department_textbox1")],
                    className="col-md-4"),
                    html.Div([
                    createIntSliderForYear(id="salary_compare_year1")], 
                    className="col-md-4")

                ], className="row"),
                # second row
                dcc.Markdown(d("""
                    #### Secondary Department
                """)),
                html.Div([
                    html.Div([
                    createDropDownForCampus(id="salary_compare_campus_dropdown2")],
                    className="col-md-4"),
                    html.Div([
                    createTextBoxForDep(id="salary_compare_department_textbox2", v="Information Sciences")],
                    className="col-md-4"),
                    html.Div([
                    createIntSliderForYear(id="salary_compare_year2")], 
                    className="col-md-4")

                ], className="row"),
                # graoh
                dcc.Graph(
                    id='salary_compare',
                    figure=salary_compare
                )
            ], id="menu2", className="tab-pane fade"),
            # compare job across the campus
            # div for each widget + graph
            html.Div([
                dcc.Markdown(d("""
                        ## Please add some explanation to the graph here.

                        #### Graph to compare salaries across the campus

                        ##### Observation: Springfield has the least population, Urbana-Champiang has the most faculty population in the dataset.
                        For most of the department,  Springfield has the least median salary in the dataset.
                    """)),
                # div for each widget
                html.Div([
                    html.Div([
                    createDropDownForDeparmentInAllCampus(id="salary_across_campus_dropdown")],
                    className="col-md-4"),
                    html.Div([
                    createIntSliderForYear(id="salary_across_campus_year")], 
                    className="col-md-4")

                ], className="row"),

                # div for each graph
                dcc.Graph(
                    id='salary_across_campus',
                    figure=salary_population_is)
            ], id="menu3", className="tab-pane fade"),
            # list median department salary
            # div for each widget + graph
            html.Div([
                html.Div([
                    dcc.Markdown(d("""
                            ## Please add some explanation to the graph here.

                            #### Median Salary of Faculty Members

                        """)),
                    # div for each graph
                    dcc.Graph(
                        id='median_salary_all_faculty',
                        figure=list_dep_salary)
                ]),
                # list median department salary for jobs
                # div for each widget + graph
                html.Div([
                    dcc.Markdown(d("""
                            ## Please add some explanation to the graph here.

                            #### Median salary of the selected job
                        """)),
                    # div for each widget
                    html.Div([
                        html.Div([
                        createDropDownForJobs(id="list_dep_job_salary_dropdown")],
                        className="col-md-4"),
                        html.Div([
                        createIntSliderForYear(id="list_dep_job_salary_year")], 
                        className="col-md-4"),
                        html.Div([
                        createIntTop(id="list_dep_job_salary_top")], 
                        className="col-md-4")

                    ], className="row"),

                    # div for each graph
                    dcc.Graph(
                        id='list_dep_job_salary',
                        figure=list_dep_job_salary)
            ]),
            ], id="menu4", className="tab-pane fade"),
            html.Div([
                dcc.Markdown(d("""
                        ## Please add some explanation to the graph here.
                    """)),
                # div for each widget
                html.Div([
                    html.Div([
                    createDropDownForCampus(id="salary_dist_boxplot_dropdown")],
                    className="col-md-4"),
                    html.Div([
                    createTextBoxForDep(id="salary_dist_boxplot_textbox")],
                    className="col-md-4"),

                ], className="row"),

                # div for each graph
                dcc.Graph(
                    id='salary_boxplot',
                    figure=salary_boxplot)
            ], id="menu5", className="tab-pane fade"),
            
            
        ], className="tab-content"),
    ], className="col-md-3"),
    ], className="row"),
], className="container", style={"padding": "10%"}
)

# app callback
# boxplot
@app.callback(
    dash.dependencies.Output('salary_boxplot', 'figure'),
    [dash.dependencies.Input('salary_dist_boxplot_dropdown', 'value'),
    dash.dependencies.Input('salary_dist_boxplot_textbox', 'value')],
    [dash.dependencies.State('salary_boxplot', 'figure')])
def update_salary_dist(dropdown_val, textbox_val, fig):
    department = textbox_val
    campus = dropdown_val
    new_fig = boxPlotAllYears(department, campus=campus)
    if len(new_fig.data[0].y) > 0:
        fig = new_fig
    return fig

# list department job salary
@app.callback(
    dash.dependencies.Output('list_dep_job_salary', 'figure'),
    [dash.dependencies.Input('list_dep_job_salary_dropdown', 'value'),
    dash.dependencies.Input('list_dep_job_salary_year', 'value'),
    dash.dependencies.Input('list_dep_job_salary_top', 'value')],
    [dash.dependencies.State('list_dep_job_salary', 'figure')])
def update_list_dep_job_salary(dropdown_val, year_val, top_val, fig):
    year = year_val
    job = dropdown_val
    top = top_val
    print(year, job, top)
    if top > 2:
        # traces
        traces =[ createAllDepJobSalaryTrace(year=year, job=job, top=top),
            createAllDepJobSalaryTrace("Chicago", year=year, job=job, top=top),
            createAllDepJobSalaryTrace("Springfield", year=year, job=job, top=top) ]
        
        # update subplot titles
        subplot_titles=('{} Median Salary of {} in Urbana-Champaign'.format(year, job), \
                    '{} Median Salary of {} in Chicago'.format(year, job), \
                    '{} Median Salary of {} in Springfield'.format(year, job))
        # update style and layout
        if len(traces[0].x) > 0:
            for idx in range(3):
                fig["data"][idx]['x'] = traces[idx].x
                fig["data"][idx]['y'] = traces[idx].y
                fig["layout"]['annotations'][idx]['text'] = subplot_titles[idx]
        
    return fig

@app.callback(
    dash.dependencies.Output('salary_across_campus', 'figure'),
    [dash.dependencies.Input('salary_across_campus_dropdown', 'value'),
    dash.dependencies.Input('salary_across_campus_year', 'value')],
    [dash.dependencies.State('salary_across_campus', 'figure')])
def update_salary_dist(dropdown_val, year_val, fig):
    year = year_val
    if dropdown_val == 'Information Sciences':
        departments = ["Management Information Systems", "Information/Decision Sciences", "Information Sciences"]
    else:
        departments = [dropdown_val]*3
    campus = [ "Springfield", "Chicago", "Urbana-Champaign" ]
    new_fig = createFigDiffDepAndCampus(departments, campus=campus, year=year)
    if len(new_fig.data[0].x) > 0:
        fig = new_fig
    return fig

@app.callback(
    dash.dependencies.Output('salary_compare', 'figure'),
    [dash.dependencies.Input('salary_compare_campus_dropdown1', 'value'),
    dash.dependencies.Input('salary_compare_department_textbox1', 'value'),
    dash.dependencies.Input('salary_compare_year1', 'value'),
    dash.dependencies.Input('salary_compare_campus_dropdown2', 'value'),
    dash.dependencies.Input('salary_compare_department_textbox2', 'value'),
    dash.dependencies.Input('salary_compare_year2', 'value')],
    [dash.dependencies.State('salary_compare', 'figure')])
def update_salary_compare(dropdown_val1, textbox_val1, year_val1, dropdown_val2, textbox_val2, year_val2,  fig):
    years = [year_val1,year_val2] 
    departments = [textbox_val1, textbox_val2]
    campus = [dropdown_val1, dropdown_val2]
    
    new_fig = createFigHist(departments, campus=campus, year=years)
    if len(new_fig.data) == 2 and len(new_fig.data[0].x) > 0 and len(new_fig.data[1].x) > 0:
        fig = new_fig
    return fig

@app.callback(
    dash.dependencies.Output('salary_hist', 'figure'),
    [dash.dependencies.Input('salary_dist_campus_dropdown', 'value'),
    dash.dependencies.Input('salary_dist_department_one_textbox', 'value'),
    dash.dependencies.Input('salary_dist_year_container', 'value')],
    [dash.dependencies.State('salary_hist', 'figure')])
def update_salary_dist(dropdown_val, textbox_val, year_val, fig):
    year = year_val
    department = [textbox_val]
    campus = [dropdown_val]
    new_fig = createFigHist(department, campus=campus, year=year)
    if len(new_fig.data[0].x) > 0:
        fig = new_fig
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
