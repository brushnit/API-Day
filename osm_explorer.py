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
https://wiki.openstreetmap.org/wiki/Top-level_tag

TKinter:
https://pythonguides.com/python-tkinter-search-box/
https://tkdocs.com/tutorial/index.html

TKinterMapView:
https://github.com/HezekiahMD/TkinterMapView2

'''

### DEPENDENCIES ###
'''
!pip install osmnx
!pip install tkintermapview
'''


import tkinter as tk
from tkinter import messagebox
import osmnx as ox
import tkintermapview as tkmv
import geopandas as gpd

# Selection of Top-Level Tags: https://wiki.openstreetmap.org/wiki/Top-level_tag
options = {
    "Airport": "aeroway",
    "Amenity": "amenity", 
    "Barrier": "barrier", 
    "Building": "building",
    "Club": "club",
    "Craft": "craft", 
    "Education": "education",
    "Emergency": "emergency", 
    "Geological": "geological", 
    "Healthcare": "healthcare", 
    "Roads": "highway",
    "Military": "military",
    "Natural": "natural",
    "Railway": "railway",
    "Shop": "shop",
    "Tourism": "tourism",
    "Waterway": "waterway"
}
default_x, default_y = 38.6270, -90.1994
default_zoom = 10

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.pack(fill=tk.BOTH, expand=True)
        self.search_var = tk.StringVar()
        self.option_var = tk.StringVar(value="boundary")
        self.user_tag_var = tk.StringVar()
        self.poly_toggle_var = tk.BooleanVar(value=True)
        self.point_toggle_var = tk.BooleanVar(value=True)
        self.line_toggle_var = tk.BooleanVar(value=True)
        self.geocode = None
  
        self.setup_layout()


    def setup_layout(self):
        '''Create and arrange all widgets in window'''
        # top search bar
        self.top_frame = tk.Frame(self, height=50, bg="#EAEAEA", borderwidth=1, relief=tk.SOLID)
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        # side option bar
        self.sidebar_frame = tk.Frame(self, width=200, bg="#F5F5F5", borderwidth=1, relief=tk.SOLID)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        # map frame
        self.map_frame = tk.Frame(self, bg="lightgray")
        self.map_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # search/option buttons and entry boxes
        tk.Label(self.top_frame, text="Enter Place Name:", bg="#EAEAEA", font=("Arial", 10)).pack(side=tk.LEFT, padx=10, pady=10)
        search_entry = tk.Entry(self.top_frame, textvariable=self.search_var, width=50, font=("Arial", 10))
        search_entry.pack(side=tk.LEFT, padx=5, pady=10, ipady=4)
        search_button = tk.Button(self.top_frame, text="Search", command=self.search_osm, font=("Arial", 10, "bold"))
        search_button.pack(side=tk.LEFT, padx=10, pady=10)
        tk.Label(self.sidebar_frame, text="Features", bg="#F5F5F5", font=("Arial", 12, "bold")).pack(pady=10, padx=10, anchor="w")

        # New toggle switch for points
        self.point_toggle = tk.Checkbutton(
            self.top_frame,
            variable=self.point_toggle_var,
            onvalue=True,
            offvalue=False,
            text='Points',
            width=10,
        )
        self.point_toggle.pack(side=tk.RIGHT, padx=10, pady=10)
        
        self.line_toggle = tk.Checkbutton(
            self.top_frame,
            variable=self.line_toggle_var,
            onvalue=True,
            offvalue=False,
            text='Lines',
            width=10,
        )
        self.line_toggle.pack(side=tk.RIGHT, padx=10, pady=10)

        self.poly_toggle = tk.Checkbutton(
            self.top_frame,
            variable=self.poly_toggle_var,
            onvalue=True,
            offvalue=False,
            text='Polygons',
            width=10,
        )
        self.poly_toggle.pack(side=tk.RIGHT, padx=10, pady=10)


        # build radio buttons
        for text, value in options.items():
            tk.Radiobutton(
                self.sidebar_frame, text=text, variable=self.option_var,
                value=value, bg="#F5F5F5", font=("Arial", 10)
            ).pack(anchor="w", padx=20, pady=2)
        tk.Radiobutton(
            self.sidebar_frame, text="Custom Tag", variable=self.option_var,
            value="custom", bg="#F5F5F5", font=("Arial", 10), command=self.custom_radiobutton_callback
        ).pack(anchor="w", padx=20, pady=2)
        self.custom_entry = tk.Entry(self.sidebar_frame, textvariable=self.user_tag_var, font=("Arial", 10), state="disabled")
        self.custom_entry.pack(anchor="w", padx=40, pady=2, ipady=4)

        update_button = tk.Button(self.sidebar_frame, text="Update View", command=self.update_data, font=("Arial", 10, "bold"), bg="#DDDDDD")
        update_button.pack(pady=20, padx=10, fill=tk.X)

        # create map widget
        self.map_widget = tkmv.TkinterMapView(self.map_frame, corner_radius=0)
        self.map_widget.pack(fill=tk.BOTH, expand=True)
        self.map_widget.set_position(default_x, default_y) #default position
        self.map_widget.set_zoom(default_zoom)

    def custom_radiobutton_callback(self):
        # Enable or disable the custom entry field based on the selected radio button
        if self.option_var.get() == "custom":
            self.custom_entry.config(state="normal")
        else:
            self.custom_entry.config(state="disabled")

    def search_osm(self):
        # Fetches search results from OSM API
        search_input = self.search_var.get().strip()
        if not search_input:
            messagebox.showerror("Error", "Please enter a place name.")
            return
        try:
            self.parent.title(f"Searching for {search_input}...")
            geocode_gdf = ox.geocode_to_gdf(search_input)
            self.geocode = geocode_gdf
            self.update_data()
            self.parent.title(f"OpenStreetMap Search - {search_input}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not find data for '{search_input}'.\nDetail: {e}")
            self.parent.title("OpenStreetMap Search")
            

    def update_data(self):
        geocode_gdf = self.geocode
        if geocode_gdf.empty:
            self.search_osm()
        else:
            tag_key = self.option_var.get()
            if tag_key == 'custom':
                tag_key = self.user_tag_var.get().strip()
            
            if tag_key == 'boundary':
                self.draw_data(geocode_gdf)
            else: 
                tags = {tag_key: True}
                features_gdf = ox.features_from_polygon(geocode_gdf.dissolve().iloc[0].geometry, tags)
                self.draw_data(features_gdf)
            
    def draw_data(self, gdf): #add param for tags 
        # clear map
        self.map_widget.delete_all_polygon()  
        self.map_widget.delete_all_marker()
        self.map_widget.delete_all_path()
        self.layers.clear()  

        gdf = gdf[gdf.geometry.notna()].explode(index_parts=False)

        if gdf.empty:
            messagebox.showinfo("No Data", f"No features found.")
            return
        try:            
            self.draw_polygons(gdf[gdf.geometry.geom_type == 'Polygon'])
            self.draw_points(gdf[gdf.geometry.geom_type == 'Point'])
            self.draw_lines(gdf[gdf.geometry.geom_type == 'LineString'])
            self.map_widget.fit_bounding_box((gdf.total_bounds[3], gdf.total_bounds[0]), (gdf.total_bounds[1], gdf.total_bounds[2]))
        except Exception as e:
            messagebox.showerror("Plotting Error", f"An error occurred while plotting the data.\n\nDetail: {e}")

    def draw_polygons(self, poly_gdf):
        if not poly_gdf.empty and self.poly_toggle_var.get():
            for row in poly_gdf.iterrows():
                coords = [(y, x) for x, y in row.geometry.exterior.coords]
                self.map_widget.set_polygon(coords, outline_color="#2c3e50", border_width=2)


    def draw_points(self, point_gdf):
        if not point_gdf.empty and self.point_toggle_var.get():
            for row in point_gdf.iterrows():
                x, y = row.geometry.x , row.geometry.y
                self.map_widget.set_marker(y,x,command = 'marker_click')


    def draw_lines(self, line_gdf):
        if not line_gdf.empty and self.line_toggle_var.get():
            for row in line_gdf.iterrows():
                coords = [(y, x) for x, y in row.geometry.coords]
                self.map_widget.set_path(coords)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("OpenStreetMap Search")
    root.geometry("1200x800")
    app = MainApplication(root)
    root.mainloop()