from django.http import HttpResponse
from django.shortcuts import render
from yahoo_fin.stock_info import *
import time
import queue
from threading import Thread

# Create your views here.
def stockPicker(request):
    stock_picker = tickers_nifty50()
    print(stock_picker)
    return render(request, 'mainapp/stockpicker.html', {'stock_picker': stock_picker})


def stockTracker(request):
    stockpicker = request.GET.getlist('stockpicker')
    print(stockpicker)
    print("...........")
    data = {}
    available_stocks = tickers_nifty50()
    for stock in stockpicker:
        print(stock)
        if stock in available_stocks:
            pass
        else:
            return HttpResponse("Error")
    n_threads = len(stockpicker)
    thread_list = []

    start = time.time()
    que =queue.Queue()
    print("start",start)
    # for stock in stockpicker:
    #     result = get_quote_table(stock)
    #     data.update({stock: result})
    for i in range(n_threads):
        thread = Thread(target = lambda q, arg1: q.put({stockpicker[i]: get_quote_table(arg1)}), args=(que,stockpicker[i]))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        data.update(result)
    end = time.time()
    time_taken = end - start
    print("total",time_taken)
    print("end",end)
    print(data)
    return render(request, 'mainapp/stocktracker.html',{'data':data})
