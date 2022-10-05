import tkinter as tk
import json
import requests
import time
import datetime
import os
import math

class RealTimeCurrencyConverter():
    def __init__(self,url):
        self.data= requests.get(url).json()
        self.currencies = self.data['rates']

    def convert(self, from_currency, to_currency, amount): 
        initial_amount = amount 
        if from_currency != 'EUR' : 
            amount = amount / self.currencies[from_currency] 
    
        amount = round(amount * self.currencies[to_currency], 4) 
        return amount

 
frame = tk.Tk()
frame.title("steam calculator")
frame.geometry('215x170')
  
def printInput():
    inp = inputtxt.get(1.0, "end-1c")
    try:
        int(inp)
        rTR = requests.get(f"https://store.steampowered.com/api/appdetails/?appids={inp}&cc=TR&l=english&v=1")
        rARS = requests.get(f"https://store.steampowered.com/api/appdetails/?appids={inp}&cc=AR&l=english&v=1")
        TRjson = json.loads(rTR.text)
        ARSjson = json.loads(rARS.text)
        try:
            TR = TRjson[f"{inp}"]["data"]["price_overview"]["final_formatted"]
            ARS = ARSjson[f"{inp}"]["data"]["price_overview"]["final_formatted"]
            name = TRjson[f"{inp}"]["data"]["name"]
            os.system("cls")
            eTR = TR.replace(" TL", "")
            eurTR = eTR.replace(",", ".")
            a, b ,c = eurTR.partition('.')
            TReurr  = math.trunc(float(a+b+c.replace('.','')))
            url = 'https://api.exchangerate-api.com/v4/latest/EUR'
            converter = RealTimeCurrencyConverter(url)
            TReur = converter.convert('TRY','EUR',float(TReurr))
            lbl2.config(text = f'[{name}]: {TR} ({str(TReur)}€)')
            print(f"[{name}]: {TR} ({str(TReur)}€)")

            eARS = ARS.replace("ARS$ ", "")
            eeARS = eARS.replace(",",".")
            n = 0
            for x in eeARS:
                if x == ".":
                    n += 1

            if n == 2 or n > 2:
                a, b, c = eeARS.partition('.')
                eurARS = math.trunc(float(a + c + b.replace('.', '')))
                url = 'https://api.exchangerate-api.com/v4/latest/EUR'
                converter = RealTimeCurrencyConverter(url)
                ARSeur = converter.convert('ARS','EUR',int(eurARS))
            else:
                ARSeur = converter.convert('ARS','EUR',float(eeARS))
            lbl.config(text = f'[{name}]: {ARS} ({ARSeur}€)')
            print(f"[{name}]: {ARS} ({ARSeur}€)")
        except Exception as e:
            print("errore, non è un gioco coglione")
            lbl.config(text = "error, did u put extra lines?\n(or the game id doesn\'t exist)")
            print(e)
    except Exception as e:
        lbl.config(text = 'error, did u put extra lines?\n(or the game id doesn\'t exist)')
        print(e)
    
inputtxt = tk.Text(frame,
                   height = 3,
                   width = 20)
  
inputtxt.pack()
  
printButton = tk.Button(frame,
                        text = "Calculate", 
                        command = printInput)
printButton.pack()
  
lbl = tk.Label(frame, text = "")
lbl2 = tk.Label(frame, text = "")
lbl.pack()
lbl2.pack()
frame.mainloop()