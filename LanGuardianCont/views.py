from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.template import Context
from .forms import formularioCont
from fabric import Connection
from ciscoconfparse import CiscoConfParse
from io import open

# Create your views here.

def contacto(request):
    formu_cont=formularioCont()
    if request.method=="POST":
        formu_cont=formularioCont(data=request.POST)
        if formu_cont.is_valid():
            ip=request.POST.get("ip")
            puerto=request.POST.get("puerto")
            usuario=request.POST.get("usuario")
            clave=request.POST.get("clave")
            #f = open("config.txt", "w")
            #c = Connection(host=usuario + "@" + ip, connect_kwargs={"password":clave}, port=puerto)
            #f.write(str(c.run('cat pepe.txt')))
            #f.close()

            try: 
                c.run()
                return redirect("/contacto/?valido")
            except:
                return redirect("/contacto/?invalido")

    return render(request,"LanGuardianCont/contacto.html", {'miform':formu_cont})

def configuracion(request):
    f = open("config.txt", "r",encoding='utf-8')
    contenido = f.read()
    f.close()    
    parse = CiscoConfParse("config.txt")
    p1 = parse.find_objects(r"^aaa new-model")

    if (len(p1) == 0):
        desc = "Habilite el sistema de control de acceso AAA"
        razon = "Los servicios de autenticación, autorización y contabilidad (AAA) proporcionan una fuente autorizada para administrar y monitorear el acceso de los dispositivos. La centralización del control mejora la coherencia del control de acceso, los servicios a los que se puede acceder una vez autenticados y la responsabilidad mediante el seguimiento de los servicios a los que se accede. Además, la centralización del control de acceso simplifica y reduce los costos administrativos de aprovisionamiento y desaprovisionamiento de cuentas, especialmente cuando se administra una gran cantidad de dispositivos"
        impacto = "La implementación de Cisco AAA es significativamente disruptiva, ya que los métodos de acceso anteriores se desactivan de inmediato. Por lo tanto, antes de implementar Cisco AAA, la organización debe revisar y planificar cuidadosamente sus criterios de autenticación (inicios de sesión y contraseñas, desafíos y respuestas, y tecnologías de token), métodos de autorización y requisitos de contabilidad"
        remediacion = "Ejecute el comando 'aaa new-model'"
        lista_reco = {'descripcion':desc, 'razon':razon,'impacto':impacto,'remediacion':remediacion}        
    print(lista_reco)
    
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
    return render(request,"LanGuardianCont/configuracion.html", {'cont':contenido, 'lis':lista_reco})