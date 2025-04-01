import pandas as pd
import numpy as np
import pandas as pd
import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px

data = pd.DataFrame({
    "Country":["Argentina", "Brazil", "Croatia", "Czechoslovakia", "England", "France"," Germany", "Hungary", "Italy", "Netherlands", "Spain", "Sweden", "Uruguay"],
    "Winners":[3, 5, 0, 0, 1, 2, 4, 0, 4, 0, 1, 0, 2],
    "Runners-Up":[3, 2, 1, 2, 0, 2, 4, 2, 2, 3, 0, 1, 0],
    "Total finals":[6, 7, 1, 2, 1, 4, 8, 2, 6, 3, 1, 1, 2],
    "Years Won":[[1978,1986,2022],[1958,1962,1970,1994,2002],[],[],[1966],[1998,2018],[1954,1974,1990,2014],[],[1934,1938,1982,2026],[],[2010],[],[1930,1950]],
    "Years runners-up":[[1930,1990,2014],[1950,1998],[2018],[1934,1962],[],[2006,2022],[1966,1982,1986,2002],[1938,1954],[1970,1994],[1974,1978,2010],[],[1958],[]],
    "Country Code":["ARG", "BRA", "HRV", "CZE", "GBR", "FRA", "DEU", "HUN", "ITA", "NLD", "ESP", "SWF", "URY"]        
})

df= pd.DataFrame(data)

fig = px.choropleth(df, locations="Country Code",
                        color="Winners",
                        hover_name="Country",
                        color_continuous_scale="Viridis",
                        labels={"Winners": "Number of Wins"})


def search_by_year(year):
    wonByYear = df[df['Years Won'].apply(lambda x: year in x)]
    runnerUpByYear=df[df['Years runners-up'].apply(lambda x: year in x)]
    
    return wonByYear, runnerUpByYear

def search_by_country(country):
    country_df=df[df["Country"] == country]
    country_df=country_df.iloc[0]
    
    return country_df

app=dash.Dash(__name__)
server=app.server

countries=data["Country"]
years=[1930,1934,1938,1950,1954,1958,1962,1966,1970,1974,1978,1982,1986,1990,1994,1998,2002,2006,2010,2014,2018,2022]
dropdownOption1 = []
dropdownOption2 = []
for country in countries:
    dropdownOption1.append({'label':country, 'value':country})
    
for year in years:
    dropdownOption2.append({'label':year, 'value':year})

app.layout = html.Div([
    html.H1("FIFA World Cup Finals", style={"text-align": "center"}),
    html.H2("All Countries Who Won"),
    dcc.Graph(id="graph_and_chart", figure=fig),
    
    html.Div([
        html.H3("choose country"),
        dcc.Dropdown(
            id="Select Country",
            options=dropdownOption1,
            value="Argentina",
            style={"width":"40%", "text-align":"center"}
        ),
        html.Div(id="Country output")   
    ]),
    
    html.Div([
        html.H3("choose year"),
        dcc.Dropdown(
            id="Select Year",
            options=dropdownOption2,
            value=1930,
            style={"width":"30%", "text-align":"center"}
        ),
        html.Div(id="Year output")
    ]),    
])

@app.callback(
    Output("Country output", "children"),
    Input("Select Country", "value"),
)

def Update_Country(value):
    country=value
    country_df=search_by_country(country)
    if country_df is not None:
        return f"Country: {value}        Number of Wins: {country_df['Winners']}"
    
    # If no data is found for the country (although it should be in the dataset), handle it gracefully
    return "Country not found."


@app.callback(
    Output("Year output", "children"),
    Input("Select Year", "value"),
)

def Update_Year(value):
    year = value
    wonCountry, runUpCountry = search_by_year(year)
    
    return f"Year: {year}        Country Won: {wonCountry['Country']}        Country Runner-up: {runUpCountry['Country']}"

if __name__ == '__main__':
    app.run()
