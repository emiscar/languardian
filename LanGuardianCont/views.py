from django.shortcuts import render, redirect
from fabric import Connection
from ciscoconfparse import CiscoConfParse
from io import open
import logging, os, io
import pandas as pd
import telnetlib

from django.views.generic import TemplateView
from .models import Dispositivo
from .forms import DispositivoFormSet

from django.urls import reverse
from urllib.parse import urlencode

from django.http import FileResponse, response
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from django.views.generic import View

# VISTA DE CLASE PARA GENERAR EL FORMULARIO DE 1 O MAS DISPOSITIVOS, CONECTARSE Y ALMACENAR LAS CONFIG
class DispositivosView(TemplateView):
    model = Dispositivo
    template_name = "LanGuardianCont/analisis.html"

    def get(self, *args, **kwargs):

        # Elimino los archivos de configuración y pdf al volver a la página de análisis
        #test = os.listdir()
        #for item in test:
        #    if item.endswith(".txt") || item.endswith(".pdf"):
        #        os.remove(item)

        # Creo la instancia del formulario
        formset = DispositivoFormSet(queryset=Dispositivo.objects.none())
        return self.render_to_response({'miform': formset})

    def post(self, *args, **kwargs):

        formset = DispositivoFormSet(data=self.request.POST)
        
        # Chequeo si los datos en los formularios son válidos
        if formset.is_valid():
            i=0
            for formu in formset:
                cd = formu.cleaned_data
                lip = cd.get('ip')
                lpuerto = cd.get('puerto')
                lusuario = cd.get('usuario')
                lclave = cd.get('clave')
                lproto = cd.get('protocolo')
                #DESMARCANDO ESTE IF/ELSE Y HABILITANDO LA LINEA 59 PUENTEO EL ESCANEO DE DISPOSITIVOS
                #if lproto == '1':
                    #res = con_telnet(lip,lpuerto,lusuario,lclave,i)
                #else:
                    #res = con_ssh(lip,lpuerto,lusuario,lclave,i)
                i=i+1
            res = True

            # VALIDO SI HUBO PROBLEMAS DE CONEXION
            if res == True:
                base_url = reverse('Config')
                query_string =  urlencode({'cant_dispo': i})
                url = '{}?{}'.format(base_url, query_string)
                return redirect(url)
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

# MÉTODO PARA CONEXIÓN POR SSH
def con_ssh(ip, puerto, usuario, clave, id):
    logging.info('connection attempt {}'.format(0))
    c = Connection(host=usuario + "@" + ip, connect_kwargs={"password":clave}, port=puerto)
    try:
        c.run('cat pepe.txt')
        f = open("config"+str(id)+".txt", "w", encoding='utf-8')
        f.write(str(c.run('cat pepe.txt')))
        f.close()
        return True
    except Exception as ex:
        print(str(ex))
        return (str(ex))

# MÉTODO PARA CONEXIÓN POR TELNET
def con_telnet(ip, puerto, usuario, clave, id):
    logging.info('connection attempt {}'.format(0))
    try:
        tn = telnetlib.Telnet(ip,puerto)
        tn.read_until(b"login: ")
        tn.write(usuario.encode('ascii') + b"\n")
        if clave:
            tn.read_until(b"Password: ")
            tn.write(clave.encode('ascii') + b"\n")
            f = open("temp.txt", "w", encoding='utf-8')
            tn.write(b"cat pepe.txt\n")
            tn.write(b"exit\n")            
            f.write(str(tn.read_all().decode('ascii')))
            f.close()
            
            # EDITO EL ARCHIVO PARA QUITAR LINEAS VACIAS Y DE COMANDOS
            a_file = open("temp.txt", "r+", encoding='utf-8')
            lines=a_file.readlines()
            a_file.seek(0)
            a_file.truncate()
            a_file.writelines(lines[10:-5])
            a_file.close()
            a_file = open("temp.txt", "r", encoding='utf-8')
            new_file = open("config"+str(id)+".txt", "w", encoding='utf-8')
            for line in a_file:
                if not line.strip(): continue
                new_file.write(line)
            
            a_file.close()
            new_file.close()
            os.remove("temp.txt")

            return True
    except Exception as ex:
        print(str(ex))
        return (str(ex))

# VISTA PARA MOSTRAR LAS CONFIGURACIONES Y RECOMENDACIONES, GENERAR REPORTES PDF
def configuracion(request):
    cont_demas = []
    reco_d =[]
    reco_demas = []
    reco_uno = []
    nist_uno = []
    nist_demas = []
    buep_uno = []
    buep_demas = []
    c_dispo = request.GET.get('cant_dispo')
    print(c_dispo)
    ## GUARDO LA CONFIG PARA PASARLA A LA WEB ##
    for i in range(int(c_dispo)):
        if i == 0:
            f = open("config"+str(i)+".txt", "r",encoding='utf-8')
            cont_uno=f.read()
            f.close()
            ## UTILIZO CONFPARSE ##
            parse = CiscoConfParse("config"+str(i)+".txt")
            ## LEO TEMPLATE NIST ##
            df = pd.read_excel("NIST.xlsx", sheet_name="NIST", header=0, na_values="NaN")
            ## MATCHEO CADA FILA DEL NIST CONTRA LA CONFIG ##            
            for index, row in df.iterrows():
                comando = df.iloc[index, 0]
                #print(eval(comando))
                if len(eval(comando)) == 0:
                    if (df.iloc[index, 7] == 1):
                        reco_uno.append(row[1:7])
                        print("Entre 1")
                    elif (df.iloc[index, 7] == 2):
                        nist_uno.append(row[1:7])
                        print("Entre 2")
                    else:
                        buep_uno.append(row[1:7])
                        print("Entre 3")
            #LLAMO AL METODO PARA GENERAR PDF
            reporgen (0, reco_uno)
        else:
            f = open("config"+str(i)+".txt", "r",encoding='utf-8')
            cont_demas.append (f.read())
            f.close()
            ## UTILIZO CONFPARSE ##
            parse = CiscoConfParse("config"+str(i)+".txt")
            ## LEO TEMPLATE NIST ##
            df = pd.read_excel("NIST.xlsx", sheet_name="NIST", header=0, na_values="NaN")
            ## MATCHEO CADA FILA DEL NIST CONTRA LA CONFIG ##
            for index, row in df.iterrows():
                comando = df.iloc[index, 0]
                #print(eval(comando))
                if len(eval(comando)) == 0:
                    if (df.iloc[index, 7] == 1):
                        reco_demas.append(row[1:7])
                        print("R_demas "+str(index)+" con ")
                        print(reco_demas)
                    elif (df.iloc[index, 7] == 2):
                        nist_demas.append(row[1:7])
                    else:
                        buep_demas.append(row[1:7])
            reco_d.append(reco_demas)
            #LLAMO AL METODO PARA GENERAR PDF
            reporgen (i, reco_demas)
        print("RECO D)")
        print (reco_d)
    return render(request,"LanGuardianCont/configuracion.html", {'cont_demas':cont_demas, 'reco_demas':reco_d, 'cant':int(c_dispo), 'cont_uno':cont_uno, 'reco_uno':reco_uno, 'nist_uno':nist_uno, 'buep_uno':buep_uno})

# METODO QUE GENERA LOS PDF
def reporgen (indi, recos):
    import time
    from reportlab.lib.enums import TA_JUSTIFY
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    doc = SimpleDocTemplate("config"+str(indi)+".pdf",pagesize=A4,rightMargin=36,leftMargin=36,topMargin=36,bottomMargin=36)
    Story=[]
    logo = "L13.png"
    tit1 = "RECOMENDACIONES"
    tit2 = "COMPLIANCE NIST"
    tit3 = "BUENAS PRACTICAS"
    magName = "Pythonista"
    issueNum = 12
    subPrice = "99.00"
    limitedDate = "03/05/2010"
    freeGift = "tin foil hat"
    formatted_time = "Reporte generado el "+time.ctime()+" para el dispositivo XXXXX"
    full_name = "Mike Driscoll"
    address_parts = ["411 State St.", "Marshalltown, IA 50158"]
    im = Image(logo, width=300, height=50)
    #Agrego el logo
    Story.append(im)
    #Agrego un espacio
    Story.append(Spacer(1, 24))
    
    styles=getSampleStyleSheet()    
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY))
    #Titulo recom
    Story.append(Paragraph(tit1, styles["Heading2"]))
    Story.append(Spacer(1, 12))
    #Tabla recomendaciones

    Story.append(Spacer(1, 12))
    #Titulo Nist
    Story.append(Paragraph(tit2, styles["Heading2"]))
    Story.append(Spacer(1, 12))
    #Tabla Nist

    Story.append(Spacer(1, 12))
    #Titulo BuePrac
    Story.append(Paragraph(tit3, styles["Heading2"]))
    Story.append(Spacer(1, 12))
    #Tabla BuePrac

    Story.append(Spacer(1, 12))
    ptext = '%s' % formatted_time
    Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 12))
    # Create return address
    #ptext = '%s' % full_name
    #Story.append(Paragraph(ptext, styles["Normal"]))       
    #for part in address_parts:
    #    ptext = '%s' % part.strip()
    #    Story.append(Paragraph(ptext, styles["Normal"]))   
    #Story.append(Spacer(1, 12))
    #ptext = 'Dear %s:' % full_name.split()[0].strip()
    #Story.append(Paragraph(ptext, styles["Normal"]))
    #Story.append(Spacer(1, 12))
    ptext = 'Lan Guardian solo emite recomendaciones de configuración de dispositivos de red en base \
            a las buenas prácticas del Marco de Ciberseguridad del NIST \
            (https://www.nist.gov). \
            La implementación de dichas recomendaciones corre por cuenta del usuario y Lan Guardian no se responsabiliza por el \
            impacto que generen sobre la empresa'
    #ptext = 'We would like to welcome you to our subscriber base for %s Magazine! \
    #        You will receive %s issues at the excellent introductory price of $%s. Please respond by\
    #        %s to start receiving your subscription and get the following free gift: %s.' % (magName, 
    #                                                                                                issueNum,
    #                                                                                                subPrice,
    #                                                                                                limitedDate,
    #                                                                                                freeGift)
    Story.append(Paragraph(ptext, styles["Justify"]))
    #Story.append(Spacer(1, 12))
    #ptext = 'Thank you very much and we look forward to serving you.'
    #Story.append(Paragraph(ptext, styles["Justify"]))
    #Story.append(Spacer(1, 12))
    #ptext = 'Sincerely,'
    #Story.append(Paragraph(ptext, styles["Normal"]))
    #Story.append(Spacer(1, 48))
    #ptext = 'Ima Sucker'
    #Story.append(Paragraph(ptext, styles["Normal"]))
    #Story.append(Spacer(1, 12))
    doc.build(Story)

# METODO PARA DESCARGAR EL PDF DESDE EL FRONT
def reporte (request):
     
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=A4, bottomup=0)


    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, "Hello world.")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')