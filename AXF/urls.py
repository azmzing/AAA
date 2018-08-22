from django.conf.urls import url

from AXF import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^home/', views.home, name='home'),
    url(r'^market/', views.market, name='market'),
    url(r'^marketwithparams/(?P<categoryid>\d+)/(?P<childcid>\d+)/(?P<order_rule>\d+)/', views.market_with_parmas, name='market_with_params'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^mine/', views.mine, name='mine'),
    url(r'^userregister/', views.user_register, name='user_register'),
    url(r'^userlogout/', views.user_logout, name='user_logout'),
    url(r'^checkuser/', views.check_user, name='check_user'),
    url(r'^checkemail/', views.check_email, name='check_email'),
    # 点击'我的'中的未登录,实现跳转
    url(r'^userlogin/', views.user_login, name='user_login'),
    # 激活邮箱
    url(r'^activeuser/', views.active_user, name='active_user'),
    # 购物车添加商品
    url(r'^addtocart/', views.add_to_cart, name='add_to_cart'),
]