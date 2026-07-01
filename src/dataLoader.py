import pandas as pd
import numpy as np
from typing import Tuple, List, Optional
from pathlib import Path

class DataLoader:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.data = None
        
    def load_data(self) -> pd.DataFrame:
        self.data = pd.read_csv(self.filepath)
        self._validate_data()
        return self.data
    
    def _validate_data(self):
        required_cols = ['Order_ID', 'Restaurant_ID', 'City', 
                        'Restaurant_Lat', 'Restaurant_Lon',
                        'Customer_Lat', 'Customer_Lon', 
                        'Order_Time', 'Delivery_Time', 'Delivery_Duration_Minutes']
        missing = set(required_cols) - set(self.data.columns)
        if missing:
            raise ValueError(f"Columnas faltantes: {missing}")
    
    def get_by_city(self, city: str) -> pd.DataFrame:
        if self.data is None:
            self.load_data()
        return self.data[self.data['City'] == city].reset_index(drop=True)
    
    def get_subset(self, city: str, num_orders: int) -> pd.DataFrame:
        city_data = self.get_by_city(city)
        if len(city_data) < num_orders:
            raise ValueError(f"Solo hay {len(city_data)} órdenes en {city}")
        return city_data.head(num_orders).reset_index(drop=True)
    
    def get_unique_cities(self) -> List[str]:
        if self.data is None:
            self.load_data()
        return sorted(self.data['City'].unique().tolist())
    
    def get_statistics(self, city: Optional[str] = None) -> dict:
        data = self.get_by_city(city) if city else self.data
        return {
            'total_orders': len(data),
            'avg_delivery_duration': data['Delivery_Duration_Minutes'].mean(),
            'max_delivery_duration': data['Delivery_Duration_Minutes'].max(),
            'min_delivery_duration': data['Delivery_Duration_Minutes'].min(),
            'unique_restaurants': data['Restaurant_ID'].nunique()
        }