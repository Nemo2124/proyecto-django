from django.shortcuts import render
from .models import Alumnos
from .forms import ComentarioContactoForm
from .models import ComentarioContacto
from django.shortcuts import get_object_or_404
import datetime
from .models import Archivos
from .forms import FormArchivos
from django.contrib import messages

# Create your views here.
def principal(request):
    alumnos = Alumnos.objects.all()
#all recupera todos los objetos del modelo ( registros de la tabla alumnos)

    return render(request, "registros/principal.html", {'8A':alumnos})
#Indicamos el lugar donde se rendirizará el resultado de esta vista

def registrar(request): 
    if request.method == 'POST':
        form = ComentarioContactoForm(request.POST)
        if form.is_valid(): #Si los datos recibidos son correctos
            form.save() #inserta
            mensaje = ComentarioContacto.objects.all()
            return render (request, 'registros/consulta.html', {'comentarios':mensaje})
        form = ComentarioContactoForm()
        #Si algo sale mal se reenvian al formulario los datos ingresados
        return render(request, 'registros/contacto.html', {'form':form})
    
def contacto(request):
    return render (request, "registros/contacto.html")
    #Indicamos el lugar donde se rendizará el resultado  de esta vista

def consulta(request):
    mensaje = ComentarioContacto.objects.all()
#all recupera todos los objetos del modelo ( registros de la tabla alumnos)
    return render(request, "registros/consulta.html", {'comentarios':mensaje})
#Indicamos el lugar donde se rendirizará el resultado de esta vista

def eliminarComentario(request, id,
        confirmacion='registros/confirmarEliminacion.html'):
        comentario = get_object_or_404(ComentarioContacto, id=id)
        if request.method=='POST':
             comentario.delete()
             mensaje=ComentarioContacto.objects.all()
             return render (request, "registros/consulta.html",
                            {'comentarios':mensaje})       
        return render(request, confirmacion, {'comentario':comentario})
    
def consultarComentarioIndividual(request, id):
     comentario=ComentarioContacto.objects.get(id=id)
     #get permite establecer una condicionante a la consulta y recupera el objeto
     #del modelo que cumple la condicion  (registro de la tabla ComentariosContacto)
     #get se emplea cuando se sabe que solo hay un onjeto que coincidde con su consulta.
     return render(request, "registros/formEditarComentario.html",
            {'comentario':comentario})
    #Indicamos el lugar donde se rendizara el resultado de esta vista 
    #y enviamos a la lista de comentarios recuperados

def editarComentarioContacto(request, id):
     comentario = get_object_or_404(ComentarioContacto, id=id)
     form =ComentarioContactoForm(request.POST, instance=comentario)
     #Referenciamos que el elemento del formulario pertenece al comentario ya existente
     if form.is_valid():
            form.save() #si el registro ya existe, se modifica.
            comentarios = ComentarioContacto.objects.all()
            return render(request, "registros/consulta.html",
                    {'comentarios':comentarios})
     #si el formulario no es valido nos regresa al formulario para verificar datos
     return render(request, "registros/formEditarComentario.html",
            {'comentario':comentario})

#Funcion FILTER
#filter nos retornará los registros que coinciden con los parametros de busqueda dados
def consultar1(request):
     #con una sola condicion
     alumnos=Alumnos.objects.filter(carrera="TI")
     return render(request, "registros/consultas.html", {'8A': alumnos})

def consultar2(request):
     #con 2 condiciones
     alumnos=Alumnos.objects.filter(carrera="TI").filter(turno="Matutino")
     return render(request, "registros/consultas.html", {'8A': alumnos})

def consultar3(request):
     #si solo deseamos recuperar ciertos datos agregamos la función only,
     #listando los campos que queremos obtener de la consulta emplear filter()
     #o en el ejemplo all()
     alumnos=Alumnos.objects.all().only("matricula", "nombre",
     "carrera", "turno", "imagen")
     return render(request, "registros/consultas.html", {'8A': alumnos})

def consultar4(request):
     alumnos=Alumnos.objects.filter(turno__contains="Vesp")
     return render(request, "registros/consultas.html", {'8A': alumnos})

def consultar5(request):
     alumnos=Alumnos.objects.filter(nombre__in=["Juan", "Ana"])
     return render(request, "registros/consultas.html", {'8A': alumnos})

def consultar6(request):
     fechaInicio = datetime.date(2026, 3, 13)
     fechaFin = datetime.date(2026, 3, 14)
     alumnos=Alumnos.objects.filter(created__range=(fechaInicio, fechaFin))
     return render(request, "registros/consultas.html", {'8A': alumnos})

def consultar7(request):
     alumnos=Alumnos.objects.filter(comentario__coment__contains='No inscrito')
     return render(request, "registros/consultas.html", {'8A': alumnos})

def archivos(request):
     if request.method == 'POST':
          form = FormArchivos(request.POST, request.FILES)
          if form.is_valid():
               titulo = request.POST['titulo']
               descripcion = request.POST['descripcion']
               archivo = request.FILES['archivo']
               insert = Archivos(titulo=titulo, descripcion=descripcion, archivo=archivo)
               insert.save()
               return render(request, "registros/archivos.html")
          else:
               messages.error(request, "Error al procesar el formulario")
     else:
          return render(request, "registros/archivos.html", {'archivo':Archivos})
     
def consultasSQL(request):
     alumnos=Alumnos.objects.raw('SELECT id, matricula, nombre, carrera, turno, imagen FROM registros_alumnos WHERE carrera="TI" ORDER BY turno DESC')
     return render(request, "registros/consultas.html", {'8A':alumnos})