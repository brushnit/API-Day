import tkinter as tk
import osmnx as ox
import geopandas as gpd




def query_osm(place_name, ):
    area = ox.geocode_to_gdf(place_name)

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        
        self.title("OpenStreetMap Search")
        self.geometry("1920x1080")
        fields = 'Place Name'

        entries = []
        for field in fields:
            row = tk.Frame(root)
            lab = tk.Label(row, width=20, text=field, anchor='w')
            ent = tk.Entry(row)
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries.append((field, ent))

        ent = tk.makeform(self, fields)
        runButton = tk.Button(self, text='Search', command=(query_osm(place_name)))
        runButton.pack(pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()