import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import numpy as np
from src.algorithmSolver import algorithmSolver
from src.dataUtils import haversineDistance

class TestHaversineDistance:
    def testSamePoint(self):
        dist = haversineDistance(0, 0, 0, 0)
        assert dist == 0

    def testKnownDistance(self):
        dist = haversineDistance(30.05, 31.23, 30.02, 31.22)
        assert 3 < dist < 4 # Distancia real Cairo-Giza es ~3.5 km

class TestalgorithmSolver:
    @pytest.fixture
    def simpleDistanceMatrix(self):
        return np.array([
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0]
        ])

    def testSolverInit(self, simpleDistanceMatrix):
        solver = algorithmSolver(simpleDistanceMatrix)
        assert solver.nPoints == 4

    def testRouteDistCalculation(self, simpleDistanceMatrix):
        solver = algorithmSolver(simpleDistanceMatrix)
        route = [0, 1, 2, 3]
        distance = solver.calculateRouteDistance(route)
        expected = 10 + 35 + 30 + 20
        assert distance == expected

    def testNearestNeighbor(self, simpleDistanceMatrix):
        solver = algorithmSolver(simpleDistanceMatrix)
        route, distance = solver.nearestNeighbor(startPoint=0)
        assert len(route) == 4
        assert route[0] == 0
        assert distance > 0

    def testTwoOptImprov(self, simpleDistanceMatrix):
        solver = algorithmSolver(simpleDistanceMatrix)
        initial_route = [0, 2, 3, 1]
        initial_distance = solver.calculateRouteDistance(initial_route)

        optimized_route, optimized_distance = solver.twoOpt(initial_route)
        assert optimized_distance <= initial_distance

if __name__ == '__main__':
    pytest.main([__file__, '-v'])