#from django.http.response import HttpResponse
#from django.forms.formsets import formset_factory
#from LanGuardianCont.models import Dispositivo
from django.shortcuts import render, redirect
#from django.template import Context
from .forms import formularioCont
from fabric import Connection
from ciscoconfparse import CiscoConfParse
from io import open
import logging
import pandas as pd
import telnetlib

#from django.views.generic.edit import FormView
#from .forms import DispositivoForm

#class AgDispo(FormView):
#    template_name = 'LanGuardianCont/analisis.html'
#    form_class = formset_factory(DispositivoForm)
#    success_url = './configuracion/'

#    def form_valid(self, form):
        
#        for f in form:
#            print(f.cleaned_data['ip'])
#            f.save()
        
#        return super(AgDispo, self).form_valid(form)

def con_ssh(ip, puerto, usuario, clave):
    logging.info('connection attempt {}'.format(0))
    c = Connection(host=usuario + "@" + ip, connect_kwargs={"password":clave}, port=puerto)
    try:
        c.run('type config.txt')
        f = open("config.txt", "w")
        f.write(str(c.run('type config.txt')))
        f.close()
        return True
    except Exception as ex:
        return (str(ex))

def con_telnet(ip, puerto, usuario, clave):
    logging.info('connection attempt {}'.format(0))
    tn = telnetlib.Telnet(ip,puerto)
    tn.read_until(b"login: ")
    tn.write(usuario.encode('ascii') + b"\n")
    if clave:
        tn.read_until(b"Password: ")
        tn.write(clave.encode('ascii') + b"\n")
        f = open("config.txt", "w")
        f.write(str(tn.write(b"ls\n")))
        f.close()
        tn.write(b"exit\n")
        print(tn.read_all().decode('ascii'))
        return True
    #try:
    #    c.run('type config.txt')
    #    f = open("config.txt", "w")
    #    f.write(str(c.run('type config.txt')))
    #    f.close()
    #    return True
    #except Exception as ex:
    #    return (str(ex))

def analisis(request):
    formu_cont=formularioCont()
    #formu2=Dispositivo()
    if request.method=="POST":
        formu_cont=formularioCont(data=request.POST)
        if formu_cont.is_valid():
            #ip=request.POST.get("ip")
            #puerto=request.POST.get("puerto")
            #usuario=request.POST.get("usuario")
            #clave=request.POST.get("clave")
            #res = con_ssh(ip,puerto,usuario,clave)
            res = True
            #error = "pepe"
            if res == True:
                return redirect("/analisis/configuracion")
            else:
                if "Authentication" in res:
                    print("Autenticación fallida. Verifique usuario y contraseña")
                    #ACA VA EL MODAL 1
                    #error = 1
                else:
                    if "10060" in res:
                        print("Timeout. Dispositivo/puerto sin respuesta")
                        #ACA VA EL MODAL 2
                        #error = 2
                    else:
                        if "11001" in res:
                            print("Ingrese una IP válida")
                            #ACA VA EL MODAL 3
                            #error = 3
            #f = open("config2.txt", "w")
            #c = Connection(host=usuario + "@" + ip, connect_kwargs={"password":clave}, port=puerto)
            #f.write(str(c.run('cat pepe.txt')))
            #f.close()

            #try: 
            #    c.run('cat pepe.txt')
            #    return redirect("/analisis/configuracion")
            #except:
            #    return redirect("/analisis/?invalido")

    return render(request,"LanGuardianCont/analisis.html", {'miform':formu_cont})#, 'err':error})

def configuracion(request):
    #from ciscoconfparse import CiscoConfParse
    ## GUARDO LA CONFIG PARA PASARLA A LA WEB ##
    f = open("config.txt", "r",encoding='utf-8')
    contenido = f.read()
    f.close()
    ## UTILIZO CONFPARSE ##
    parse = CiscoConfParse("config.txt")
    ## LEO TEMPLATE NIST ##
    df = pd.read_excel("NIST.xlsx", sheet_name="NIST", header=0, na_values="NaN")
    #print(df["COMANDO"])
    #i=0
    ## MATCHEO CADA FILA DEL NIST CONTRA LA CONFIG ##
    reco_nist = []
    for index, row in df.iterrows():
        comando = df.iloc[index, 0]
        #i=i+1
        #print(index)
        #exec(print(dir()))
        #print ("Comando leido: ",comando)
        #print ("Resultado leido: ",parse.find_objects(r"^aaa new-model"))
        #print ("Real: ",eval('''parse.find_objects(r"^aaa new-model")'''))
        print(eval(comando))
        if len(eval(comando)) == 0:
            #print("RECOMIENDO")
            #descr=row[1]
            #print(descr)
            #raz=row[2]
            #print(raz)
            #imp=row[3]
            #print(imp)
            #reme=row[4]
            #print(reme)
            #com_rem=row[5]
            #print(com_rem)
            #nist=row[6]
            #print(nist)
            reco_nist.append(row[1:7])
    #print(lista_reco2)
    #p1 = parse.find_objects(r"^aaa new-model")

    #if (len(p1) == 0):
    #desc = "Habilite el sistema de control de acceso AAA"
    #razon = "Los servicios de autenticación, autorización y contabilidad (AAA) proporcionan una fuente autorizada para administrar y monitorear el acceso de los dispositivos. La centralización del control mejora la coherencia del control de acceso, los servicios a los que se puede acceder una vez autenticados y la responsabilidad mediante el seguimiento de los servicios a los que se accede. Además, la centralización del control de acceso simplifica y reduce los costos administrativos de aprovisionamiento y desaprovisionamiento de cuentas, especialmente cuando se administra una gran cantidad de dispositivos"
    #razon = "Los servicios de autenticación, autorización y contabilidad (AAA) proporcionan una fuente autorizada para administrar y monitorear el acceso de los dispositivos."
    #impacto = "La implementación de Cisco AAA es significativamente disruptiva, ya que los métodos de acceso anteriores se desactivan de inmediato. Por lo tanto, antes de implementar Cisco AAA, la organización debe revisar y planificar cuidadosamente sus criterios de autenticación (inicios de sesión y contraseñas, desafíos y respuestas, y tecnologías de token), métodos de autorización y requisitos de contabilidad"
    #remediacion = "Ejecute el comando 'aaa new-model'"
    #lista_reco = {'descripcion':desc, 'razon':razon,'impacto':impacto,'remediacion':remediacion}        
    #print(lista_reco)
    
    #if (len(aaauth) == 0):
        
    #    print("No esta configurado")
    #    print("Se recomienda configurar el servicio AAA porque XXXXXXXXXX")
    #    print("Para realizarlo debe ejecutar la sentencia: XXXXXXXXXXX")
    #else:
    #    #print(aaauth)
    #    for obj in aaauth:
    #        if "authentication" in obj.text:
    #            print("Tiene configurada authentication")
    #        if "authorization" in obj.text:
    #            print("Tiene configurada authorization")
    #        if "accounting" in obj.text:
    #            print("Tiene configurada accounting")
    #        if "session-id" in obj.text:
    #            print("Tiene configurada session-id")
    #        if "new-model" in obj.text:
    #            print("Tiene configurada new-model")
    return render(request,"LanGuardianCont/configuracion.html", {'cont':contenido, 'nist':reco_nist})

def valtemplate (nist):


    return True

