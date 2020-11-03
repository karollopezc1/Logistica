# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 12:19:39 2020

@author: Karol Lopez y María Agamez 
"""
from ortools.linear_solver import pywraplp
import numpy as np

#MAXIMIZACION DE COBERTURA

def main ():
    solver = pywraplp.Solver ( 'SolveAssignmentProblemMIP' , 
                           pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING )
    
    #parametros
    C=np.array([[0,35,78,76,98,55 ], #distancia del poblado i al poblado j
                [35,0,60,59,91,81 ],  
                [78,60,0,3,37,87 ],   
                [76,59,3,0,36,83 ] ,
                [98,91,37,36,0,84],
                [55,81,87,83,84,0 ]])
    i=6 #ambulancia
    j=6 #poblados 
    P=2 #cantidad de ambulancias que se deben asignar
    ds=20 #Distancia maxima de servicio	
        
    matrizy=np.zeros((i,j)) #matriz solución 
    matrizx=np.zeros((6,1)) #x
    
    #definición de variables
    
    x = {} #Si la ambulancia se ubica en el npoblado i	
    y  ={} #Si la ambulancia i sirve al poblado j
    
    for a in range (i):
        x [ a ] = solver.BoolVar ( 'x [%i]' % ( a ))
        
    for a in range (i):
        for b in range (j):
            y [ a, b ] = solver.BoolVar ( 'y [%i %i]' % ( a, b ))
    
    #función objetivo
    solver.Maximize(solver.Sum([y[(a,b)] for b in range (j) for a in range (i)]))  
    
    #restricciones
    solver.Add(solver.Sum([x[(a)] for a in range (i) ]) == P)
    
    for a in range (i):
        for b in range(j):
            solver.Add(ds*x[(a)]>=y[(a,b)]*C[(a,b)])
            
    for a in range (i):
        for b in range(j):
            solver.Add(x[(a)]>=y[(a,b)])
                    
    for b in range (j) :
        solver.Add(solver.Sum([y[(a,b)]for a in range( i)])<=1)
     
    #impresion de resultado            
    result_status = solver.Solve()
    if result_status ==0:
        print("solución Optima ", result_status)
    else:
        if result_status==1:
            print("solución Factible ", result_status)
        else:
            print("solución Infactible ", result_status)
    #0:  Optimo
    #1: Factible
    #2: Infactible
    #3: No acotado
    if result_status == solver.OPTIMAL:
        print()
        print("FO = ", solver.Objective().Value())       
        for a in range(i):
            matrizx[a]=x[a].solution_value()
            for b in range (j):
                matrizy[a,b]=y[a,b].solution_value()                
        print()
        print("matriz x_i")
        print(matrizx)
        print("Matriz y_i,j")
        print(matrizy)    
        print()
        print("Time=", solver.WallTime(), "milisegundos")
    else:
        result_status==solver.INFEASIBLE
        print("no solution found")
if __name__ == '__main__':
    main()
   
        
        
    
        