"""
Author: Vladislav Slugin (vsdev.)
Date: 11.04.2024
Version: 1.1

Description:
This program is a stock market simulator with a graphical user interface (GUI).
Users can visualize real-time stock price changes and buy and sell stocks.
Stock prices are updated automatically every 5 seconds to reflect simulated market conditions.

The program uses Tkinter to create the GUI and Matplotlib to display stock price graphs.

To Do:
- Integrate AI
"""
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
import threading
import time


class Stock:
    def __init__(self, name, initial_price):
        self.name = name
        self.current_price = initial_price
        self.price_history = [initial_price]

    def update_price(self, new_price):
        self.current_price = new_price
        self.price_history.append(new_price)


def simulate_market(stocks):
    while True:
        for stock in stocks:
            # Changing stock
            change = random.randint(-10, 10)
            new_price = max(stock.current_price + change, 1)  # Not < 1
            stock.update_price(new_price)
        time.sleep(5)


class StockApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Stock Simulator")

        self.stocks = [Stock("TechCorp", 100), Stock("HealthPlus", 50)]
        self.selected_stock = None
        self.balance = 1000
        self.portfolio = {stock.name: 0 for stock in self.stocks}

        self.create_widgets()
        self.update_balance_display()

        # Start simulation
        threading.Thread(target=simulate_market, args=(self.stocks,), daemon=True).start()
        self.update()

    def create_widgets(self):
        # UI.
        self.balance_label = tk.Label(self.master, text="")
        self.balance_label.pack()

        self.stock_listbox = tk.Listbox(self.master)
        self.stock_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        for stock in self.stocks:
            self.stock_listbox.insert(tk.END, stock.name)

        self.stock_listbox.bind('<<ListboxSelect>>', self.on_stock_select)

        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.buy_button = tk.Button(self.master, text="Buy", command=self.buy_stock)
        self.buy_button.pack(side=tk.LEFT)

        self.sell_button = tk.Button(self.master, text="Sell", command=self.sell_stock)
        self.sell_button.pack(side=tk.RIGHT)

    def on_stock_select(self, event=None):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            self.selected_stock = self.stocks[index]

            self.ax.clear()
            self.ax.plot(self.selected_stock.price_history)
            self.ax.set_title(self.selected_stock.name)
            self.canvas.draw()

    def buy_stock(self):
        if self.selected_stock and self.balance >= self.selected_stock.current_price:
            self.balance -= self.selected_stock.current_price
            self.portfolio[self.selected_stock.name] += 1
            self.update_balance_display()
        else:
            messagebox.showwarning("Warning", "Not enough balance to buy!")

    def sell_stock(self):
        if self.selected_stock and self.portfolio[self.selected_stock.name] > 0:
            self.balance += self.selected_stock.current_price
            self.portfolio[self.selected_stock.name] -= 1
            self.update_balance_display()
        else:
            messagebox.showwarning("Warning", "You do not own this stock!")

    def update_balance_display(self):
        self.balance_label.config(text=f"Balance: ${self.balance}")
        portfolio_text = "Portfolio: " + ", ".join(
            [f"{name}: {qty}" for name, qty in self.portfolio.items() if qty > 0])
        self.balance_label.config(text=f"Balance: ${self.balance}\n{portfolio_text}")

    def update(self):
        if self.selected_stock is not None:
            self.on_stock_select()

        # Next update after 5000ms (5s)
        self.master.after(5000, self.update)

    def on_stock_select(self, event=None):
        if event:
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                self.selected_stock = self.stocks[index]

        # Updating for selected stock
        if self.selected_stock:
            self.ax.clear()
            self.ax.plot(self.selected_stock.price_history)
            self.ax.set_title(self.selected_stock.name)
            self.canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = StockApp(root)
    root.mainloop()
