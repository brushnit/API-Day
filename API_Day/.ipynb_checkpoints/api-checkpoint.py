import osmnx as ox
import geopandas as gpd

place_name = "Saint Louis, MO, USA"
area = ox.geocode_to_gdf(place_name)

area
type(area)
gpd.geodataframe.GeoDataFrame

area.plot()
