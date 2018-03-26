# option-Pricing
Calculating Option Prices of European Call/Put and American Put using Finite Difference Method and Studying it's convergence to Black Scholes Equation as the number of steps are increased. 

Function - priceOption(strike,time,spotPrice,sigma,rateOfInterest,divident,numberOfTimeSteps,numberOfPriceSteps,optionType,option):


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

Return- Value of the option
