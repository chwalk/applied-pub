import numpy as np


bell_curve = None 
 

def create():
    global bell_curve
    bell_curve = np.random.normal(0, 20, 10000)
    return f"Created the bell curve."


def show_point():
    size = bell_curve.size 
    index = np.random.randint(0, size) 
    height = bell_curve[index] 
    print(f"The size of the bell curve is {size}. Found point ({index}, {height}).") 
    return f"Found point ({index}, {height})."


# Main entry point for the cloud function
def bell_curve(request):
    try:
        command = request.args.get('command')
        print(command)
        
        if command: 
            if command == 'create':
                return create()
            elif command == 'show_point':
                return show_point()
            else:
                return f"Command {command} not found."

        return f"This HTTP triggered function executed successfully. Pass a command in the query string or in the request body."
    except Exception as err:
        return f"This HTTP triggered function executed successfully, but errored with {str(err)}."
