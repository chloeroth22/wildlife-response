## Wildlife Response to Wildfire
### Study Background
The Rocky Mountain Research Center and the USDA are currently recording data on a study to determine the response to fire across species. They are studying three 2020 megafires in Colorado that burned over 230,000 hectares,
where they have sampled 134 burned and unburned locations over the last 1.5 years, with varying burn severity. 

<img 
  src="img/fire_locations.png" 
  alt="Fire Locations" 
  style="max-width:100%; height:auto; display:block; margin-left:auto; margin-right:auto;">

  
They performed acoustic monitoring of birds and bats for 3 weeks at each location. Acoustic recording units were place on 2 meter PVC pipes
and recorded birds for an hour before sunset and an hour after sunrise, and bats were recorded continuously from sunset to sunrise. Trail cameras were placed at each site to record non flying mammals. They aim to study the 
changes in occupancy and biodiversity with variations in fire variables (fire severity and pyrodiversity), topology/elevation, pre-fire vegetation, and drought mortality. Learning the patterns of post-fire occupancy can 
help inform how to best manage forests after wildfires to support wildlife.

Similar work has been done studying the relationship between pyrodiversity and bat occupancy, including the papers referenced below. It has been found that bats are impacted by fire severity, fire frequency, time since last burn, 
burn extent, season of burn, and pyrodiversity. There has been some evidence showing that species richness increases in pyrodiverse areas - potentially due to a greater accessibility of foraging habitats and increased 
habitat heterogeneity. Generally, bats show positive or neutral response to prescribed fire, and a negative, though sometimes short-lived, response to wildfire.

[The effects of wildfire severity and pyrodiversity on bat occupancy and diversity in fire-suppressed forests](https://www.nature.com/articles/s41598-019-52875-2)

[Bats and fire: a global review](https://research.fs.usda.gov/treesearch/63537)

### Project

In order to narrow down this project into something more manageable for my time frame I decided to pursue the question of: how do elevation and pyrodiversity influence bat presence and activity in areas 
affected by the 2020 East Troublesome fire? My goal was to be able to determine some summary statistics and rudimentary analysis on these relationships. 

The data provided by the RMRC included 27 sites within or just outside the boundary of the East Troublesome fire that had recorded bat data. 

<img 
  src="img/et_boundary.png" 
  alt="East Troublesome Boundary" 
  style="max-width:100%; height:auto; display:block; margin-left:auto; margin-right:auto;">

### Data Sources
My data sources included a site data csv that contained site information like longitude, latitude, and types of recordings pulled and a bat recording csv file containing site number, data, 
number of high and low frequency bats, and bat species recorded. Both of these csvs had a temporal range of May to August 2024 and were provided by the RMRC. Additionally, I used a shapefile from the MTBS burned
area boundary dataset, which is a shapefile containing the boundary of the East Troublesome fire. I also used SRTM elevation data which is a DEM with 30 arc sec resolution. 

### Methods
difference between low frequency and high frequency bats - which are high and low frequency?
occupancy modeling?

What your methods are. Note that your code should be expressive to provide a good overview of your workflow -- you do not need to get into the nitty gritty details of the python steps that you applied.
  
### Results
What you discovered about your topic  / question. General 
In the future - elevation, georeference longitude latitude, pyrodiversity
make presentation

<img 
  src="img/activityseverity.png" 
  alt="Bat Activity Versus Fire Severity" 
  style="max-width:100%; height:auto; display:block; margin-left:auto; margin-right:auto;">
  
  <img 
  src="img/hi_pass_predicted.png" 
  alt="High Frequency Predictions" 
  style="max-width:100%; height:auto; display:block; margin-left:auto; margin-right:auto;">
  
  <img 
  src="img/hi_pass_table.png" 
  alt="High Frequency Table" 
  style="max-width:100%; height:auto; display:block; margin-left:auto; margin-right:auto;">
  
  <img 
  src="img/lo_pass_predicted.png" 
  alt="Low Frequency Predictions" 
  style="max-width:100%; height:auto; display:block; margin-left:auto; margin-right:auto;">
  
  <img 
  src="img/lo_pass_table.png" 
  alt="Low Frequency Table" 
  style="max-width:100%; height:auto; display:block; margin-left:auto; margin-right:auto;">

