"""sudoku URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('solver/', views.solver_index, name='solver index'),
    path('solver/update_setting', views.update_setting, name='update setting'),
    path('solver/get_next_step', views.get_next_step, name='get next step'),
    path('solver/generate_sudoku', views.generate_sudoku, name='generate sudoku'),
    path('solver/check_solvability', views.check_solvability, name='check solvability'),
    path('solver/edit_jigsaw_shape', views.edit_jigsaw_shape, name='edit jigsaw shape'),
    path('solver/<name>', views.solver, name='solver'),
    path('guides/', views.guides_index, name='guide index'),
    path('guides/<name>', views.detail, name='detail'),
]
