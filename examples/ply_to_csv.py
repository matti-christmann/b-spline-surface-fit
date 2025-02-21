import pandas as pd
import numpy as np
import sys

def ply_to_csv(ply_file, csv_file):
    with open(ply_file, 'r') as file:
        lines = file.readlines()
    
    # Find the start of vertex data
    header_ended = False
    vertex_data = []
    for line in lines:
        if header_ended:
            vertex_data.append(list(map(float, line.strip().split())))
        if line.strip() == "end_header":
            header_ended = True
    
    # Convert to DataFrame
    df = pd.DataFrame(vertex_data)
    
    # Save as CSV
    df.to_csv(csv_file, index=False, header=False)
    print(f"Saved CSV file: {csv_file}")

if __name__ == "__main__":

    
    ply_file = "/home/mattichristmann/Dokumente/03 Code/05 scripts/test_env/examples/random_point_cloud.ply"
    csv_file = "random_point_cloud.csv"
    ply_to_csv(ply_file, csv_file)
