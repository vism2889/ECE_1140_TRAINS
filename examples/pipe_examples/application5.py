from multiprocessing import Process,Pipe

def send(child_conn):
    msg = "Hello this is Application#5\nYou can call me the Train Controller!\nCalled from Application#1\n"
    child_conn.send(msg)
    child_conn.close()

if __name__ == '__main__':
    print("Hello I am Application#5\nI am the Train Controller\nYou called me directly\n")