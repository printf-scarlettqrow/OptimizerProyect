import pandas as pd
import os

output_folder = './data'
df = pd.read_csv('./data/datasetOrders.csv')

# Solamente estos son realmente importantes para lo que quiero lograr.
usefulAtributes = [
        'Order_ID', 
        'Restaurant_ID', 
        'City', 
        'Restaurant_Lat', 
        'Restaurant_Lon', 
        'Customer_Lat', 
        'Customer_Lon',
        'Order_Time',
        'Delivery_Time',
        'Delivery_Duration_Minutes'
]

dfUseful = df[usefulAtributes].copy()

# Como en este caso no hay ningún valor nulo, usamos todo no más
print("Valores nulos por columna:")
print(dfUseful.isnull().sum())

# Y creamos una df basada en lo que teníamos no mas
outputPath = os.path.join(output_folder, 'selectedDataset.csv')
dfUseful.to_csv(outputPath, index=False)