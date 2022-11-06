from multiprocessing import Process,Pipe

def send(child_conn):
    msg = "Hello this is Application#4\nYou can call me the Train Model!\nCalled from Application#1\n"
    child_conn.send(msg)
    child_conn.close()

if __name__ == '__main__':
    print("Hello I am Application#4\nI am the Train Model\nYou called me directly\n")