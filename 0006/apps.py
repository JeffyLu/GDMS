#apps.py

from django.apps import AppConfig


class ProjectConfig(AppConfig):
    name = 'project'
    #app名称
    verbose_name = '课题'
    
#相对应的__init__.py
    
default_app_config = 'project.apps.ProjectConfig'
