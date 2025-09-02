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


import tkinter as tk
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# need to optimize so that it doesn't need to make recurrent calls if place_name is the same
def query_osm(place_name, plot_frame, option):
    for widget in plot_frame.winfo_children():
        widget.destroy()
    try:
        result = gpd.GeoDataFrame()
        # CALL API
        result = ox.geocode_to_gdf(place_name)   
        
        if option == 'Streets':
            tags = {'highway': True}   
            geom = ox.features_from_polygon(result.iloc[0]['geometry'], tags)  
        elif option == 'Buildings':
            tags = {'building': True}   
            geom = ox.features_from_polygon(result.iloc[0]['geometry'], tags)
        else:
            geom = result

        # CREATE PLOT
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
    except Exception as e:
        tk.Label(plot_frame, text=f"Error: Could not find data for '{place_name}'.\nDetails: {e}", fg="red").pack(pady=20)


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        input_frame = tk.Frame(self)
        input_frame.pack(fill=tk.X, pady=(0,10))

        # OPTIONS
        options = {
            "Boundary" : "Boundary",
            "Streets" : "Streets",
            "Buildings" : "Buildings",
        }
        option_frame = tk.Frame(input_frame)
        option_frame.pack(fill=tk.X, pady=(0,10))
        option_label = tk.Label(option_frame, text="Options")
        option_label.pack(side=tk.LEFT, padx=(0, 5))
        option_var = tk.StringVar(option_frame, "Boundary")
        for (text, value) in options.items(): 
            tk.Radiobutton(option_frame, text = text, variable = option_var, value = value).pack(side="top", ipady = 5) 

        # SEARCH BOX
        search_frame = tk.Frame(input_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        search_label = tk.Label(search_frame, text="Enter place name:")
        search_label.pack(side=tk.LEFT, padx=(0, 5))
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, width=50)
        search_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        search_button = tk.Button(search_frame, text="Search", command=lambda: query_osm(search_var.get(), plot_area, option_var.get()))
        search_button.pack(side=tk.LEFT)

        # OUTPUT
        plot_area = tk.Frame(self, relief=tk.SUNKEN, borderwidth=2)
        plot_area.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        result_label = tk.Label(plot_area, anchor="center")
        result_label.pack(expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("OpenStreetMap Search")
    root.geometry("1000x750")
    root.resizable(False, False)
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()