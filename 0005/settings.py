#数据库mysql配置
DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'database',
         'USER': 'user',
         'PASSWORD': 'password',
         'HOST': 'localhost',
         'PORT': '3306',
    }
}

#中文环境
LANGUAGE_CODE = 'zh-hans'

#上海时区
TIME_ZONE = 'Asia/Shanghai'

#静态目录设置
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'commonstatic'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')



