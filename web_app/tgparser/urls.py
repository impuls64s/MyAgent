from django.urls import path


from . import views

urlpatterns = [
    path('', views.tables_view, name="tables_view"),
    path('delete/', views.del_table, name="del_table"),
    
    path('<int:table_id>/phrases/', views.phrases_view, name='phrases_view'),
    path('phrases/<int:phrase_id>/update', views.upd_phrase, name='upd_phrase'),
    path('phrases/<int:phrase_id>/delete', views.del_phrase, name='del_phrase'),

    path('chat_messages/', views.view_messages, name='view_messages'),
    path('msg_detail/<int:msg_id>/', views.msg_detail, name='msg_detail'),
    path('blocked_users/', views.view_blocked_users, name='view_blocked_users'),
    path('del_blocked_user/<int:usr_id>', views.del_blocked_user, name='del_blocked_user'),

    path('control/<int:bot_id>/', views.bot_control, name='bot_control'),

    
    path('bots/', views.view_bots, name='view_bots'),
    path('create/', views.create_bot, name='create_bot'),
    path('edit/<int:bot_id>/', views.edit_bot, name='edit_bot'),
    path('delete/<int:bot_id>/', views.del_bot, name='del_bot'),
    path('send_code/<int:bot_id>/', views.send_code, name='send_code'),
    path('activate/<int:bot_id>/', views.activate_bot, name='activate'),
]