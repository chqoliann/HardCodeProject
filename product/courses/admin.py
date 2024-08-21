from django.contrib import admin
from courses import models as cmodels


admin.site.register(cmodels.Course)
admin.site.register(cmodels.Group)
admin.site.register(cmodels.Lesson)


