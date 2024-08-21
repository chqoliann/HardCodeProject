from django.contrib import admin
from users import models as umodels


admin.site.register(umodels.CustomUser)
admin.site.register(umodels.Balance)
admin.site.register(umodels.Subscription)