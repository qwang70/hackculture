import numpy as np
import pandas as pd
# plotly
import plotly
import plotly.plotly as py
from plotly.graph_objs import *

# import csv data
SalaryOverYears = pd.read_csv("https://raw.githubusercontent.com/qwang70/hackculture/master/csv/SalaryOverYears.csv")

def getSalary(department, campus, year_col):
    salary = SalaryOverYears.loc[\
                (SalaryOverYears['Department'] == department) \
                & (SalaryOverYears['Campus'] == campus), year_col].dropna()
    return salary


def createFigHist(departments, campus, year = 2017):
    assert len(departments) == len(campus)
    
    # if year is a int, cast to a list
    if type(year) is int:
        year = [year]*len(campus)
    else:
        assert type(year) is list
        assert len(year) == len(campus)
        
    # get the salary
    data = []
    for idx in range(len(departments)):
        year_col = "Salary" + str(year[idx])
        salary = getSalary(departments[idx], campus[idx], year_col)
        data.append(Histogram(
            x=salary,
            histnorm='percent',
            name=departments[idx],
            opacity=0.75
        ))

    layout = Layout(
        title='Salary Range of Faculty in {}'.format(' & '.join(departments)),
        xaxis=dict(
            title='Salary'
        ),
        yaxis=dict(
            title='Percentage of Faculty'
        ),
        bargap=0.2,
        bargroupgap=0.1
    )
    fig = Figure(data=data, layout=layout)
    return fig

def createFigDiffDepAndCampus(departments, campus, year=2017):
    assert len(departments) == len(campus)
    
    # if year is a int, cast to a list
    if type(year) is int:
        year = [year]*len(campus)
    else:
        assert type(year) is list
        assert len(year) == len(campus)
        
    # get the salary
    populationSize = []
    labels = []
    medians = []
    for idx in range(len(departments)):
        year_col = "Salary" + str(year[idx])
        salary = getSalary(departments[idx], campus[idx], year_col)
        populationSize.append(len(salary))
        median = salary.median()
        medians.append(int(median))
        labels.append('{} - {}'.format(campus[idx], departments[idx]))
    # parameters used to create graph
        
    population_bar = Bar(
            x = labels,
            y = populationSize,  
            name="population size",       
            opacity=0.75,    
           )
    salary_scatter = Scatter(
            x = labels,
            y = medians,
            name="median salary",
            # marker + lines
            mode = 'lines+markers',
            line = dict(
                width = 4,),
            yaxis='y2',           
            opacity=0.75
)
    layout = Layout(
        title= "Number of Faculty and Median Salary in the Dataset",
        xaxis=dict(
            title='Department',
        ),
        yaxis=dict(
            title='Number of Faculty'
        ),
        yaxis2=dict(
            title='Median Salary',
            overlaying='y',
            side='right',
            
            # label color
            titlefont=dict(
                color='#ff7f0e'
            ),
            tickfont=dict(
                color='#ff7f0e'
            ),
        ),
        margin=Margin(
         b=160,
        ),
    )
    fig = Figure(data=[population_bar, salary_scatter], layout=layout)
    return fig
    
def createAllDepSalaryTrace(campus = "Urbana-Champaign", year = 2017, top = None):
    year_col = "Salary" + str(year)
    
    
    # get the median salary of each department
    gb = SalaryOverYears.loc[SalaryOverYears['Campus'] == campus, ["Department", year_col]].dropna()\
                .groupby(['Department'])
    agg_df = gb.agg(['median', 'count'])
    agg_df = agg_df[agg_df[(year_col, 'count')] > 5]
    sorted_depMedian = agg_df.sort_values((year_col, 'median'), ascending = False)
    x = sorted_depMedian[(year_col, 'median')].tolist()
    y = sorted_depMedian.index.tolist()
        
    # select top subset elements
    if top:
        x = x[:top]
        y = y[:top]

    x.reverse()
    y.reverse()
    return Bar(
        y=y,
        x=x,
        name='Median Salary',
        orientation = 'h',
        opacity=0.75
    )

def createFigListAllDepSalary(campus = "Urbana-Champaign", year = 2017, top = None):
    assert year >= 2013 and year <= 2017
    
    trace1 = createAllDepSalaryTrace(top=top)
    trace2 = createAllDepSalaryTrace("Chicago", year, top=top)
    trace3 = createAllDepSalaryTrace("Springfield", year, top=top)

    fig = tls.make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing = 0.05,\
              subplot_titles=('{} Median Salary of Faculty Members in Urbana-Champaign'.format(year), \
                              '{} Median Salary of Faculty Members in Chicago'.format(year), \
                              '{} Median Salary of Faculty Members in Springfield'.format(year)))

    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 2, 1)
    fig.append_trace(trace3, 3, 1)

    fig['layout'].update( \
        height=1200, width=600,
        margin=Margin(\
            l=180, \
            pad=5,
            ),\
        showlegend=False,)
    return fig
        
def createAllDepJobSalaryTrace(campus = "Urbana-Champaign", year = 2017, job = "ASST PROF", top = None):
    year_col = "Salary" + str(year)
    
    # get the median salary of each job & departmentdepartment
    gb = SalaryOverYears.loc[\
             (SalaryOverYears['Campus'] == campus) & (SalaryOverYears['JobTitle'] == job), \
             ["Department",year_col]].dropna()\
            .groupby(['Department'])
    agg_df = gb.agg(['median', 'count'])
    agg_df = agg_df[agg_df[(year_col, 'count')] > 2]
    sorted_depMedian = agg_df.sort_values((year_col, 'median'), ascending = False)
    x = sorted_depMedian[(year_col, 'median')].tolist()
    y = sorted_depMedian.index.tolist()

    # select top subset elements
    if top:
        x = x[:top]
        y = y[:top]

    x.reverse()
    y.reverse()
    return Bar(
        y=y,
        x=x,
        name='Median Salary',
        orientation = 'h',

        marker=dict(
            color='rgba(50, 171, 96, 0.7)',
            line=dict(
                color='rgba(50, 171, 96, 1.0)',
            )
        ),
        opacity=0.75
    )

def createFigListAllDepJobSalary(year = 2017, job = "ASST PROF", top = None):
    trace1 = createAllDepJobSalaryTrace(top=top)
    trace2 = createAllDepJobSalaryTrace("Chicago", year, job, top=top)
    trace3 = createAllDepJobSalaryTrace("Springfield", year, job, top=top)

    fig = tls.make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing = 0.05, \
                          subplot_titles=('{} Median Salary of {} in Urbana-Champaign'.format(year, job), \
                                          '{} Median Salary of {} in Chicago'.format(year, job), \
                                          '{} Median Salary of {} in Springfield'.format(year, job)))

    fig.append_trace(trace1, 1, 1)
    fig.append_trace(trace2, 2, 1)
    fig.append_trace(trace3, 3, 1)

    fig['layout'].update( \
        height=1200, width=600,
        margin=Margin(\
            l=180, \
            pad=5,
            ),\
        showlegend=False,
        )
    return fig

def boxPlotAllYears(department, campus):
    # get the salary
    data = []
    for year in range(2013, 2018):
        year_col = "Salary" + str(year)
        salary = getSalary(department, campus, year_col)
        data.append(Box(
            y=salary,
            boxpoints='all',
            name = year,
            jitter=0.3,
            pointpos=-1.8)
            )
    layout = Layout(
        title = "Box Plot for Faculties in {} Over 5 Years".format(department)
    )

    return Figure(data=data,layout=layout)