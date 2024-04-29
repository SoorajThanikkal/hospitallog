# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import reg,drreg,breg,lreg,pay,labservice,lbreg,labpay,Bookdoctor


# Register your models here.

admin.site.register(reg)
admin.site.register(drreg)
admin.site.register(breg)
admin.site.register(lreg)
admin.site.register(pay)
admin.site.register(labservice)
admin.site.register(lbreg)
admin.site.register(labpay)
admin.site.register(Bookdoctor)