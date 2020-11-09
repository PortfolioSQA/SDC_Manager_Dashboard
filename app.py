import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import dash_bootstrap_components as dbc
import dash_table
import pandas as pd
from etl2 import load_data
from datetime import date
import urllib
from dash.dash import no_update
from datetime import datetime as dt
from dateutil import tz
import plotly.express as px
import plotly.graph_objects as go

# sample data
a = pd.read_csv('harvest_database_example.csv', index_col = 'file_identifier')
b = pd.read_csv('related_identifiers_example.csv')

df = load_data(a, b)
df['datasource'] = df['datasource'].fillna('Unknown')

# get a set of sorted science centers for dropdown menu
SC = set(df['datasource'])
sorted_SC = sorted(SC)

#used for default pie chart
value_counts = df.status.value_counts()

#used to plot the releases over time
df1 = df.copy()
df1.mdate = pd.to_datetime(df1.mdate)
dfg = df1.groupby('mdate').count()
dfg = dfg.rename(columns={"datasource": "Count"})


################
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# USGS & ScienceBase Headers and Footers
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>      
        {%css%}
	<link rel="icon" type="image/png" href="../assets/favicons/favicon-16x16.png" sizes="16x16">	
	<link rel="icon" type="image/png" href="../assets/favicons/favicon-32x32.png" sizes="32x32">
	<link href="https://fonts.googleapis.com/css?family=Abel|Asap|Barlow+Condensed|Dosis&display=swap" rel="stylesheet">	
	<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.0/css/all.css" integrity="sha384-lZN37f5QGtY3VHgisS14W3ExzMWZxybE1SJSEsQp9S+oqd12jhcu+A56Ebc1zFSJ" crossorigin="anonymous">
	
	<!-- START USGS Google Tag Manager -->
	<script></script>
	<!-- END USGS Google Tag Manager -->	
    </head>
    <body>
	
	<!-- opening div for body -->
	<div class="tmp-container">
	  <div class="row">
		<div class="col-12"> 
		  <!-- BEGIN USGS Applications Header Template -->
		  <header id="navbar" class="header-nav"  role="banner">
			<div class="tmp-container"> 
			  <!-- primary navigation bar --> 
			  <!-- search bar-->
			  <div class="header-search"> <a class="logo-header" href="https://www.usgs.gov/" title="Home"> <img src="../assets/images/logo.png" alt="Home" class="img" border="0" /> </a> </div>
			  <!-- end search bar--> 
			</div>
			<!-- end header-container--> 
		  </header>
		  <!-- END USGS Applications Header Template --> 
		</div>
	  </div>

	  <!-- BEGIN SDC_Dashboard Header and Navigation -->
	 <!-- BEGIN Navigation Template -->	
 	<div class="row">
	<div class="col-12">
		<div class="nav-background clearIt">	
		<nav class="navbar navbar-light">
		<a class="sb navbar-brand" href="#"><img src="../assets/images/powered_by_sb.png" alt="Powered by SDC_Dashboard" /> Science Data Catalog Dash</a>
		</nav>	
		</div>	
	</div>
	</div>
<!-- END Navigation Template -->
	  <!-- END SDC_Dashboard Header and Navigation -->

	  <div id="maincontent headquarters"> <!-- opening div for USGS VisId main content --> 
		<!-- BEGIN SDC_Dashboard Image and Header Content -->
		<div class="row clearIt">
		  <div class="col-md-12 top-section">
			<h1>SDC Management Dashboard</h1>
			<p>View datasets and statistics filtered by science data center, date, and/or status.<br>
			<a href="#">Learn more about how these metrics are calculated. </a></p>
			 <p>Questions? Contact us at: <a href="mailto:sashaqanderson@gmail.com">sashaqanderson@gmail.com</a></p>
		  </div>
		</div>
		<!-- END SDC_Dashboard Image and Header Content -->
		
			{%app_entry%}  
            {%config%}
            {%scripts%}
            {%renderer%}     
		
		<!-- End Page Content and Image Template -->
		<div class="sb-footer">
		  <div class="row">
			<div class="col-md-4 col-sm-4 col-xs-4 align-left">Contact Us: <a href="mailto:sashaqanderson@gmail.com">sashaqanderson@gmail.com</a> <br />
			  Updates: <a href="#">Sign Up</a> <br />
			  <img src="../assets/images/kisspng-quotation-marks.jpg" alt="starting quotation mark" height="15px;" /><a href="#">Cite Science Data Catalog</a> </div>
			<div class="col-md-4 col-sm-4 col-xs-4 ">
			  <center>
				<br />
				<a href="#">Home</a> &nbsp;|&nbsp; <a href="#">Terms of Use</a> &nbsp;|&nbsp; <a href="#">About</a> &nbsp;|&nbsp; <a href="#">Report Problem</a>
			  </center>
			</div>
			<div class="col-md-4 col-sm-4 col-xs-4 updates">Version: 0.0.1 <br />
			  Last Updated: Tuesday, August 17, 2019 </div>
		  </div>
		</div>
	  </div><!-- closing div for USGS VisId main content -->  

	  <!-- BEGIN USGS Footer Template -->
	  <footer class="footer">
		<div class="tmp-container"> 
		  <!-- .footer-wrap --> 
		  <!-- .footer-doi -->
		  <div class="footer-doi"> 
			<!-- footer nav links -->
			<ul class="menu nav">
			  <li class="first leaf menu-links menu-level-1"><a href="https://www.doi.gov/privacy">DOI Privacy Policy</a></li>
			  <li class="leaf menu-links menu-level-1"><a href="https://www.usgs.gov/laws/policies_notices.html">Legal</a></li>
			  <li class="leaf menu-links menu-level-1"><a href="https://www2.usgs.gov/laws/accessibility.html">Accessibility</a></li>
			  <li class="leaf menu-links menu-level-1"><a href="https://www.usgs.gov/sitemap.html">Site Map</a></li>
			  <li class="last leaf menu-links menu-level-1"><a href="https://answers.usgs.gov/">Contact USGS</a></li>
			</ul>
			<!--/ footer nav links --> 
		  </div>
		  <!-- /.footer-doi -->

		  <hr>

		  <!-- .footer-utl-links -->
		  <div class="footer-doi">
			<ul class="menu nav">
			  <li class="first leaf menu-links menu-level-1"><a href="https://www.doi.gov/">U.S. Department of the Interior</a></li>
			  <li class="leaf menu-links menu-level-1"><a href="https://www.doioig.gov/">DOI Inspector General</a></li>
			  <li class="leaf menu-links menu-level-1"><a href="https://www.whitehouse.gov/">White House</a></li>
			  <li class="leaf menu-links menu-level-1"><a href="https://www.whitehouse.gov/omb/management/egov/">E-gov</a></li>
			  <li class="leaf menu-links menu-level-1"><a href="https://www.doi.gov/pmb/eeo/no-fear-act">No Fear Act</a></li>
			  <li class="last leaf menu-links menu-level-1"><a href="https://www2.usgs.gov/foia">FOIA</a></li>
			</ul>
		  </div>
		  <!-- /.footer-utl-links --> 
		  <!-- .footer-social-links -->
		  <div class="footer-social-links">
			<ul class="social">
			  <li class="follow">Follow</li>
			  <li class="twitter"> <a href="https://twitter.com/usgs" target="_blank"> <i class="fa fa-twitter-square"><span class="only">Twitter</span></i> </a> </li>
			  <li class="facebook"> <a href="https://facebook.com/usgeologicalsurvey" target="_blank"> <i class="fa fa-facebook-square"><span class="only">Facebook</span></i> </a> </li>
			  <li class="googleplus"> <a href="https://plus.google.com/112624925658443863798/posts" target="_blank"> <i class="fa fa-google-plus-square"><span class="only">Google+</span></i> </a> </li>
			  <li class="github"> <a href="https://github.com/usgs" target="_blank"> <i class="fa fa-github"><span class="only">GitHub</span></i> </a> </li>
			  <li class="flickr"> <a href="https://flickr.com/usgeologicalsurvey" target="_blank"> <i class="fa fa-flickr"><span class="only">Flickr</span></i> </a> </li>
			  <li class="youtube"> <a href="https://youtube.com/usgs" target="_blank"> <i class="fa fa-youtube-play"><span class="only">YouTube</span></i> </a> </li>
			  <li class="instagram"> <a href="https://instagram.com/usgs" target="_blank"> <i class="fa fa-instagram"><span class="only">Instagram</span></i> </a> </li>
			</ul>
		  </div>
		  <!-- /.footer-social-links --> 
		</div>
		<!-- /.footer-wrap --> 
	  </footer>
	</div>
	<!-- END USGS Footer Template- -->	
	
	<!-- START USGS Google Tag Manager (noscript) -->
	<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=" 
	height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
	<!-- END USGS Google Tag Manager (noscript) -->
    </body>
</html>
"""


row = html.Div(
    [
        # START Layout for Data by
        html.Div(
            [
                dbc.Col(html.Div("Filter Datasets by:", className="explore-sb-row-h2",), lg=12),
                html.Div(
                    [
                        html.Div(
                        [
                        #     html.Div(
                        # className="explore-sb-box header-h3",
                        #     ),
                        html.Div(
                            [html.Div('Organization of Interest:'),
                                    dcc.Dropdown(
                                        id='sci_center',
                                        style={
                                            'height': '2px', 
                                            # 'width': '100px', 
                                            'font-size': "75%",
                                            'min-height': '1px',
                                            },
                                        options= [{'label': 'All Science Centers', 'value': 'All'}] + [{'label': str(item),'value': str(item)}
                                                  for item in sorted_SC],
                                        value= 'All'),
                            html.P(),
                            html.Br(),                           
                            dbc.FormGroup(
                                [
                                    dbc.Label("Status"),
                                    dbc.RadioItems(
                                        options=[
                                            {"label": "All", "value": 'all_status'},
                                            {"label": "Active", "value": 'active'},
                                            {"label": "Inactive", "value": 'inactive'},
                                        ],
                                        value='all_status',
                                        id="status",
                                    ),
                                ]
                            ),
                            html.Div(id='output-container-button')
                            ],
                        className="explore-sb-box header-h3",
                                 ),
                        ],
                        ),
                    ],
                    className="col-lg-6 col-md-6 col-sm-12",
                ),
                html.Div(
                    [
                        html.Div(
                            [dbc.FormGroup(
                                [
                                    dbc.Label("Date type:"),
                                    dbc.RadioItems(
                                        options=[
                                            {"label": "Beginning Date", "value": 'beg_date'},
                                            {"label": "End Date", "value": 'end_date'},
                                            {"label": "Last Updated", "value": 'mdate'},
                                            {"label": "Last Harvest", "value": 'last_harv'},
                                        ],
                                        style = {'font-size':'17px'},
                                        value='beg_date',
                                        id="date_type",
                                    ),
                                ],
                            ),
                        html.Div("Date range:"),
                        html.Div(dcc.DatePickerRange(
                            id='date-picker-range',
                            min_date_allowed = date(1700, 1, 1),
                            max_date_allowed = date.today(),
                            initial_visible_month = date.today(),
                            start_date = date(1700, 1, 1),
                            end_date = date.today(),
                        )
                        ),
                        html.Div(id='output-container-date-picker-range')],
                            className="explore-sb-box header-h3",
                        ),
                    ],
                    className="col-lg-6 col-md-6 col-sm-12",
                ),
            ],
            className="row clearIt bg-light explore-sb-row",
        ),
        # END Layout for Data by
        # START Layout for Select an Organization of Interest
        html.Div(
            [
                dbc.Col(
                    html.Div(
                        "Dataset Count Results:",
                        className="explore-sb-row-h2",
                    ),
                    lg=12,
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3("Total Data Published"),
                                html.Div(dcc.Loading(id='loading-3',
                                                   children=
                                                   html.Div(html.Div(id='live-update-text'), className="explore-sb-row-h2",))
                                       , className="textHeader"),
                            ],
                            className="explore-sb-box header-h3",
                        ),  
                    ],
                    className="col-lg-6 col-md-6 col-sm-12",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3("Total Active"),
                                html.Div(dcc.Loading(id='loading-5',
                                                   children=
                                                   html.Div(html.Div(id='live-update-text3'), className="explore-sb-row-h2",))
                                       , className="textHeader"),
                            ],
                            className="explore-sb-box header-h3",
                        ),
                    ],
                    className="col-lg-6 col-md-6 col-sm-12",
                ),
            ],
            className="row clearIt bg-light explore-sb-row",
        ),
        # END Layout for Select an Organization of Interest
    ]
)

# START Layout for Select a Date Range
app.layout = html.Div(
    [
        row,
        # START Layout for Tabbed Content
        dbc.Row(
            [
                # dbc.Col(
                #     html.Div("Select a Date Range", className="explore-sb-row-h2",),
                #     width=12,
                # ),
                dcc.Tabs(
                    id="tabs-with-classes",
                    value="tab-1",
                    parent_className="custom-tabs",
                    className="custom-tabs-container",
                    children=[
                        dcc.Tab(
                            label="Datatable",
                            value="tab-1",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                        dcc.Tab(
                            label="Status",
                            value="tab-2",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ),
                        dcc.Tab(
                            label="Release by Date",
                            value="tab-3",
                            className="custom-tab",
                            selected_className="custom-tab--selected",
                        ), 
                    ]
                ),
                html.Div(id="tabs-content-classes"),
            ],
            className="row clearIt bg-light explore-sb-row",
        ),
    ]
)
# START Layout for Tabbed Content
# END Layout for Select a Date Range


value_counts = df.status.value_counts()


@app.callback(
    Output("tabs-content-classes", "children"), [Input("tabs-with-classes", "value")]
)
def render_content(tab):
    if tab == "tab-1":
        return html.Div(
            [
                html.H4("Science Data Catalog Results", className="align-left"),
                html.A(
                    "Download Data Table (CSV)", id = 'download-button',
                    download = 'data.csv',
                    href='',
                    target='_blank',
                    # className="align-right",
                ),
                dcc.Loading(id='loading-2',
                        children=[html.Div(
                dash_table.DataTable(
                    id='datatable',
                    data=df.to_dict('records'),
                    columns=[
                    {"name": ["Status"], "id": "status"},
                    {"name": ["Science Center"], "id": "datasource"},
                    {"name": ["Citations"], "id": "citations"},
                    {"name": ["DOI"], "id": "doi"},
                    ],
                    style_cell_conditional=[
                        {'if': {'column_id': 'status'},
                          'width': '8%',
                          'textAlign': 'left'},
                        {'if': {'column_id': 'citations'},
                          'width': '10%',
                          'textAlign': 'center'},
                        {'if': {'column_id': 'datasource'},
                          'width': '60%',
                          'textAlign': 'left'},
                    ],
                    style_header= {
                        'whiteSpace':'normal',
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    },
                    style_cell={
                        'overflow': 'hidden',
                        'maxWidth': '60px',
                        'height': 'auto'
                    },
                    style_table={
                        'maxHeight': '600px',
                        'overflowY': 'scroll'
                    },
                        style_data={
                        'whiteSpace': 'normal',
                        'height': 'auto',
                        'lineHeight': '15px'
                    },
                    sort_action="native",
                    sort_mode="multi",
                    )
                )], type = "default"),
                dcc.Link(
                    "Learn more about how these metrics are calculated.",
                    href="#",
                    className="learn-more-link align-left",
                ),
            ]
        )
    elif tab == "tab-2":
        return html.Div(
            [
                # html.P("Science Centers", className="center-date-range-text"),
                html.Div(dcc.Loading(id='loading-4',
                   children=
                   html.Div(html.Div(id='live-update-text2'), className="explore-sb-row-h2",
                            )
                   ), className="center-date-range-text"
                         ),
                html.H4("Status - Active/Inactive"),
                dcc.Graph(
                    id='pie-graph-1',
                    figure = go.Figure(data=[go.Pie(labels=value_counts.index, values=value_counts.values)])
                    ),

            ]
        )
    elif tab == "tab-3":
        return html.Div(
            [
                html.H4("Release by Date"),
                dcc.Graph(
                    id="example-graph-2",
                    figure = px.bar(dfg, x=dfg.index, y="Count")
                ),
            ]
        )

#function to filter data for table
def filter_data(sci_center, status, date_type, startdate, enddate):
    df1 = df.copy()
    startdate = dt.strptime(startdate, '%Y-%m-%d')
    startdate = startdate.replace(tzinfo=tz.gettz('UTC'))
    enddate = dt.strptime(enddate, '%Y-%m-%d')
    enddate = enddate.replace(tzinfo=tz.gettz('UTC'))
    #filter by date
    if date_type == 'beg_date':
        df1 = df1.reset_index().set_index('last_harvest_date')
        df1.index = pd.to_datetime(df1.index)
        df1 = df1.loc[startdate: enddate]  
    if date_type == 'end_date':
        df1 = df1.reset_index().set_index('last_harvest_date')
        df1.index = pd.to_datetime(df1.index)
        df1 = df1.loc[startdate: enddate] 
    if date_type == 'mdate':
        df1 = df1.reset_index().set_index('mdate')
        df1.index = pd.to_datetime(df1.index)
        df1 = df1.loc[startdate: enddate] 
    if date_type == 'last_harv':
        df1 = df1.reset_index().set_index('last_harvest_date')
        df1.index = pd.to_datetime(df1.index)
        df1 = df1.loc[startdate: enddate] 
    df1 = df1.set_index('file_identifier')
    #filter by science center and status
    if sci_center == 'All' and status == 'all_status':
        return df1
    elif sci_center == 'All' and status != 'all_status':
        df2 = df1.copy()
        if status == 'active':
            df2 = df2[df2['status']==1]
        if status == 'inactive':
            df2 = df2[df2['status']==0]
        return df2
    elif sci_center != 'All' and status == 'all_status':
        df2 = df1.copy()
        df2 = df2[df2['datasource']==sci_center]
        return df2
    elif sci_center != 'All' and status != 'all_status':
        df2 = df1.copy()
        df2 = df2[df2['datasource']==sci_center]
        if status == 'active':
            df2 = df2[df2['status']==1]
        if status == 'inactive':
            df2 = df2[df2['status']==0]
        return df2

#return table count
@app.callback(
    Output('live-update-text', 'children'),
    [Input('sci_center', 'value'),
      Input('status', 'value'),
      Input('date_type', 'value'), 
      Input('date-picker-range', 'start_date'),
      Input('date-picker-range', 'end_date')])
def set_display_livedata(sci_center, status, date_type,  startd, endd):
    #connect to database and obtain blood pressure where id=value
    df3 = filter_data(sci_center, status, date_type, startd, endd)
    if df3 is None:
        return 0
    else:
        return len(df3)

#return table count
@app.callback(
    Output('live-update-text3', 'children'),
    [Input('sci_center', 'value'),
      Input('status', 'value'),
      Input('date_type', 'value'), 
      Input('date-picker-range', 'start_date'),
      Input('date-picker-range', 'end_date')])
def set_display_livedata2(sci_center, status, date_type,  startd, endd):
    #connect to database and obtain blood pressure where id=value
    df3 = filter_data(sci_center, status, date_type, startd, endd)
    if df3 is None:
        return 0
    else:
        return len(df3[df3.status == 1])
    
#update table    
@app.callback(
    Output('datatable', 'data'),
    [Input('sci_center', 'value'),
      Input('status', 'value'),
      Input('date_type', 'value'), 
      Input('date-picker-range', 'start_date'),
      Input('date-picker-range', 'end_date')])
def table_selection(sci_center, status, date_type,  startd, endd):
    df4 = filter_data(sci_center, status, date_type, startd, endd)
    if df4 is not None:
        return df4.to_dict("records")
    else:
        return [{}]
def update_selected_row_indices(sci_center, status, date_type,  startd, endd):
    df4 = filter_data(sci_center, status, date_type, startd, endd)
    if df4 is not None:
        return df4.to_dict("records")
    else:
        return [{}]

#download table
@app.callback(Output('download-button', 'href'), 
              [Input('datatable', 'data')])
def update_download_link(data):
    df5 = pd.DataFrame(data)
    csv_string = df5.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(csv_string)
    return csv_string

#update pie chart
@app.callback(Output('pie-graph-1', 'figure'), 
    [Input('sci_center', 'value'),
      Input('status', 'value'),
      Input('date_type', 'value'), 
      Input('date-picker-range', 'start_date'),
      Input('date-picker-range', 'end_date')])
def pie_status(sci_center, status, date_type,  startd, endd):
    df6 = filter_data(sci_center, status, date_type, startd, endd)
    value_counts = df6.status.value_counts()
    trace1 = go.Pie(
                labels = value_counts.index,
                values= value_counts.values,)
    data = [trace1]
    layout = go.Layout()
    fig = go.Figure(data=data, layout=layout)
    return fig

#update graph by date
@app.callback(Output('example-graph-2', 'figure'), 
    [Input('sci_center', 'value'),
      Input('status', 'value'),
      Input('date_type', 'value'), 
      Input('date-picker-range', 'start_date'),
      Input('date-picker-range', 'end_date')])
def time_series(sci_center, status, date_type,  startd, endd):
    df7 = filter_data(sci_center, status, date_type, startd, endd)
    df7.mdate = pd.to_datetime(df7.mdate)
    dfg = df7.groupby('mdate').count()
    dfg = dfg.rename(columns={"datasource": "Count"})
    figure = px.bar(dfg, x=dfg.index, y="Count")
    return figure

# update science center text
@app.callback(
    Output('live-update-text2', 'children'),
    [Input('sci_center', 'value'),])
def new_text(value):
    return value

if __name__ == "__main__":
    app.run_server(debug=True)
