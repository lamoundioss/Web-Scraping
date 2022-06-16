from flask import Flask, redirect, url_for,render_template,request,flash
import requests
import modele
import base

# web scraping

app=Flask(__name__)

def recup_data(data):
    for element in data:
        n = data.id


@app.route('/')
def index():
    data_jumia = base.session.query(modele.Telephones).filter(modele.Telephones.id_vendeur=='1').all()
    data_soumari = base.session.query(modele.Telephones).filter(modele.Telephones.id_vendeur=='2').all()
    data_nova = base.session.query(modele.Telephones).filter(modele.Telephones.id_vendeur=='3').all()
    nj = len(data_jumia)
    ns = len(data_soumari)
    nn = len(data_nova)
    print(nj,ns,nn)
    n = [nj,ns,nn]
    car_jumia = base.session.query(modele.Caracteristique).filter(modele.Caracteristique.id_car==data_jumia.id_telephone).all()
    car_soumari = base.session.query(modele.Caracteristique).filter(modele.Caracteristique.id_car==data_soumari.id_telephone).all()
    car_nova = base.session.query(modele.Caracteristique).filter(modele.Caracteristique.id_car==data_nova.id_telephone).all()
    # print('data',data)
    return render_template('index.html', data_jumia = data_jumia, data_soumari=data_soumari, data_nova=data_nova, n=n)

if __name__=='__main__':
    app.run(debug=True) 