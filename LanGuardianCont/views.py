from django.shortcuts import render, redirect
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
            f = open("config.txt", "w")
            c = Connection(host=usuario + "@" + ip, connect_kwargs={"password":clave}, port=puerto)
            f.write(str(c.run('cat pepe.txt')))
            f.close()
            parse = CiscoConfParse("config.txt")
            aaauth = parse.find_objects(r"^aaa")
    
            if (len(aaauth) == 0):
                print("No esta configurado")
                print("Se recomienda configurar el servicio AAA porque XXXXXXXXXX")
                print("Para realizarlo debe ejecutar la sentencia: XXXXXXXXXXX")
            else:
                #print(aaauth)
                for obj in aaauth:
                    if "authentication" in obj.text:
                        print("Tiene configurada authentication")
                    if "authorization" in obj.text:
                        print("Tiene configurada authorization")
                    if "accounting" in obj.text:
                        print("Tiene configurada accounting")
                    if "session-id" in obj.text:
                        print("Tiene configurada session-id")
                    if "new-model" in obj.text:
                        print("Tiene configurada new-model")

            try: 
                c.run()
                return redirect("/contacto/?valido")
            except:
                return redirect("/contacto/?invalido")

    return render(request,"LanGuardianCont/contacto.html", {'miform':formu_cont})