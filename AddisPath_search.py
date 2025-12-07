import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import heapq
import math
import json
import os
import requests
from PIL import Image, ImageTk
from ttkthemes import ThemedTk
from collections import defaultdict

class PathFinder:
    def __init__(self, master):
        self.master = master
        master.title("City Path Finder")
        master.geometry("1200x800")
        
        # City data
        self.cities = {
            "Addis Ababa": {
                "locations": [
                    "Bole Airport", "Meskel Square", "Piassa", "Merkato", 
                    "Kazanchis", "Mexico Square", "Stadium", "Megenagna",
                    "CMC", "Ayat", "Gerji", "Lideta", "Arat Kilo", "Sidist Kilo",
                    "Shola", "Lamberet", "Kality", "Jemo", "Lebu", "Sarbet"
                ],
                # Distance in km (approximate)
                "distances": {
                    ("Bole Airport", "Meskel Square"): 5.2,
                    ("Bole Airport", "Kazanchis"): 4.7,
                    ("Bole Airport", "Gerji"): 3.1,
                    ("Bole Airport", "Megenagna"): 4.8,
                    ("Meskel Square", "Piassa"): 3.6,
                    ("Meskel Square", "Kazanchis"): 1.5,
                    ("Meskel Square", "Stadium"): 2.3,
                    ("Meskel Square", "Mexico Square"): 2.7,
                    ("Meskel Square", "Lideta"): 2.9,
                    ("Piassa", "Merkato"): 1.8,
                    ("Piassa", "Arat Kilo"): 2.2,
                    ("Merkato", "Mexico Square"): 2.4,
                    ("Merkato", "Lideta"): 2.1,
                    ("Kazanchis", "Stadium"): 1.9,
                    ("Kazanchis", "Megenagna"): 3.9,
                    ("Mexico Square", "Lideta"): 1.5,
                    ("Mexico Square", "Sarbet"): 2.8,
                    ("Stadium", "Megenagna"): 4.5,
                    ("Stadium", "Arat Kilo"): 3.2,
                    ("Megenagna", "CMC"): 3.7,
                    ("Megenagna", "Gerji"): 2.9,
                    ("Megenagna", "Shola"): 2.5,
                    ("CMC", "Ayat"): 4.3,
                    ("Ayat", "Lamberet"): 3.8,
                    ("Gerji", "Shola"): 4.1,
                    ("Lideta", "Arat Kilo"): 2.8,
                    ("Lideta", "Sarbet"): 3.3,
                    ("Arat Kilo", "Sidist Kilo"): 1.2,
                    ("Shola", "Lamberet"): 2.7,
                    ("Lamberet", "Kality"): 7.9,
                    ("Kality", "Jemo"): 4.5,
                    ("Jemo", "Lebu"): 3.2,
                    ("Sarbet", "Lebu"): 5.8
                },
                # Elevation in meters (approximate)
                "elevations": {
                    "Bole Airport": 2324,
                    "Meskel Square": 2355,
                    "Piassa": 2410,
                    "Merkato": 2380,
                    "Kazanchis": 2370,
                    "Mexico Square": 2390,
                    "Stadium": 2400,
                    "Megenagna": 2450,
                    "CMC": 2480,
                    "Ayat": 2520,
                    "Gerji": 2360,
                    "Lideta": 2395,
                    "Arat Kilo": 2440,
                    "Sidist Kilo": 2460,
                    "Shola": 2420,
                    "Lamberet": 2390,
                    "Kality": 2310,
                    "Jemo": 2300,
                    "Lebu": 2280,
                    "Sarbet": 2350
                },
                # Approximate coordinates (latitude, longitude) for visualization
                "coordinates": {
                    "Bole Airport": (8.9778, 38.7989),
                    "Meskel Square": (9.0105, 38.7611),
                    "Piassa": (9.0352, 38.7523),
                    "Merkato": (9.0384, 38.7368),
                    "Kazanchis": (9.0199, 38.7776),
                    "Mexico Square": (9.0083, 38.7408),
                    "Stadium": (9.0225, 38.7513),
                    "Megenagna": (9.0213, 38.8001),
                    "CMC": (9.0305, 38.8231),
                    "Ayat": (9.0388, 38.8508),
                    "Gerji": (9.0025, 38.8176),
                    "Lideta": (9.0054, 38.7295),
                    "Arat Kilo": (9.0397, 38.7635),
                    "Sidist Kilo": (9.0448, 38.7606),
                    "Shola": (9.0283, 38.8201),
                    "Lamberet": (9.0350, 38.8302),
                    "Kality": (8.9491, 38.7914),
                    "Jemo": (8.9346, 38.7632),
                    "Lebu": (8.9612, 38.7214),
                    "Sarbet": (8.9927, 38.7251)
                },
                # Traffic intensity (1-10 scale, 10 being heaviest)
                "traffic": {
                    ("Bole Airport", "Meskel Square"): 8,
                    ("Bole Airport", "Kazanchis"): 7,
                    ("Bole Airport", "Gerji"): 6,
                    ("Bole Airport", "Megenagna"): 7,
                    ("Meskel Square", "Piassa"): 9,
                    ("Meskel Square", "Kazanchis"): 8,
                    ("Meskel Square", "Stadium"): 7,
                    ("Meskel Square", "Mexico Square"): 9,
                    ("Meskel Square", "Lideta"): 8,
                    ("Piassa", "Merkato"): 10,
                    ("Piassa", "Arat Kilo"): 7,
                    ("Merkato", "Mexico Square"): 9,
                    ("Merkato", "Lideta"): 8,
                    ("Kazanchis", "Stadium"): 6,
                    ("Kazanchis", "Megenagna"): 7,
                    ("Mexico Square", "Lideta"): 8,
                    ("Mexico Square", "Sarbet"): 6,
                    ("Stadium", "Megenagna"): 5,
                    ("Stadium", "Arat Kilo"): 6,
                    ("Megenagna", "CMC"): 7,
                    ("Megenagna", "Gerji"): 7,
                    ("Megenagna", "Shola"): 6,
                    ("CMC", "Ayat"): 5,
                    ("Ayat", "Lamberet"): 4,
                    ("Gerji", "Shola"): 5,
                    ("Lideta", "Arat Kilo"): 7,
                    ("Lideta", "Sarbet"): 6,
                    ("Arat Kilo", "Sidist Kilo"): 5,
                    ("Shola", "Lamberet"): 4,
                    ("Lamberet", "Kality"): 5,
                    ("Kality", "Jemo"): 3,
                    ("Jemo", "Lebu"): 2,
                    ("Sarbet", "Lebu"): 4
                }
            }
        }
        
        self.current_city = "Addis Ababa"
        self.graph = self.build_graph(self.current_city)
        
        # Store multiple paths if found
        self.multiple_paths = []
        self.current_path_index = 0
        
        # UI setup
        self.setup_ui()
        
        # Initialize constraints
        self.time_cost_constraints = True
    def build_graph(self, city_name):
        """Build a networkx graph from the city data"""
        G = nx.Graph()
        city_data = self.cities[city_name]
        
        # Add nodes with attributes
        for loc in city_data["locations"]:
            G.add_node(loc, 
                       elevation=city_data["elevations"][loc],
                       pos=city_data["coordinates"][loc])
        
        # Add edges with attributes
        for (u, v), dist in city_data["distances"].items():
            traffic = city_data["traffic"].get((u, v), 5)
            
            # Add the edge in both directions
            G.add_edge(u, v, 
                      distance=dist,
                      traffic=traffic,
                      travel_time=dist * (1 + (traffic / 10)))  # Simple travel time model
            
            # Also add the reverse edge with the same attributes
            if (v, u) not in city_data["distances"]:
                G.add_edge(v, u, 
                          distance=dist,
                          traffic=traffic,
                          travel_time=dist * (1 + (traffic / 10)))
        
        return G
    
    def setup_ui(self):
        """Set up the main UI components"""
        # Main frame
        main_frame = ttk.Frame(self.master)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for inputs
        left_panel = ttk.Frame(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=10, pady=10)
        
        # City selection
        ttk.Label(left_panel, text="Select City:").pack(pady=(0, 5), anchor=tk.W)
        self.city_var = tk.StringVar(value=self.current_city)
        city_dropdown = ttk.Combobox(left_panel, textvariable=self.city_var, 
                                   values=list(self.cities.keys()), state="readonly")
        city_dropdown.pack(fill=tk.X, pady=(0, 10))
        city_dropdown.bind("<<ComboboxSelected>>", self.on_city_change)
        
        # Source and destination
        ttk.Label(left_panel, text="Starting Point:").pack(pady=(0, 5), anchor=tk.W)
        self.source_var = tk.StringVar()
        self.source_dropdown = ttk.Combobox(left_panel, textvariable=self.source_var, 
                                          values=self.cities[self.current_city]["locations"], 
                                          state="readonly")
        self.source_dropdown.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(left_panel, text="Destination:").pack(pady=(0, 5), anchor=tk.W)
        self.dest_var = tk.StringVar()
        self.dest_dropdown = ttk.Combobox(left_panel, textvariable=self.dest_var, 
                                        values=self.cities[self.current_city]["locations"], 
                                        state="readonly")
        self.dest_dropdown.pack(fill=tk.X, pady=(0, 10))
        
        # Algorithm selection
        ttk.Label(left_panel, text="Algorithm:").pack(pady=(0, 5), anchor=tk.W)
        self.algorithm_var = tk.StringVar(value="A*")
        algorithms = ttk.Frame(left_panel)
        algorithms.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Radiobutton(algorithms, text="Hill Climbing", variable=self.algorithm_var, value="Hill Climbing").pack(anchor=tk.W)
        ttk.Radiobutton(algorithms, text="Greedy", variable=self.algorithm_var, value="Greedy").pack(anchor=tk.W)
        ttk.Radiobutton(algorithms, text="A*", variable=self.algorithm_var, value="A*").pack(anchor=tk.W)
        
        # Constraint options
        ttk.Label(left_panel, text="Constraints:").pack(pady=(0, 5), anchor=tk.W)
        constraints = ttk.Frame(left_panel)
        constraints.pack(fill=tk.X, pady=(0, 10))
        
        # Block Road (Optional)
        ttk.Label(left_panel, text="Block Road (Optional):").pack(pady=(0, 5), anchor=tk.W)
        block_frame = ttk.Frame(left_panel)
        block_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(block_frame, text="From:").pack(anchor=tk.W)
        self.block_from_var = tk.StringVar()
        self.block_from_dropdown = ttk.Combobox(block_frame, textvariable=self.block_from_var, 
                                              values=self.cities[self.current_city]["locations"], 
                                              state="readonly")
        self.block_from_dropdown.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(block_frame, text="To:").pack(anchor=tk.W)
        self.block_to_var = tk.StringVar()
        self.block_to_dropdown = ttk.Combobox(block_frame, textvariable=self.block_to_var, 
                                            values=self.cities[self.current_city]["locations"], 
                                            state="readonly")
        self.block_to_dropdown.pack(fill=tk.X, pady=(0, 5))
        
        self.time_cost_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(constraints, text="Time/Cost Optimization", variable=self.time_cost_var).pack(anchor=tk.W)
        
        # Additional option to handle unknown states
        self.handle_unknown_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(constraints, text="Handle Unknown Locations", variable=self.handle_unknown_var).pack(anchor=tk.W)
        
        # Find path button
        find_btn = ttk.Button(left_panel, text="Find Path", command=self.find_path)
        find_btn.pack(fill=tk.X, pady=(10, 0))
        
        # Reset button
        reset_btn = ttk.Button(left_panel, text="Reset", command=self.reset)
        reset_btn.pack(fill=tk.X, pady=(10, 0))
        
        # Navigation buttons for multiple paths
        path_nav_frame = ttk.Frame(left_panel)
        path_nav_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.prev_path_btn = ttk.Button(path_nav_frame, text="Previous Path", command=self.show_previous_path)
        self.prev_path_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.prev_path_btn.configure(state="disabled")
        
        self.next_path_btn = ttk.Button(path_nav_frame, text="Next Path", command=self.show_next_path)
        self.next_path_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self.next_path_btn.configure(state="disabled")
        
        # Right panel for results and visualization
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Map/Graph visualization area
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, master=right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Results area
        ttk.Label(right_panel, text="Path Details:").pack(pady=(10, 5), anchor=tk.W)
        self.result_text = scrolledtext.ScrolledText(right_panel, height=8)
        self.result_text.pack(fill=tk.X, expand=False)
        
        # Path counter label
        self.path_counter = ttk.Label(right_panel, text="No paths found")
        self.path_counter.pack(pady=(5, 0), anchor=tk.W)
        
        # Draw initial map
        self.draw_map()
    
    def on_city_change(self, event=None):
        """Handle city selection change"""
        self.current_city = self.city_var.get()
        self.graph = self.build_graph(self.current_city)
        
        # Update dropdowns with new city locations
        locations = self.cities[self.current_city]["locations"]
        self.source_dropdown["values"] = locations
        self.dest_dropdown["values"] = locations
        
        # Clear existing selections
        self.source_var.set("")
        self.dest_var.set("")
        
        # Redraw map
        self.draw_map()
    
    def draw_map(self, path=None):
        """Draw the city map with optional path highlighted"""
        self.ax.clear()
        
        # Get node positions
        pos = nx.get_node_attributes(self.graph, 'pos')
        
        # Draw nodes and edges
        nx.draw_networkx_nodes(self.graph, pos, node_size=100, 
                             node_color='skyblue', ax=self.ax)
        
        nx.draw_networkx_edges(self.graph, pos, width=1.0, 
                             edge_color='gray', ax=self.ax)
        
        # Draw highlighted path if available
        if path and len(path) > 1:
            path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
            nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges, 
                                 width=3.0, edge_color='red', ax=self.ax)
            nx.draw_networkx_nodes(self.graph, pos, nodelist=path, 
                                 node_size=150, node_color='lightgreen', ax=self.ax)
            
            # Highlight start and end
            nx.draw_networkx_nodes(self.graph, pos, nodelist=[path[0]], 
                                 node_size=200, node_color='green', ax=self.ax)
            nx.draw_networkx_nodes(self.graph, pos, nodelist=[path[-1]], 
                                 node_size=200, node_color='red', ax=self.ax)
        
        # Draw labels
        nx.draw_networkx_labels(self.graph, pos, font_size=8, font_color='black', ax=self.ax)
        
        # Set plot title and layout
        self.ax.set_title(f"Map of {self.current_city}")
        self.ax.set_axis_off()
        
        # Update canvas
        self.canvas.draw()
    def find_path(self):
        """Find and display the path based on selected algorithm and constraints"""
        # Get inputs
        source = self.source_var.get()
        dest = self.dest_var.get()
        algorithm = self.algorithm_var.get()
        handle_unknown = self.handle_unknown_var.get()
        
        # Reset multiple paths
        self.multiple_paths = []
        self.current_path_index = 0
        self.prev_path_btn.configure(state="disabled")
        self.next_path_btn.configure(state="disabled")
        self.path_counter.config(text="No paths found")
        
        # Update constraints
        self.block_from = self.block_from_var.get()
        self.block_to = self.block_to_var.get()
        self.blocked_edge = None
        
        if self.block_from and self.block_to:
            if self.block_from != self.block_to:
                self.blocked_edge = (self.block_from, self.block_to)
            else:
                messagebox.showwarning("Warning", "Blocked road start and end points cannot be the same. Ignoring block.")
        
        self.time_cost_constraints = self.time_cost_var.get()
        
        # Handle missing inputs - Addressing unknown state requirement
        if not source or not dest:
            if handle_unknown:
                # Try to suggest a valid location
                if not source and not dest:
                    messagebox.showinfo("Unknown Locations", 
                                        "Both starting point and destination are unknown.\n"
                                        "Please select at least one location.")
                    return
                elif not source:
                    # Suggest closest location to destination
                    suggested_source = self.suggest_location(dest)
                    if suggested_source:
                        msg = f"Starting point is unknown. Would you like to start from {suggested_source}?"
                        if messagebox.askyesno("Suggestion", msg):
                            source = suggested_source
                            self.source_var.set(source)
                        else:
                            return
                    else:
                        messagebox.showerror("Error", "Cannot suggest a starting point.")
                        return
                elif not dest:
                    # Suggest destination based on starting point
                    suggested_dest = self.suggest_location(source)
                    if suggested_dest:
                        msg = f"Destination is unknown. Would you like to go to {suggested_dest}?"
                        if messagebox.askyesno("Suggestion", msg):
                            dest = suggested_dest
                            self.dest_var.set(dest)
                        else:
                            return
                    else:
                        messagebox.showerror("Error", "Cannot suggest a destination.")
                        return
            else:
                messagebox.showerror("Error", "Please select both starting point and destination.")
                return
        
        # Check if source and dest are same
        if source == dest:
            messagebox.showinfo("Info", "Starting point and destination are the same.")
            path = [source]
            self.multiple_paths = [[path, 0, 0]]  # [path, distance, time]
            self.show_results(path, 0, 0, algorithm)
            self.draw_map(path)
            self.path_counter.config(text="Path 1 of 1")
            return
            
        # Check if source and dest are in the graph
        if source not in self.graph.nodes or dest not in self.graph.nodes:
            if handle_unknown:
                if source not in self.graph.nodes:
                    suggested_src = self.find_nearest_known_location(source)
                    msg = f"'{source}' is not a known location. Would you like to use '{suggested_src}' instead?"
                    if messagebox.askyesno("Unknown Location", msg):
                        source = suggested_src
                        self.source_var.set(source)
                    else:
                        return
                
                if dest not in self.graph.nodes:
                    suggested_dst = self.find_nearest_known_location(dest)
                    msg = f"'{dest}' is not a known location. Would you like to use '{suggested_dst}' instead?"
                    if messagebox.askyesno("Unknown Location", msg):
                        dest = suggested_dst
                        self.dest_var.set(dest)
                    else:
                        return
            else:
                messagebox.showerror("Error", "Selected locations are not in the map.")
                return
        
        # Find path using the selected algorithm
        try:
            if algorithm == "Hill Climbing":
                self.multiple_paths = self.hill_climbing_search_all_paths(source, dest, blocked_edge=self.blocked_edge)
            elif algorithm == "Greedy":
                self.multiple_paths = self.greedy_search_all_paths(source, dest, blocked_edge=self.blocked_edge)
            else:  # A*
                self.multiple_paths = self.a_star_search_all_paths(source, dest, blocked_edge=self.blocked_edge)
                
            if not self.multiple_paths:
                messagebox.showinfo("No Path", "Could not find a path between the selected locations.")
                self.path_counter.config(text="No paths found")
                return
                
            # Display first path
            self.current_path_index = 0
            path, distance, time = self.multiple_paths[0]
            
            # Update navigation buttons
            if len(self.multiple_paths) > 1:
                self.next_path_btn.configure(state="normal")
                
            # Display results
            self.show_results(path, distance, time, algorithm)
            self.draw_map(path)
            
            # Update path counter
            self.path_counter.config(text=f"Path 1 of {len(self.multiple_paths)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def suggest_location(self, reference_point=None):
        """Suggest a location based on reference point or popularity"""
        if reference_point and reference_point in self.graph.nodes:
            # Get neighbors of reference point
            neighbors = list(self.graph.neighbors(reference_point))
            if neighbors:
                # Return a random neighbor
                return np.random.choice(neighbors)
        
        # If no reference point or neighbors, return a central/popular location
        central_locations = ["Meskel Square", "Bole Airport", "Stadium", "Mexico Square"]
        for loc in central_locations:
            if loc in self.graph.nodes:
                return loc
        
        # Last resort: return any location
        return np.random.choice(list(self.graph.nodes))
    
    def find_nearest_known_location(self, unknown_location):
        """Find a known location with a similar name"""
        known_locations = list(self.graph.nodes)
        
        # Try simple text matching
        best_match = None
        best_score = 0
        
        for loc in known_locations:
            # Calculate similarity score (simple substring matching)
            unknown_lower = unknown_location.lower()
            loc_lower = loc.lower()
            
            if unknown_lower in loc_lower or loc_lower in unknown_lower:
                score = len(set(unknown_lower) & set(loc_lower)) / max(len(unknown_lower), len(loc_lower))
                if score > best_score:
                    best_score = score
                    best_match = loc
        
        # If no good match found by name, return a central location
        if best_match is None or best_score < 0.3:
            central_locations = ["Meskel Square", "Bole Airport", "Stadium", "Mexico Square"]
            return np.random.choice(central_locations)
            
        return best_match
    def hill_climbing_search_all_paths(self, start, goal, max_paths=5, blocked_edge=None):
        """Implement hill climbing search algorithm that can find multiple paths"""
        # First, try to find at least one path
        initial_path, distance, time = self.hill_climbing_search(start, goal, blocked_edge)
        
        if not initial_path:
            return []  # No path found
        
        all_paths = [(initial_path, distance, time)]
        
        # Try different starting neighbors to find alternative paths
        neighbors = list(self.graph.neighbors(start))
        
        for neighbor in neighbors:
            if len(all_paths) >= max_paths:
                break
                
            # Skip if already in a path
            if any(neighbor in path[0][1:3] for path in all_paths):
                continue
                
            # Try hill climbing from this neighbor
            alt_path, alt_dist, alt_time = self.hill_climbing_search_with_first_step(start, neighbor, goal, blocked_edge)
            
            if alt_path and not self.is_similar_path(alt_path, [p[0] for p in all_paths]):
                all_paths.append((alt_path, alt_dist, alt_time))
        
        # Sort paths by distance (or time if time optimization is enabled)
        if self.time_cost_constraints:
            all_paths.sort(key=lambda x: x[2])  # Sort by time
        else:
            all_paths.sort(key=lambda x: x[1])  # Sort by distance
        
        return all_paths
    
    def hill_climbing_search(self, start, goal, blocked_edge=None):
        """Basic hill climbing search implementation"""
        current = start
        path = [current]
        visited = {current}
        total_distance = 0
        total_time = 0
        
        while current != goal:
            # Find all neighbors of current node
            neighbors = list(self.graph.neighbors(current))
            if not neighbors:
                return None, 0, 0  # No neighbors, search fails
                
            # Filter out already visited neighbors
            neighbors = [n for n in neighbors if n not in visited]
            if not neighbors:
                return None, 0, 0  # No unvisited neighbors, search fails
                
            # Apply blocked road constraint
            if blocked_edge:
                u, v = blocked_edge
                # Filter out neighbors if the edge (current, neighbor) is the blocked edge
                neighbors = [n for n in neighbors if not ((current == u and n == v) or (current == v and n == u))]
                if not neighbors:
                    return None, 0, 0
            
            # Evaluate neighbors based on elevation difference to goal
            # (Closer to goal's elevation is better in hill climbing)
            next_node = None
            best_value = float('inf')
            
            goal_elevation = self.graph.nodes[goal]['elevation']
            
            for neighbor in neighbors:
                neighbor_elevation = self.graph.nodes[neighbor]['elevation']
                # Calculate elevation difference to goal
                elevation_diff = abs(neighbor_elevation - goal_elevation)
                
                # Apply time/cost constraint if enabled
                cost_factor = 0
                if self.time_cost_constraints:
                    cost_factor = self.graph[current][neighbor]['travel_time']
                    
                # Total evaluation (lower is better)
                evaluation = elevation_diff + cost_factor
                
                if evaluation < best_value:
                    best_value = evaluation
                    next_node = neighbor
            
            if next_node is None:
                return None, 0, 0  # No valid next node, search fails
                
            # Update path and tracking variables
            edge_distance = self.graph[current][next_node]['distance']
            edge_time = self.graph[current][next_node]['travel_time']
            
            total_distance += edge_distance
            total_time += edge_time
            
            current = next_node
            path.append(current)
            visited.add(current)
            
            # Break if we're stuck in a loop
            if len(path) > len(self.graph.nodes) * 2:
                return None, 0, 0  # Likely in a loop, search fails
        
        return path, round(total_distance, 2), round(total_time, 2)

    def hill_climbing_search_with_first_step(self, start, first_step, goal, blocked_edge=None):
        """Hill climbing with forced first step to find alternative paths"""
        if first_step not in self.graph.neighbors(start):
            return None, 0, 0  # Invalid first step
            
        # Calculate initial step metrics
        initial_distance = self.graph[start][first_step]['distance']
        initial_time = self.graph[start][first_step]['travel_time']
        
        # Start from the first step
        current = first_step
        path = [start, current]
        visited = {start, current}
        total_distance = initial_distance
        total_time = initial_time
        
        # Continue with regular hill climbing
        while current != goal:
            # Similar to hill_climbing_search
            neighbors = list(self.graph.neighbors(current))
            if not neighbors:
                return None, 0, 0
                
            neighbors = [n for n in neighbors if n not in visited]
            if not neighbors:
                return None, 0, 0
                
            if blocked_edge:
                u, v = blocked_edge
                neighbors = [n for n in neighbors if not ((current == u and n == v) or (current == v and n == u))]
                if not neighbors:
                    return None, 0, 0
            
            next_node = None
            best_value = float('inf')
            goal_elevation = self.graph.nodes[goal]['elevation']
            
            for neighbor in neighbors:
                neighbor_elevation = self.graph.nodes[neighbor]['elevation']
                elevation_diff = abs(neighbor_elevation - goal_elevation)
                
                cost_factor = 0
                if self.time_cost_constraints:
                    cost_factor = self.graph[current][neighbor]['travel_time']
                    
                evaluation = elevation_diff + cost_factor
                
                if evaluation < best_value:
                    best_value = evaluation
                    next_node = neighbor
            
            if next_node is None:
                return None, 0, 0
                
            edge_distance = self.graph[current][next_node]['distance']
            edge_time = self.graph[current][next_node]['travel_time']
            
            total_distance += edge_distance
            total_time += edge_time
            
            current = next_node
            path.append(current)
            visited.add(current)
            
            if len(path) > len(self.graph.nodes) * 2:
                return None, 0, 0
        
        return path, round(total_distance, 2), round(total_time, 2)
    def greedy_search_all_paths(self, start, goal, max_paths=5, epsilon=0.1, blocked_edge=None):
        """Find multiple paths using greedy search with randomization"""
        all_paths = []
        
        # Try multiple runs with different heuristic weightings
        for i in range(max_paths * 2):  # Try more times than needed to ensure we get diverse paths
            if len(all_paths) >= max_paths:
                break
                
            # Add some randomness to the heuristic to find alternative paths
            random_factor = 1.0 + (np.random.random() * epsilon * i)
            
            path, distance, time = self.greedy_search(start, goal, random_factor, blocked_edge)
            
            if path and not self.is_similar_path(path, [p[0] for p in all_paths]):
                all_paths.append((path, distance, time))
        
        # If we still don't have enough paths, try different initial neighbors
        if len(all_paths) < max_paths and len(all_paths) > 0:
            neighbors = list(self.graph.neighbors(start))
            for neighbor in neighbors:
                if len(all_paths) >= max_paths:
                    break
                    
                path, distance, time = self.greedy_search_with_first_step(start, neighbor, goal, blocked_edge)
                
                if path and not self.is_similar_path(path, [p[0] for p in all_paths]):
                    all_paths.append((path, distance, time))
        
        # Sort by distance or time
        if self.time_cost_constraints:
            all_paths.sort(key=lambda x: x[2])  # Sort by time
        else:
            all_paths.sort(key=lambda x: x[1])  # Sort by distance
            
        return all_paths
    
    def greedy_search(self, start, goal, random_factor=1.0, blocked_edge=None):
        """Implement greedy best-first search algorithm"""
        # Priority queue for greedy search (f_score, tiebreaker, node)
        open_set = [(0, 0, start)]
        tiebreaker = 0
        
        # Dictionary to store the path
        came_from = {}
        
        # Set of visited nodes
        visited = set()
        
        while open_set:
            # Get node with lowest heuristic value
            _, _, current = heapq.heappop(open_set)
            
            if current in visited:
                continue
                
            visited.add(current)
            
            # Check if goal is reached
            if current == goal:
                # Reconstruct path
                path = [current]
                while path[0] != start:
                    path.insert(0, came_from[path[0]])
                    
                # Calculate total distance and time
                total_distance = 0
                total_time = 0
                for i in range(len(path) - 1):
                    total_distance += self.graph[path[i]][path[i+1]]['distance']
                    total_time += self.graph[path[i]][path[i+1]]['travel_time']
                    
                return path, round(total_distance, 2), round(total_time, 2)
            
            # Find all neighbors of current node
            for neighbor in self.graph.neighbors(current):
                if neighbor in visited:
                    continue
                
                # Apply blocked road constraint
                if blocked_edge:
                    u, v = blocked_edge
                    if (current == u and neighbor == v) or (current == v and neighbor == u):
                        continue
                
                # Heuristic: direct distance to goal (using coordinates)
                h_score = self.heuristic(neighbor, goal)
                
                # Apply random factor to enable finding different paths
                h_score = h_score * random_factor
                
                # Apply time/cost constraint if enabled
                if self.time_cost_constraints:
                    traffic_factor = self.graph[current][neighbor]['traffic'] / 10.0
                    h_score = h_score * (1 + traffic_factor)
                
                # Add to open set with heuristic score and tiebreaker
                tiebreaker += 1
                heapq.heappush(open_set, (h_score, tiebreaker, neighbor))
                
                # Store path
                if neighbor not in came_from:
                    came_from[neighbor] = current
        
        # No path found
        return None, 0, 0
    
    def greedy_search_with_first_step(self, start, first_step, goal, blocked_edge=None):
        """Greedy search with forced first step to find alternative paths"""
        if first_step not in self.graph.neighbors(start):
            return None, 0, 0  # Invalid first step
            
        # Calculate initial step metrics
        initial_distance = self.graph[start][first_step]['distance']
        initial_time = self.graph[start][first_step]['travel_time']
        
        # Priority queue for greedy search
        open_set = [(0, 0, first_step)]
        tiebreaker = 0
        
        # Dictionary to store the path
        came_from = {first_step: start}
        
        # Set of visited nodes
        visited = set([start])
        
        while open_set:
            # Similar to greedy_search
            _, _, current = heapq.heappop(open_set)
            
            if current in visited:
                continue
                
            visited.add(current)
            
            if current == goal:
                path = [current]
                while path[0] != start:
                    path.insert(0, came_from[path[0]])
                    
                total_distance = 0
                total_time = 0
                for i in range(len(path) - 1):
                    total_distance += self.graph[path[i]][path[i+1]]['distance']
                    total_time += self.graph[path[i]][path[i+1]]['travel_time']
                    
                return path, round(total_distance, 2), round(total_time, 2)
            
            for neighbor in self.graph.neighbors(current):
                if neighbor in visited:
                    continue
                
                if blocked_edge:
                    u, v = blocked_edge
                    if (current == u and neighbor == v) or (current == v and neighbor == u):
                        continue
                
                h_score = self.heuristic(neighbor, goal)
                
                if self.time_cost_constraints:
                    traffic_factor = self.graph[current][neighbor]['traffic'] / 10.0
                    h_score = h_score * (1 + traffic_factor)
                
                tiebreaker += 1
                heapq.heappush(open_set, (h_score, tiebreaker, neighbor))
                
                if neighbor not in came_from:
                    came_from[neighbor] = current
        
        return None, 0, 0
    def a_star_search_all_paths(self, start, goal, max_paths=5, epsilon=0.1, blocked_edge=None):
        """Find multiple paths using A* search with different heuristic weights"""
        all_paths = []
        
        # First try standard A*
        path, distance, time = self.a_star_search(start, goal, blocked_edge=blocked_edge)
        
        if path:
            all_paths.append((path, distance, time))
        
        # If we have one path, try to find alternatives by:
        # 1. Varying the heuristic weight
        # 2. Penalizing edges in the existing path
        if path:
            # Create a modified graph with penalties on existing paths
            modified_graph = self.create_penalized_graph(path)
            
            # Try with higher and lower heuristic weights
            for w in np.linspace(0.8, 1.2, num=max_paths):
                if len(all_paths) >= max_paths:
                    break
                    
                alt_path, alt_dist, alt_time = self.a_star_search(start, goal, heuristic_weight=w, 
                                                                modified_graph=modified_graph, blocked_edge=blocked_edge)
                
                if alt_path and not self.is_similar_path(alt_path, [p[0] for p in all_paths]):
                    all_paths.append((alt_path, alt_dist, alt_time))
        
        # Sort paths by distance or time
        if self.time_cost_constraints:
            all_paths.sort(key=lambda x: x[2])  # Sort by time
        else:
            all_paths.sort(key=lambda x: x[1])  # Sort by distance
            
        return all_paths
    
    def create_penalized_graph(self, path):
        """Create a modified graph with penalties on existing path edges"""
        # Create a copy of the current graph
        G = self.graph.copy()
        
        # Add penalties to edges in the path
        if len(path) > 1:
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                # Increase the cost of these edges
                G[u][v]['distance'] = G[u][v]['distance'] * 1.5
                G[u][v]['travel_time'] = G[u][v]['travel_time'] * 1.5
                
                # Also penalize the reverse edge
                G[v][u]['distance'] = G[v][u]['distance'] * 1.5
                G[v][u]['travel_time'] = G[v][u]['travel_time'] * 1.5
        
        return G
    
    def a_star_search(self, start, goal, heuristic_weight=1.0, modified_graph=None, blocked_edge=None):
        """Implement A* search algorithm with option for heuristic weight and modified graph"""
        # Use provided graph or default graph
        graph = modified_graph if modified_graph else self.graph
        
        # Priority queue for A* search (f_score, tiebreaker, node)
        open_set = [(0, 0, start)]
        tiebreaker = 0
        
        # Dictionary to store the path
        came_from = {}
        
        # g_score[n] is the cost from start to n
        g_score = {node: float('inf') for node in graph.nodes}
        g_score[start] = 0
        
        # f_score[n] is g_score[n] + heuristic(n, goal)
        f_score = {node: float('inf') for node in graph.nodes}
        f_score[start] = self.heuristic(start, goal) * heuristic_weight
        
        # Set of visited nodes (for optimization)
        visited = set()
        
        while open_set:
            # Get node with lowest f_score
            _, _, current = heapq.heappop(open_set)
            
            if current in visited:
                continue
                
            visited.add(current)
            
            # Check if goal is reached
            if current == goal:
                # Reconstruct path
                path = [current]
                while path[0] != start:
                    path.insert(0, came_from[path[0]])
                    
                # Calculate total distance and time using the original graph
                total_distance = 0
                total_time = 0
                for i in range(len(path) - 1):
                    total_distance += self.graph[path[i]][path[i+1]]['distance']
                    total_time += self.graph[path[i]][path[i+1]]['travel_time']
                    
                return path, round(total_distance, 2), round(total_time, 2)
            
            # Find all neighbors of current node
            for neighbor in graph.neighbors(current):
                if neighbor in visited:
                    continue
                    
                # Apply blocked road constraint
                if blocked_edge:
                    u, v = blocked_edge
                    if (current == u and neighbor == v) or (current == v and neighbor == u):
                        continue
                
                # Calculate tentative g_score
                edge_cost = graph[current][neighbor]['distance']
                
                # Apply time/cost constraint if enabled
                if self.time_cost_constraints:
                    # Modify edge cost based on traffic
                    traffic_factor = graph[current][neighbor]['traffic'] / 10.0
                    edge_cost = edge_cost * (1 + traffic_factor)
                
                tentative_g_score = g_score[current] + edge_cost
                
                # If this path is better than any previous one
                if tentative_g_score < g_score[neighbor]:
                    # Update path
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + (self.heuristic(neighbor, goal) * heuristic_weight)
                    
                    # Add to open set with tiebreaker for consistent ordering
                    tiebreaker += 1
                    heapq.heappush(open_set, (f_score[neighbor], tiebreaker, neighbor))
        
        # No path found
        return None, 0, 0
    
    def is_similar_path(self, new_path, existing_paths, similarity_threshold=0.7):
        """Check if a new path is too similar to any existing path"""
        if not existing_paths:
            return False
            
        for path in existing_paths:
            # Calculate Jaccard similarity (intersection over union)
            path_set = set(path)
            new_path_set = set(new_path)
            
            intersection = len(path_set.intersection(new_path_set))
            union = len(path_set.union(new_path_set))
            
            similarity = intersection / union if union > 0 else 0
            
            if similarity > similarity_threshold:
                return True
                
        return False
    
    def heuristic(self, node, goal):
        """Calculate heuristic (straight-line distance) between node and goal"""
        node_coords = self.graph.nodes[node]['pos']
        goal_coords = self.graph.nodes[goal]['pos']
        
        # Calculate Haversine distance (distance on a sphere)
        lat1, lon1 = node_coords
        lat2, lon2 = goal_coords
        
        # Convert to radians
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))
        r = 6371  # Radius of earth in kilometers
        
        return c * r
    
    def show_previous_path(self):
        """Show the previous path in the multiple paths list"""
        if self.multiple_paths and self.current_path_index > 0:
            self.current_path_index -= 1
            
            path, distance, time = self.multiple_paths[self.current_path_index]
            algorithm = self.algorithm_var.get()
            
            self.show_results(path, distance, time, algorithm)
            self.draw_map(path)
            
            # Update navigation buttons
            self.next_path_btn.configure(state="normal")
            if self.current_path_index == 0:
                self.prev_path_btn.configure(state="disabled")
                
            # Update path counter
            self.path_counter.config(text=f"Path {self.current_path_index + 1} of {len(self.multiple_paths)}")
    
    def show_next_path(self):
        """Show the next path in the multiple paths list"""
        if self.multiple_paths and self.current_path_index < len(self.multiple_paths) - 1:
            self.current_path_index += 1
            
            path, distance, time = self.multiple_paths[self.current_path_index]
            algorithm = self.algorithm_var.get()
            
            self.show_results(path, distance, time, algorithm)
            self.draw_map(path)
            
            # Update navigation buttons
            self.prev_path_btn.configure(state="normal")
            if self.current_path_index == len(self.multiple_paths) - 1:
                self.next_path_btn.configure(state="disabled")
                
            # Update path counter
            self.path_counter.config(text=f"Path {self.current_path_index + 1} of {len(self.multiple_paths)}")
    
    def show_results(self, path, distance, time, algorithm):
        """Display the search results in the text area"""
        self.result_text.delete(1.0, tk.END)
        
        self.result_text.insert(tk.END, f"Algorithm: {algorithm}\n\n")
        
        if len(path) <= 1:
            self.result_text.insert(tk.END, "Start and destination are the same location.\n")
            return
            
        self.result_text.insert(tk.END, f"Path found: {' -> '.join(path)}\n\n")
        self.result_text.insert(tk.END, f"Total Distance: {distance} km\n")
        self.result_text.insert(tk.END, f"Estimated Travel Time: {time} min\n\n")
        
        # Display constraints applied
        constraints = []
        if self.blocked_edge:
            constraints.append(f"Road blocked: {self.blocked_edge[0]} <-> {self.blocked_edge[1]}")
        if self.time_cost_constraints:
            constraints.append("Time/traffic optimization")
        if self.handle_unknown_var.get():
            constraints.append("Unknown location handling")
            
        if constraints:
            self.result_text.insert(tk.END, f"Constraints applied: {', '.join(constraints)}\n")
        
        # If multiple paths available, show navigation hint
        if len(self.multiple_paths) > 1:
            self.result_text.insert(tk.END, f"\nFound {len(self.multiple_paths)} possible paths. "
                                          f"Use the 'Previous Path' and 'Next Path' buttons to navigate.\n")
    
    def reset(self):
        """Reset the UI state"""
        self.source_var.set("")
        self.dest_var.set("")
        self.algorithm_var.set("A*")
        self.block_from_var.set("")
        self.block_to_var.set("")
        self.time_cost_var.set(True)
        self.handle_unknown_var.set(True)
        self.result_text.delete(1.0, tk.END)
        self.draw_map()
        
        # Reset path navigation
        self.multiple_paths = []
        self.current_path_index = 0
        self.prev_path_btn.configure(state="disabled")
        self.next_path_btn.configure(state="disabled")
        self.path_counter.config(text="No paths found")

# Main application
def main():
    root = ThemedTk(theme="arc")  # Using a modern theme
    app = PathFinder(root)
    root.mainloop()

if __name__ == "__main__":
    main()
