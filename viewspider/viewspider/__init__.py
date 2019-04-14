"""
class A():
    def __init__(self,name,**kwargs):
        self.name=name
        #kwargs.setdefault(self,'age')

    def set_attr(self,attrs):
        for key,value in attrs.items():
            if hasattr(self,key) and key != id:
                setattr(self,key,value)

    def _name(self):
        print(self.name)

a=A(name="ss",whom = "you")
a._name()
print(hasattr(a,"name"),hasattr(a,"_name"))
print(getattr(a,"name"),getattr(a,"_name"))
"""


