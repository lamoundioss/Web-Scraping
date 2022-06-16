from numpy import integer
from sqlalchemy import Boolean, Column, ForeignKey,String,Integer,TEXT
import base
from sqlalchemy.orm import *

class Telephones(base.base):
    __tablename__='telephones'
    id_telephone=Column(Integer, primary_key=True)
    marque=Column(String(50))
    modele=Column(String(50))
    price=Column(String(50))
    id_vendeur=Column(String(50))
    id_car=Column(String(50))
    def __init__(self, id_telephone, marque, modele, price, id_vendeur, id_car ):
        self.id_telephone=id_telephone
        self.marque=marque
        self.modele=modele
        self.price=price
        self.id_vendeur=id_vendeur
        self.id_car=id_car


class Vendeur(base.base):
    __tablename__='vendeurs'
    id_vendeur=Column(Integer, primary_key=True)
    name=Column(String(50))
    
    def __init__(self, id_vendeur, name):
        self.id_vendeur=id_vendeur
        self.name=name
        
class Caracteristique(base.base):
    __tablename__='caracteristiques'
    id_car=Column(Integer, primary_key=True)
    memoire=Column(String(50))
    ram=Column(String(50))
    def __init__(self, id_car, memoire, ram):
        self.id_car=id_car
        self.memoire=memoire
        self.ram=ram
        

# base.init_base()