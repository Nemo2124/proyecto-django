from django.contrib import admin
from .models import Alumnos
from .models import Comentario
from .models import ComentarioContacto

# Register your models here.
class AdministrarModelo(admin.ModelAdmin):
    readonly_fields = ('created', 'updated')
    list_display = ('matricula', 'nombre', 'carrera', 'turno', 'created')
    search_fields = ('matricula', 'nombre', 'carrera', 'turno')
    date_hierarchy = 'created'
    list_filter = ('carrera', 'turno')

    def get_readonly_fields(self, request, obj=None):
        #si el usuario pertenece al grupo de permisos "Usuario"
        if request.user.groups.filter(name="permisos" ).exists():
            #Bloquea los campos
            return('matricula', 'turno')
        #cualquier otro usuario que no pertenece al grupo "Usuario"
        else: 
            #Bloquea solo los campos
            return('created', 'updated')

admin.site.register(Alumnos, AdministrarModelo)

class AdministrarComentarios(admin.ModelAdmin):
    list_display = ('id', 'coment')
    search_fields = ('id', 'created')
    date_hierarchy = 'created'
    readonly_fields = ('created', 'id')

admin.site.register(Comentario, AdministrarComentarios)

class AdministrarComentariosContacto(admin.ModelAdmin):
    list_display = ('id', 'mensaje')
    search_fields = ('id', 'created')
    date_hierarchy = 'created'
    readonly_fields = ('created', 'id')

admin.site.register(ComentarioContacto, AdministrarComentariosContacto)