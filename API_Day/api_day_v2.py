### SOURCES ###
'''
OSMNX: 
https://github.com/gboeing/osmnx
https://osmnx.readthedocs.io/en/stable/user-reference.html
https://pygis.io/docs/d_access_osm.html

OSM:
https://wiki.openstreetmap.org/wiki/OSMPythonTools
https://racum.blog/articles/osm-python/0
https://wiki.openstreetmap.org/wiki/Map_features

TKinter:
https://github.com/HezekiahMD/TkinterMapView2
https://stackoverflow.com/questions/17466561/what-is-the-best-way-to-structure-a-tkinter-application
https://pythonguides.com/python-tkinter-search-box/
https://tkdocs.com/tutorial/index.html
https://medium.com/@roy-chng/make-python-tkinter-applications-look-modern-eb9d25a8e7bb
https://www.reddit.com/r/learnpython/comments/auq4ln/is_it_actually_possible_to_create_a_rather_good/
https://tkinter.com/how-to-add-maps-to-your-tkinter-app-python-tkinter-gui-tutorial-217/

Other APIs:
https://github.com/public-api-lists/public-api-lists
https://publicapis.io/district-of-columbia-open-data-api
https://www.stlouis-mo.gov/government/departments/information-technology/web-development/city-api/index.cfm
https://data-msdis.opendata.arcgis.com/ : uses ESRI ArcGIS API https://developers.arcgis.com/rest/
https://api.nasa.gov/
https://docs.sentinel-hub.com/api/latest/data/sentinel-2-l2a/
'''

### DEPENDENCIES ###
'''
!pip install osmnx
!pip install tkintermapview
'''

# add status (loading/working) icon (animated?)
# create map frame that scales correctly 

# CONSTANTS
tags = {
            "Boundary" : "boundary",
            "Streets" : "highway",
            "Buildings" : "building",
        }

import tkinter as tk
import osmnx as ox
import geopandas as gpd
import tkintermapview as tkmv

def plot_data(geom, map_widget):
    map_widget.delete_all_polygon()
    
    polygon_1 = map_widget.set_polygon(geom, command=polygon_click, )
    
# reformat to have a sidebar for option and layers, and top navbar for searching
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.cached_place = None
        self.cached_result = None #future: abstract to hold many layers?
        self.message_area = None

        search_var = tk.StringVar()
        self.search_var = search_var
        input_frame = tk.Frame(self)
        option_frame = tk.Frame(input_frame)
        self.option_var = tk.StringVar(option_frame, "boundary")

        # OPTIONS


        # make this a pop up
        # FUNCTION display text message
        def show_message(message):
            tk.Label(self.message_area, text=f"Error: {message}", fg="red").pack(pady=20)

        # FUNCTION call API or previous API return
        def query_osm():
            place_name = self.search_var.get().strip()
            tag = self.option_var.get()

            if not place_name:
                show_message("Please enter a place name.")
                return

            try:
                if place_name == self.cached_place and self.cached_result is not None:
                    result = self.cached_result
                else:
                    show_message('Searching...')
                    result = ox.geocode_to_gdf(place_name)
                    self.cached_place = place_name
                    self.cached_result = result

                if tag == 'boundary': #relies on 'tag' being passed in tag syntax
                    geom = result
                else:
                    show_message(f'Searching for {tag}...')
                    tags = {tag: True}
                    geom = ox.features_from_polygon(result.iloc[0]['geometry'], tags)
                
                plot_data(geom, place_name, self.plot_area)
            except Exception as e:
                show_message(f'Error: Could not find data for \'{place_name}\'\nDetail: {e}')
                self.cached_place = None
                self.cached_result = None
        

        input_frame.pack(fill=tk.X, pady=(0,10))
        option_frame.pack(fill=tk.X, pady=(0,10))
        option_label = tk.Label(option_frame, text="Options")
        option_label.pack(side=tk.LEFT, padx=(0, 5))

        for (text, value) in tags.items(): 
            tk.Radiobutton(option_frame, text = text, variable =self.option_var, value = value).pack(side="top", ipady = 5) 

        # TEXT SEARCH BOX
        search_frame = tk.Frame(input_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        search_label = tk.Label(search_frame, text="Enter place name:")
        search_label.pack(side=tk.LEFT, padx=(0, 5))
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=50)
        search_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        search_button = tk.Button(search_frame, text="Search", command=query_osm)
        search_button.pack(side=tk.LEFT)

        

if __name__ == "__main__":
    root = tk.Tk()
    root.title("OpenStreetMap Search")
    root.geometry("1000x750")
    root.resizable(False, False)

    map_widget = tkmv.TkinterMapView(root, width=800, height=600, corner_radius=0) # is here the best place to initialize the widget? 

    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()