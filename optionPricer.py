import math
import numpy as np
'''
Function to Calculate the Price of vanilla European or American Options

Method Used- Finite Difference Method

Inputs- strike- Strike Price
        time- Maturity (in years)
        spotPrice- Spot Price
        sigma- volatility 
        rateOfInterest- risk free interest rate
        divident - annual divident yield
        numberOfTimeSteps - number of time steps
        numberOfPriceSteps- number of price steps
        optionType - "CALL" or "PUT"
        option = "American" or "European"
        
        returns - value of the option
        
'''
def priceOption(strike,time,spotPrice,sigma,rateOfInterest,divident,numberOfTimeSteps,numberOfPriceSteps,optionType,option):
    #Calculating time Steps given the time to Maturity and number of Time Steps
    timeStep = time/numberOfTimeSteps
    
    #Calculating nu to make further calculations simpler (r-q- (0.5 𝜎^2))
    nu = rateOfInterest-divident-0.5*sigma**2
    
    #sigma max as a way to create a relation between dx and dt i.e sigmaMax = priceStep/sqrt(timeStep), approximating
    #the value of sigma max from stability condition nu*sqrt(dt)/sigmamax < 1
    sigmaMax = 2*nu*np.sqrt(timeStep)
    
    #verifying stability condition sigma^2*dt < dx^2
    if sigmaMax < sigma*np.sqrt(2):
        sigmaMax = sigma* np.sqrt(2)
    
    priceStep = sigmaMax*np.sqrt(timeStep)
    
    #a variable to simplify calculations of probabilities
    p = 0.5*(sigma/sigmaMax)**2    
    
    #probability of going up in next step
    pu = p + 0.5*np.sqrt(timeStep)*nu/sigmaMax
    
    #probability of neither going up nor going down
    pm = 1.0 - 2*p
    
    #probability of going down
    pd = p - 0.5*np.sqrt(timeStep) * nu/sigmaMax 
    
    #a variable to simplify calculations
    D = 1/(1+rateOfInterest*timeStep)
    
    #exponentional value of price Step
    E = np.exp(sigmaMax*np.sqrt(timeStep))
    
    #List to contain Log prices of stock
    St = range(2*numberOfPriceSteps+1)
    
    #Stock price estimation at (numberOfpriceSteps) below the given price.
    St[0] = spotPrice*np.exp(-numberOfPriceSteps*sigmaMax*np.sqrt(timeStep))
    
    #Estimating Stock prices at each interval of price step
    for i in range(1,2*numberOfPriceSteps+1):
        St[i] = St[i-1]*E
    
    #A grid to store Option prices at all price step and time step
    C = np.zeros([numberOfTimeSteps+1,2*numberOfPriceSteps+1])
    
    while(True):
        
        if(optionType == "CALL" or optionType == "Call" or optionType == "call"):
            
            #Calculating Call Option price at maturity time for all price steps
            for j in range(0,2*numberOfPriceSteps+1):
                C[numberOfTimeSteps][j] = max(0,St[j]-strike)
            
            break
        
        if(optionType == "PUT" or optionType == "Put" or optionType == "put"):
           
            #Calculating Put Option price at maturity time for all price steps
            for j in range(0,2*numberOfPriceSteps+1):
                C[numberOfTimeSteps][j] = max(0,strike-St[j])
            
            break
        
        break
    
    while(True):
        
        if(option == "European"):
            
            #Calculating Option prices at interior points of the grid for European options
            for k in range(numberOfTimeSteps-1,-1,-1):
                
                for l in range(1,2*numberOfPriceSteps):
                    C[k][l] = pu*C[k+1][l+1] + pm*C[k+1][l] + pd*C[k+1][l-1]
                    C[k][l] = C[k][l]*D
                
                C[k][0] = 2*C[k][1]-2*C[k][2]
                C[k][2*numberOfPriceSteps] = 2*C[k][2*numberOfPriceSteps-1] - C[k][2*numberOfPriceSteps-2]
            
            break
        
        if(option == "American"):
            #Calculating Option prices at interior points of the grid for American options
            for k in range(numberOfTimeSteps-1,-1,-1):
                
                for l in range(1,2*numberOfPriceSteps):
                    C[k][l] = pu*C[k+1][l+1] + pm*C[k+1][l] + pd*C[k+1][l-1]
                    C[k][l] = C[k][l]*D
                
                C[k][0] = 2*C[k][1]-2*C[k][2]
                C[k][2*numberOfPriceSteps] = 2*C[k][2*numberOfPriceSteps-1] - C[k][2*numberOfPriceSteps-2]
                
                #Calculating Option prices at initial time for American options
                for i in range(0,2*numberOfPriceSteps+1):
                    
                    if(optionType=="CALL"):
                        C[k][i] = max(C[k][i],St[i]-strike)
                    
                    else:
                        C[k][i] = max(C[k][i],strike-St[i])
                        
            break
        break
    
    #Calculating Gamma
    gamma = (C[1][numberOfPriceSteps+1]+C[1][numberOfPriceSteps-1]-2*C[1][numberOfPriceSteps])/sigmaMax**2
   
    
    return C[0][numberOfPriceSteps]




