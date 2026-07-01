import pandas as pd
import numpy as np
from .dataUtils import haversineDistance
from .algorithmSolver import algorithmSolver
from typing import Tuple, List

class RouteCalculator:
    
    def __init__(self, ordersDf: pd.DataFrame):
        self.orders = ordersDf.copy()
        self.distanceMatrix = None
        self.solver = None
    
    def prepareDeliveryPoints(self) -> np.ndarray:
        points = self.orders[['Customer_Lat', 'Customer_Lon']].values
        return points
    
    def calculateDistanceMatrixHaversine(self) -> np.ndarray:
        n = len(self.orders)
        distMatrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    distMatrix[i][j] = haversineDistance(
                        self.orders.iloc[i]['Restaurant_Lat'],
                        self.orders.iloc[i]['Restaurant_Lon'],
                        self.orders.iloc[j]['Customer_Lat'],
                        self.orders.iloc[j]['Customer_Lon']
                    )
        
        self.distanceMatrix = distMatrix
        return distMatrix
    
    def optimizeRoute(self, method: str = 'nearestNeighbor2Opt') -> Tuple[List[int], float, dict]:
        if self.distanceMatrix is None:
            self.calculateDistanceMatrixHaversine()
        
        self.solver = algorithmSolver(self.distanceMatrix)
        route, distance = self.solver.solve(method=method)
        
        stats = {
            'totalDistanceKm': distance,
            'numberOfStops': len(route),
            'averageDistancePerStop': distance / len(route),
            'methodUsed': method
        }
        
        return route, distance, stats
    
    def getRouteDetails(self, route: List[int]) -> pd.DataFrame:
        
        routeDetails = self.orders.iloc[route][
            ['Order_ID', 'Restaurant_ID', 'City', 'Restaurant_Lat', 
             'Restaurant_Lon', 'Customer_Lat', 'Customer_Lon']
        ].reset_index(drop=True)
        
        routeDetails['Stop_Number'] = range(1, len(routeDetails) + 1)
        
        return routeDetails