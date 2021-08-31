from django.shortcuts import render, redirect
from fabric import Connection
from ciscoconfparse import CiscoConfParse
from io import open
import logging
import pandas as pd
import telnetlib

from django.views.generic import TemplateView
from .models import Dispositivo
from .forms import DispositivoFormSet

class DispositivosView(TemplateView):
    model = Dispositivo
    template_name = "LanGuardianCont/analisis.html"

    def get(self, *args, **kwargs):

        # Create an instance of the formset
        formset = DispositivoFormSet(queryset=Dispositivo.objects.none())
        return self.render_to_response({'miform': formset})

    def post(self, *args, **kwargs):

        formset = DispositivoFormSet(data=self.request.POST)
        # Check if submitted forms are valid
        if formset.is_valid():
            i=0
            for formu in formset:
                cd = formu.cleaned_data
                lip = cd.get('ip')
                lpuerto = cd.get('puerto')
                lusuario = cd.get('usuario')
                lclave = cd.get('clave')
                lproto = cd.get('protocolo')
                if lproto == '1':
                    res = con_telnet(lip,lpuerto,lusuario,lclave,i)
                else:
                    res = con_ssh(lip,lpuerto,lusuario,lclave,i)
                i=i+1
            #res = True
            if res == True:
                return redirect("/analisis/configuracion")
            else:
                if "Authentication" in res:
                    print("Autenticación fallida. Verifique usuario y contraseña")
                    #ACA VA EL MODAL 1
                else:
                    if "10060" in res:
                        print("Timeout. Dispositivo/puerto sin respuesta")
                        #ACA VA EL MODAL 2
                    else:
                        if "11001" in res:
                            print("Ingrese una IP válida")
                            #ACA VA EL MODAL 3
        return self.render_to_response({'miform': formset})

def con_ssh(ip, puerto, usuario, clave, id):
    logging.info('connection attempt {}'.format(0))
    c = Connection(host=usuario + "@" + ip, connect_kwargs={"password":clave}, port=puerto)
    try:
        c.run('type config.txt')
        f = open("config"+id+".txt", "w")
        f.write(str(c.run('type config.txt')))
        f.close()
        return True
    except Exception as ex:
        return (str(ex))

def con_telnet(ip, puerto, usuario, clave, id):
    logging.info('connection attempt {}'.format(0))
    try:
        tn = telnetlib.Telnet(ip,puerto)
        tn.read_until(b"login: ")
        tn.write(usuario.encode('ascii') + b"\n")
        if clave:
            tn.read_until(b"Password: ")
            tn.write(clave.encode('ascii') + b"\n")
            f = open("config"+id+".txt", "w")
            f.write(str(tn.write(b"ls\n")))
            f.close()
            tn.write(b"exit\n")
            print(tn.read_all().decode('ascii'))
            return True
    except Exception as ex:
        print(str(ex))
        return (str(ex))

def configuracion(request):
    
    ## GUARDO LA CONFIG PARA PASARLA A LA WEB ##
    f = open("config.txt", "r",encoding='utf-8')
    contenido = f.read()
    f.close()
    ## UTILIZO CONFPARSE ##
    parse = CiscoConfParse("config.txt")
    ## LEO TEMPLATE NIST ##
    df = pd.read_excel("NIST.xlsx", sheet_name="NIST", header=0, na_values="NaN")
    
    ## MATCHEO CADA FILA DEL NIST CONTRA LA CONFIG ##
    reco_nist = []
    for index, row in df.iterrows():
        comando = df.iloc[index, 0]
        #print(eval(comando))
        if len(eval(comando)) == 0:
            reco_nist.append(row[1:7])

    return render(request,"LanGuardianCont/configuracion.html", {'cont':contenido, 'nist':reco_nist})
