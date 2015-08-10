from flask import jsonify
from socketModule import socketModule

__author__ = 'AVPetrov'



def test_get_tpregion():
    client=socketModule()
    obj=client.sendRqst("localhost",11101,bytes("get:", 'UTF-8'))
    print(obj)
    obj.out_prediction()


if __name__ == "__main__":
    print("Testing")
    test_get_tpregion()