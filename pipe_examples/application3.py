from multiprocessing import Process,Pipe

def send(child_conn):
    msg = "Hello this is Application#3\nYou can call me the Track Model!\nCalled from Application#1\n"
    child_conn.send(msg)
    child_conn.close()

if __name__ == '__main__':
    print("Hello I am Application#3\nI am the Track Model\nYou called me directly\n")