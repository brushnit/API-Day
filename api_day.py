### SOURCES ###
'''
https://pygis.io/docs/d_access_osm.html
https://github.com/gboeing/osmnx
https://osmnx.readthedocs.io/en/stable/getting-started.html
https://wiki.openstreetmap.org/wiki/OSMPythonTools
https://racum.blog/articles/osm-python/
https://peps.python.org/pep-0008/
https://github.com/HezekiahMD/TkinterMapView2
'''

### DEPENDENCIES ###
'''
!pip install osmnx
'''


import tkinter as tk
import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def query_osm(place_name, plot_frame):
    for widget in plot_frame.winfo_children():
        widget.destroy()
    try:
        # Call API
        area = ox.geocode_to_gdf(place_name)   

        # Create a matplotlib figure and axes
        fig, ax = plt.subplots(figsize=(6, 6))
        area.plot(ax=ax)
        ax.set_xticks([]) # Remove ticks and labels
        ax.set_yticks([]) 
        ax.set_xlabel('') 
        ax.set_ylabel('') 
        ax.set_title(place_name)
        fig.tight_layout()

        # Embed the plot in the Tkinter window
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
         
        # SEARCH BOX
        search_frame = tk.Frame(self)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        search_label = tk.Label(search_frame, text="Enter place name:")
        search_label.pack(side=tk.LEFT, padx=(0, 5))
        search_var = tk.StringVar()
        search_entry = tk.Entry(search_frame, textvariable=search_var, width=50)
        search_entry.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        search_button = tk.Button(search_frame, text="Search", command=lambda: query_osm(search_var.get(), plot_area))
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