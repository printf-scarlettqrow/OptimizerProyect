import numpy as np
from typing import List, Tuple
from itertools import permutations
import warnings

class algorithmSolver:
    
    def __init__(self, distanceMatrix: np.ndarray):
        self.distanceMatrix = distanceMatrix
        self.nPoints = len(distanceMatrix)
        self.bestRoute = None
        self.bestDistance = float('inf')
    
    def calculateRouteDistance(self, route: List[int]) -> float:
        total = 0
        for i in range(len(route) - 1):
            total += self.distanceMatrix[route[i]][route[i+1]]
        total += self.distanceMatrix[route[-1]][route[0]]
        return total
    
    @staticmethod
    def calculateDistanceMatrix(coords: np.ndarray) -> np.ndarray:
        n = len(coords)
        distMatrix = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i != j:
                    distMatrix[i][j] = np.linalg.norm(coords[i] - coords[j])
        return distMatrix
    
    def nearestNeighbor(self, startPoint: int = 0) -> Tuple[List[int], float]:
        unvisited = set(range(self.nPoints))
        current = startPoint
        route = [current]
        unvisited.remove(current)
        
        while unvisited:
            nearest = min(unvisited, 
                         key=lambda x: self.distanceMatrix[current][x])
            route.append(nearest)
            unvisited.remove(nearest)
            current = nearest
        
        distance = self.calculateRouteDistance(route)
        return route, distance
    
    def twoOpt(self, route: List[int], maxIterations: int = 1000) -> Tuple[List[int], float]:
        bestRoute = route.copy()
        bestDistance = self.calculateRouteDistance(bestRoute)
        improved = True
        iterations = 0
        
        while improved and iterations < maxIterations:
            improved = False
            iterations += 1
            
            for i in range(1, len(bestRoute) - 1):
                for j in range(i + 1, len(bestRoute)):
                    # Crear nueva ruta intercambiando segmento
                    newRoute = bestRoute[:i] + bestRoute[i:j][::-1] + bestRoute[j:]
                    newDistance = self.calculateRouteDistance(newRoute)
                    
                    if newDistance < bestDistance:
                        bestRoute = newRoute
                        bestDistance = newDistance
                        improved = True
                        break
                
                if improved:
                    break
        
        return bestRoute, bestDistance
    
    def nearestNeighborWith2Opt(self, startPoint: int = 0, maxIterations: int = 1000) -> Tuple[List[int], float]:
        initialRoute, _ = self.nearestNeighbor(startPoint)
        optimizedRoute, optimizedDistance = self.twoOpt(initialRoute, maxIterations)
        
        return optimizedRoute, optimizedDistance
    
    def solve(self, method: str = 'nearestNeighbor2Opt', 
              startPoint: int = 0) -> Tuple[List[int], float]:
        
        if method == 'nearestNeighbor':
            return self.nearestNeighbor(startPoint)
        elif method == 'nearestNeighbor2Opt':
            return self.nearestNeighborWith2Opt(startPoint)
        else:
            raise ValueError(f"Método desconocido: {method}")