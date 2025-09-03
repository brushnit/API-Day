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
'''


# need to optimize so that it doesn't need to make recurrent calls if place_name is the same
# add status (loading/working) icon


import tkinter as tk
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_data(geom, place_name, plot_frame):
    for widget in plot_frame.winfo_children():
        widget.destroy()
    fig, ax = plt.subplots(figsize=(6, 6))
    geom.plot(ax=ax)
    ax.set_xticks([]) # remove ticks & labels
    ax.set_yticks([]) 
    ax.set_xlabel('') 
    ax.set_ylabel('') 
    ax.set_title(place_name)
    fig.tight_layout()

    # EMBED PLOT IN WIDGET
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.cached_place = None
        self.cached_result = None #future: abstract to hold many layers?
        self.plot_area = None

        search_var = tk.StringVar()
        self.search_var = search_var
        input_frame = tk.Frame(self)
        option_frame = tk.Frame(input_frame)
        self.option_var = tk.StringVar(option_frame, "boundary")

        # OPTIONS
        options = {
            "Boundary" : "boundary",
            "Streets" : "highway",
            "Buildings" : "building",
        }

        # FUNCTION display text message
        def show_message(message):
            tk.Label(self.plot_area, text=f"Error: {message}", fg="red").pack(pady=20)

        # FUNCTION call API or previous API return
        def query_osm():
            place_name = self.search_var.get().strip()
            option = self.option_var.get()

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

                if option == 'boundary': #relies on 'option' being passed in tag syntax
                    geom = result
                else:
                    show_message(f'Searching for {option}...')
                    tags = {option: True}
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

        for (text, value) in options.items(): 
            tk.Radiobutton(option_frame, text = text, variable =self.option_var, value = value).pack(side="top", ipady = 5) 

        # SEARCH BOX
        search_frame = tk.Frame(input_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        search_label = tk.Label(search_frame, text="Enter place name:")
        search_label.pack(side=tk.LEFT, padx=(0, 5))
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=50)
        search_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        search_button = tk.Button(search_frame, text="Search", command=query_osm)
        search_button.pack(side=tk.LEFT)

        # OUTPUT
        self.plot_area = tk.Frame(self, relief=tk.SUNKEN, borderwidth=2)
        self.plot_area.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        result_label = tk.Label(self.plot_area, anchor="center")
        result_label.pack(expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("OpenStreetMap Search")
    root.geometry("1000x750")
    root.resizable(False, False)
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()