from whatToDoNow.models import Tag, Task, ToDoList, EndUser
from django.contrib import admin

admin.site.register(EndUser)
admin.site.register(ToDoList)
admin.site.register(Task)
admin.site.register(Tag)