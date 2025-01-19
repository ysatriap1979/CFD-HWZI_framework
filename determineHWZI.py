import pandas as pd
import numpy as np
from stl import mesh
from scipy.interpolate import griddata
import matplotlib.pyplot as plt

# Langkah 1: Baca Data dari Semua File CSV
print("Membaca file CSV...")
files = [
    'sliceData_h355m_utaraSelatan_kEqn.csv',
    'sliceData_h355m_selatanUtara_kEqn.csv',
    'sliceData_h355m_baratTimur_kEqn.csv',
    'sliceData_h355m_timurBarat_kEqn.csv'
]
dfs = []
directions = ['NS', 'SN', 'BT', 'TB']

for i, file in enumerate(files):
    df = pd.read_csv(file)
    df = df[['Points:0', 'Points:1', 'Points:2', 'U_Magnitude']].rename(
        columns={'U_Magnitude': f'U_Magnitude_{directions[i]}'}
    )
    dfs.append(df)

print("Menggabungkan data kecepatan dari semua arah...")
combined = dfs[0]
for df in dfs[1:]:
    combined = pd.merge(combined, df, on=['Points:0', 'Points:1', 'Points:2'], how='outer')
combined.fillna(0, inplace=True)

# Hitung kecepatan maksimum di setiap titik
print("Menghitung kecepatan maksimum...")
combined['U_Max'] = combined[[f'U_Magnitude_{d}' for d in directions]].max(axis=1)

# Langkah 2: Baca File Geometri STL
print("Membaca file geometri Pulau Lemukutan...")
stl_mesh = mesh.Mesh.from_file('geometriLEMUKUTAN.stl')
topo_x = stl_mesh.x.flatten()
topo_y = stl_mesh.y.flatten()
topo_z = stl_mesh.z.flatten()

# Interpolasi nilai topografi
print("Menginterpolasi data geometri...")
points = np.column_stack((topo_x, topo_y))
values = topo_z
grid_points = combined[['Points:0', 'Points:1']].values
combined['Topography_Z'] = griddata(points, values, grid_points, method='linear')

# Hitung jarak vertikal
print("Menghitung jarak vertikal...")
combined['Vertical_Distance'] = 355 - (combined['Topography_Z'] + 10)

# Langkah 3: Filter Zona Potensial Berdasarkan Rentang Jarak Vertikal
print("Memfilter zona High-Wind berdasarkan rentang jarak vertikal...")
vertical_range = (1, 275)  # Rentang jarak vertikal (10-20 meter)
threshold_percent = 0.95  # Ambang batas 70%
V_global_max = combined['U_Max'].max()
V_threshold = threshold_percent * V_global_max
print(f"Ambang batas kecepatan: {V_threshold:.2f} m/s")

combined['High_Wind_Zone'] = (combined['U_Max'] > V_threshold) & \
                             (combined['Vertical_Distance'] >= vertical_range[0]) & \
                             (combined['Vertical_Distance'] <= vertical_range[1])

# Simpan hasil
output_csv = 'high_wind_zones_filtered_new.csv'
combined.to_csv(output_csv, index=False)
print(f"Hasil disimpan ke: {output_csv}")

# Visualisasi
print("Memvisualisasikan hasil zona High-Wind...")
high_wind = combined[combined['High_Wind_Zone']]
plt.figure(figsize=(12, 8))
scatter = plt.scatter(
    high_wind['Points:0'], high_wind['Points:1'],
    c=high_wind['U_Max'], cmap='viridis', s=10, label='High-Wind Zone'
)
plt.colorbar(scatter, label='Kecepatan Maksimum (m/s)')
plt.title(f'Zona Kecepatan Tinggi ({int(threshold_percent * 100)}% dari Maksimum, {vertical_range[0]}-{vertical_range[1]}m)', fontsize=14)
plt.xlabel('X (m)')
plt.ylabel('Y (m)')
plt.grid()
plt.axis('equal')
plt.savefig('high_wind_zone_plot.png', dpi=300)
plt.show()

