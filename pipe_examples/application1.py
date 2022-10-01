from multiprocessing import Process,Queue,Pipe
from application2 import send as send2
from application3 import send as send3
from application4 import send as send4
from application5 import send as send5

if __name__ == '__main__':
    #Assumes this application is the CTC office
    print("Hello this is application#1\nYou can call me the CTC Office!\nYou called me directly\n")

    parent_conn,app2= Pipe()
    p2 = Process(target=send2, args=(app2,))
    p2.start()
    print(parent_conn.recv())   # prints "Hello"

    parent_conn,app3= Pipe()
    p3 = Process(target=send3, args=(app3,))
    p3.start()
    print(parent_conn.recv())   # prints "Hello"

    parent_conn,app4= Pipe()
    p4 = Process(target=send4, args=(app4,))
    p4.start()
    print(parent_conn.recv())   # prints "Hello"

    parent_conn,app5= Pipe()
    p5 = Process(target=send5, args=(app5,))
    p5.start()
    print(parent_conn.recv())   # prints "Hello"