from django.conf.urls import url
from scholarsys import views

urlpatterns = [
    # main page
    url(r'^home', views.home, name='home'),
    url(r'^login', views.login, name='login'),
    url(r'^logout', views.logout_view, name='logout'),
    url(r'^signup', views.signup, name='signup'),
    url(r'^media',views.add_achievement,name='media'),

    # achievement
    url(r'^achievement/$', views.manage_achievement, name='achievement'),
    url(r'^achievement/add_achievement', views.add_achievement, name='add_achievement'),
    url(r'^achievement/delete_achievement', views.delete_achievement, name='delete_achievement'),
    url(r'^achievement/verify_achievement', views.verify_achievement, name='verify_achievement'),

    # scholarship
    url(r'^scholarship/$', views.manage_scholarship, name='scholarship'),
    url(r'^scholarship/cancle_scholarship', views.cancel_scholarship, name='cancel_scholarship'),
    url(r'^scholarship/add_scholarship', views.add_scholarship, name='add_scholarship'),
    url(r'^scholarship/apply_scholarship', views.apply_scholarship, name='apply_scholarship'),
    url(r'^scholarship/delete_scholarship', views.delete_scholarship, name='delete_scholarship'),
    # Generate Report
    url(r'^generate_report', views.generate_report, name='generate_Report'),
    url(r'^$', views.home, name='home'),
]
