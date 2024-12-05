import time
start_time = time.time()
end_time = None

def start():
    global start_time
    start_time = time.time()
    
def end():
    global end_time
    end_time = time.time()
    
def total():
    global start_time
    global end_time
    if end_time == None:
        end()
    return end_time - start_time

def ttotal():
    global start_time
    global end_time
    if end_time == None:
        end()
    return 'It took the computer ' + str(end_time - start_time) + ' seconds'
