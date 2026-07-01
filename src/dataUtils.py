import numpy as np
from typing import Tuple
import haversine as hs
from haversine import Unit

# Para calcular distancia en kilómetros entre dos puntos geográficos
def haversineDistance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    origen = (lat1, lon1)
    destino = (lat2, lon2)
    distancia_km = hs.haversine(origen, destino, unit=Unit.KILOMETERS)
    return distancia_km

# Validador de coordenadas
def validateCoordinates(lat: float, lon: float) -> bool:
    return -90 <= lat <= 90 and -180 <= lon <= 180

# Separamos las coordenadas en restaurantes y clientes
def parteCoordinates(df) -> Tuple[np.ndarray, np.ndarray]:
    restaurant_coords = df[['Restaurant_Lat', 'Restaurant_Lon']].values
    customer_coords = df[['Customer_Lat', 'Customer_Lon']].values
    return restaurant_coords, customer_coords

# Recorre y aplica la distancia de Haversine para cada pedido
def distanceCalculate(df) -> np.ndarray:
    distances = []
    for _, row in df.iterrows():
        dist = haversineDistance(
            row['Restaurant_Lat'], row['Restaurant_Lon'],
            row['Customer_Lat'], row['Customer_Lon']
        )
        distances.append(dist)
    return np.array(distances)

# Formato de la ruta
def formatingRoute(route: list, cities: list = None) -> str:
    if cities:
        route_str = " → ".join([str(cities[i]) if i < len(cities) else str(i) 
                               for i in route])
    else:
        route_str = " → ".join(map(str, route))
    return route_str

# Formato de la distancia
def formatingDistance(distance_km: float) -> str:
    return f"{distance_km:.2f} km"