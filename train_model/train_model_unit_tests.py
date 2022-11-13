from train import Train as t
import unittest
import time

class TestTrainModel(unittest.TestCase):

    #startup
    def test_startup(self):
        t.__init__(t)
        t.dispatch(t)
        time.sleep(5)
        t.set_power(t, 120000)
        speed = t.get_speed(t)
        print("testing assert")
        self.assertTrue(speed>0)

    def test_serv_brake(self):
        t.__init__(t)
        t.dispatch(t)

        t.service_brake == 'On'
        t.serv_brake_func(t)

        time.sleep(2)
        speed = t.get_speed(t)
        self.assertTrue(speed == 0)
    
    def test_e_brake(self):
        t.__init__(t)
        t.dispatch(t)

        t.e_brake == 'On'
        t.ebrake(t)

        time.sleep(2)
        speed = t.get_speed(t)
        self.assertTrue(speed == 0)

if __name__ == '__main__':
    print('running unittest')
    unittest.main()
   

