#!/usr/bin/env python
# -*- coding:utf-8 -*-

# Importations
from flask import Flask
from flask import render_template
from flask import request
import sqlite3 as lite
import time

startTime=time.time()

chemin_BDD="E:\Drive\ENSAM\PJT_WEB-BDD\Versions\V_dev\BDD.db"
con = lite.connect(chemin_BDD)
con.row_factory=lite.Row
cur = con.cursor()

def SQL(query):
	n=len(query)
	print(n*"_"+"\n"+query+"\n")
	cur.execute(query)
	print(n*"-")
	if (query[0]=="S"):
		_return=cur.fetchall()
	elif (query[0]=="U" or query[0]=="I"):
		con.commit()
		_return=None
	return _return

def set_CommandeVehicule(Id_vehicule,Id_option):
	SQL("INSERT INTO CommandeVehicule (Id_vehicule,Options,Date_Commande) VALUES ('{}','{}','{}')".format(Id_vehicule,Id_option,int(time.time()-startTime)))
	SQL("INSERT INTO Historique(Date,Commande,Emeteur,Recepteur,Information) VALUES ('{}','{}','{}','{}','{}')".format(int(time.time()-startTime),Id_vehicule,"Client","Agilean","Commande "+get_NomVehicule(Id_vehicule)+" "+get_NomOption(Id_option)))
	return
def set_CommandeKit(Id_kit,Id_commande):
	SQL("INSERT INTO CommandeKit (Id_kit,DateCommande,Id_commande) VALUES ('{}','{}','{}')".format(Id_kit,int(time.time()-startTime),Id_commande))
	SQL("INSERT INTO Historique(Date,Commande,Emeteur,Recepteur,Information) VALUES ('{}','{}','{}','{}','{}')".format(int(time.time()-startTime),Id_commande,"Agilean","Agilog","Commande "+get_NomKit(Id_kit)))
	return
def set_LancementVehicule(Id_commande):
	SQL("UPDATE CommandeVehicule SET (DateLancement)=('{}') WHERE Id='{}'".format(int(time.time()-startTime),Id_commande))
	s=SQL("SELECT Id_kit FROM Kit_Option WHERE Id_Option='{}'".format(get_IdOption(Id_commande)))+SQL("SELECT Id_kit FROM Kit_Vehicule WHERE Id_vehicule='{}'".format(get_IdVehicule(Id_commande)))
	kits=[]
	for i in s:
		for id_kit in i:
			kits.append(id_kit)
	for id_kit in kits:
		set_CommandeKit(id_kit,Id_commande)
	SQL("INSERT INTO Historique(Date,Commande,Emeteur,Recepteur,Information) VALUES ('{}','{}','{}','{}','{}')".format(int(time.time()-startTime),Id_commande,"Agilean","Client","Commande "+"Lancement "+get_NomVehicule(Id_vehicule)+" "+get_NomOption(Id_option)))
	return
def set_PreparationKit(Id_kit):
	SQL("UPDATE CommandeKIT SET DatePreparation WHERE Id='{}'".format(Id_kit))
	SQL("INSERT INTO Historique(Date,Commande,Emeteur,Recepteur,Information) VALUES ('{}','{}','{}','{}','{}')".format(int(time.time()-startTime),get_IdCommande(Id_kit),"Agilog","Agilean","Preparation "+get_NomKit(Id_kit)))
	return
def set_LivraisonKit(Id_kit):
	SQL("UPDATE CommandeKIT SET DateLivraison WHERE Id='{}'".format(Id_kit))
	SQL("INSERT INTO Historique(Date,Commande,Emeteur,Recepteur,Information) VALUES ('{}','{}','{}','{}','{}')".format(int(time.time()-startTime),get_IdCommande(Id_kit),"Agilog","Agilean","Livraison "+get_NomKit(Id_kit)))
	return
def set_ReceptionKit(Id_kit):
	SQL("UPDATE CommandeKIT SET DateReception WHERE Id='{}'".format(Id_kit))
	SQL("INSERT INTO Historique(Date,Commande,Emeteur,Recepteur,Information) VALUES ('{}','{}','{}','{}','{}')".format(int(time.time()-startTime),get_IdCommande(Id_kit),"Agilean","Agilog","Reception "+get_NomKit(Id_kit)))
	return
def set_ConstructionVehicule(Id_commande):
	SQL("UPDATE CommandeVehicule SET (DateConstruction)=('{}') WHERE Id='{}'".format(int(time.time()-startTime),Id_commande))
	SQL("INSERT INTO Historique(Date,Commande,Emeteur,Recepteur,Information) VALUES ('{}','{}','{}','{}','{}')".format(int(time.time()-startTime),Id_commande,"Agilean","Client","Commande "+"Construction "+get_NomVehicule(Id_vehicule)+" "+get_NomOption(Id_option)))
	return
def set_ControleVehicule(Id_commande):
	SQL("UPDATE CommandeVehicule SET (DateControle)=('{}') WHERE Id='{}'".format(int(time.time()-startTime),Id_commande))
	SQL("INSERT INTO Historique(Date,Commande,Emeteur,Recepteur,Information) VALUES ('{}','{}','{}','{}','{}')".format(int(time.time()-startTime),Id_commande,"Agilean","Client","Commande "+"Controle "+get_NomVehicule(Id_vehicule)+" "+get_NomOption(Id_option)))
	return
def set_VenteVehicule(Id_commande):
	SQL("UPDATE CommandeVehicule SET (DateVente)=('{}') WHERE Id='{}'".format(int(time.time()-startTime),Id_commande))
	SQL("INSERT INTO Historique(Date,Commande,Emeteur,Recepteur,Information) VALUES ('{}','{}','{}','{}','{}')".format(int(time.time()-startTime),Id_commande,"Client","Agilean","Commande "+"Vente "+get_NomVehicule(Id_vehicule)+" "+get_NomOption(Id_option)))
	return

def get_IdCommande(Id_kit):
	return SQL("SELECT Id_commande FROM CommandeKit WHERE Id='{}'".format(Id_kit))
def get_IdVehicule(Id_commande):
	return SQL("SELECT Id_vehicule FROM CommandeVehicule WHERE Id='{}'".format(Id_commande))[0][0]
def get_IdKit(Id_commande):
	return SQL("SELECT Id FROM CommandeKit WHERE Id='{}'".format(Id_commande))[0][0]
def get_IdOption(Id_commande):
	return SQL("SELECT Id_option FROM CommandeVehicule WHERE Id='{}'".format(Id_commande))[0][0]
def get_NomVehicule(Id_vehicule):
	return SQL("SELECT nom FROM Vehicule WHERE Id='{}'".format(Id_vehicule))[0][0]
def get_NomKit(Id_kit):
	return SQL("SELECT nom FROM Kit WHERE Id='{}'".format(Id_kit))[0][0]
def get_NomOption(Id_option):
	return SQL("SELECT nom FROM Option WHERE Id='{}'".format(Id_option))[0][0]
def get_IdKits(Id_commande):
	Id_vehicule=get_IdVehicule(Id_commande)
	Id_option=get_IdOption(Id_commande)
	s=SQL("SELECT Id_kit FROM Kit_Option WHERE Id_Option='{}'".format(Id_option))+SQL("SELECT Id_kit FROM Kit_Vehicule WHERE Id_vehicule='{}'".format(Id_vehicule))
	liste=[]
	for i in s:
		for id_kit in i:
			liste.append(id_kit)
	return liste
def get_logs():
	historique=SQL("SELECT * FROM Historique ORDER BY Id DESC")
	logs=[]
	for i in range(len(historique)):
		log={}
		log["Id"]=historique[i][0]
		log["Date"]=historique[i][1]
		log["Commande"]=historique[i][2]
		log["Emeteur"]=historique[i][3]
		log["Recepteur"]=historique[i][4]
		log["Information"]=historique[i][5]
		logs.append(log)
	return logs

set_LancementVehicule(1)

#Initialisations
app = Flask(__name__)

@app.route('/')

@app.route('/index')
def index():
	return render_template('index.html',logs=get_logs())
	
#@app.route('/Site_Accueil')
#def site_accueil():
#	Temps = int(time.time()-startTime)
#	return render_template('Site_Accueil.html', Temps=Temps)
	
@app.route('/Site_Agilean_Visuel')
def site_agilean_Visuel():
	commandes=[]
	IDs=Commandes() 
	for Id in IDs:
		commande={}
		commande['Id']=Id
		commande['Vehicule']=Vehicule(Id)
		commande['Options']=Options(Id)
		commande['Date_Commande']=Date_Commande(Id)
		commande['Date_Lancement']=Date_Lancement(Id)
		commande['Date_Envoi']=Date_Envoi(Id)
		commande['Date_Livraison']=Date_Livraison(Id)
		commande['Date_Reception']=Date_Reception(Id)
		commande['Date_Controle']=Date_Controle(Id)
		commande['Date_Vente']=Date_Vente(Id)
		commandes.append(commande)
	return render_template('Site_Agilean_Visuel.html',commandes=commandes, Temps=int(time.time()-startTime))

@app.route('/Site_Agilean_Formulaire',methods=['GET','POST'])
def site_agilean_Formulaire():
	if (request.method == 'POST'):
		if (request.form['Vehicule']!=""):
			Options=""
			if request.form.get('100'):
				Options+="1"
			else:
				Options+="0"
			if request.form.get('010'):
				Options+="1"
			else:
				Options+="0"
			if request.form.get('010'):
				Options+="1"
			else:
				Options+="0"
			set_Commande(request.form['Vehicule'],Options,int(time.time()-startTime))
		elif (str(request.form['Numero_Lancement'])!="0"):
			set_Lancement(request.form['Numero_Lancement'],int(time.time()-startTime))
		elif (str(request.form['Numero_Reception'])!="0"):
			if (str(request.form['Conforme_Reception'])=="1"):
				set_Reception(request.form['Numero_Reception'],int(time.time()-startTime))
			else:
				refus_Reception(request.form['Numero_Reception'],int(time.time()-startTime))
		elif (str(request.form['Numero_Controle'])!="0"):
			print(30*"#")
			print(str(request.form['Numero_Controle']))
			if (str(request.form['Conforme_Controle'])=="1"):
				set_Controle(request.form['Numero_Controle'],int(time.time()-startTime))
			else:
				refus_Controle(request.form['Numero_Controle'],int(time.time()-startTime))
		elif (str(request.form['Numero_Vente'])!="0"):
			if (str(request.form['Conforme_Vente'])=="1"):
				set_Vente(request.form['Numero_Vente'],int(time.time()-startTime))
			else:
				refus_Vente(request.form['Numero_Vente'],int(time.time()-startTime))
	return render_template('Site_Agilean_Formulaire.html')

@app.route('/Site_Agilog_Visuel')
def site_agilog_Visuel():
	commandes=[]
	IDs=Commandes() 
	for Id in IDs:
		commande={}
		commande['Id']=Id
		commande['Vehicule']=Vehicule(Id)
		commande['Options']=Options(Id)
		commande['Date_Lancement']=Date_Lancement(Id)
		commande['Date_Envoi']=Date_Envoi(Id)
		commande['Date_Livraison']=Date_Livraison(Id)
		commande['Date_Reception']=Date_Reception(Id)
		commandes.append(commande)
	return render_template('Site_Agilog_Visuel.html',commandes=commandes,Temps=int(time.time()-startTime))
	
@app.route('/Site_Agilog_Formulaire',methods=['POST','GET'])
def site_agilog_Formulaire():
	if (request.method == 'POST'):
		Numero_Envoi=request.form['Numero_Envoi']
		Numero_Livraison=request.form['Numero_Livraison']
		if(str(Numero_Envoi)!="0"):
			set_Envoi(Numero_Envoi,int(time.time()-startTime))
		elif(str(Numero_Livraison)!="0"):
			set_Livraison(Numero_Livraison,int(time.time()-startTime))
	return render_template('Site_Agilog_Formulaire.html')
	
if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, port=5571)

