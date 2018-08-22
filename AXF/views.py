import uuid

from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.template import loader
from django.urls import reverse

from AXF.models import HomeWheel, HomeNav, HomeMustBuy, HomeShop, HomeMainShow, Foodtype, Goods, UserModel, CartModel

ALL_TYPE = '0'      # 0 代表全部类型
ORDER_TOTAL = '0'   # 0 代表综合排序
PRICE_ASC = '1'     # 1 代表价格升序
PRICE_DESC = '2'    # 2 代表价格降序

def index(request):
    return HttpResponse('必胜.狮子登龙号！！！')


def home(request):
    wheels = HomeWheel.objects.all()
    navs = HomeNav.objects.all()
    mustbuys = HomeMustBuy.objects.all()
    shops = HomeShop.objects.all()
    shops0_1 = shops[0:1]
    shops1_3 = shops[1:3]
    shops3_7 = shops[3:7]
    shops7_11 = shops[7:11]
    mainshows = HomeMainShow.objects.all()
    data = {
        'title': '首页',
        'wheels': wheels,
        'navs': navs,
        'mustbuys': mustbuys,
        'shops0_1': shops0_1,
        'shops1_3': shops1_3,
        'shops3_7': shops3_7,
        'shops7_11': shops7_11,
        'mainshows': mainshows,
    }
    return render(request, 'home/home.html', context=data)


def market(request):
    return redirect(reverse('axf:market_with_params', kwargs={'categoryid': 104749, 'childcid': 0, 'order_rule': 0}))


def market_with_parmas(request, categoryid, childcid, order_rule):
    foodtypes = Foodtype.objects.all()
    if childcid == ALL_TYPE:
        goods_list = Goods.objects.filter(categoryid=categoryid)
    else:
        goods_list = Goods.objects.filter(categoryid=categoryid).filter(childcid=childcid)
    foodtype = Foodtype.objects.get(typeid=categoryid)
    '''
        order_rule
            0   代表综合排序
            1   代表价格升序
            2   代表价格降序
            3   代表竞价排名
    '''
    if order_rule == ORDER_TOTAL:
        pass
    elif order_rule == PRICE_ASC:
        goods_list = goods_list.order_by('price')
    elif order_rule == PRICE_DESC:
        goods_list = goods_list.order_by('-price')
    '''
        全部类型：0#进口水果：110 #国产水果：120
    '''
    childtypenames = foodtype.childtypenames
    '''
        [全部类型：0, 进口水果：110, 国产水果:120]
    '''
    childtypename_list = childtypenames.split('#')
    '''
        [[全部类型, 0], [进口水果, 1], [国产水果, 2]]
    '''
    child_type_list = []
    for childtypename in childtypename_list:
        child_type_list.append(childtypename.split(':'))
    data = {
        'title': '闪购',
        'foodtypes': foodtypes,
        'goods_list': goods_list,
        'categoryid': int(categoryid),
        'child_type_list': child_type_list,
        'childcid': childcid,
        'order_rule': order_rule,
    }
    return render(request, 'market/market.html', context=data)


def cart(request):
    data = {
        'title': '购物车',

    }
    return render(request, 'cart/cart.html', context=data)


def mine(request):
    is_login = False
    # 获取用户登录信息
    user_id = request.session.get('user_id')
    data = {
        'title': '我的',
        'is_login': is_login,
    }
    if user_id:
        is_login = True
        # 为获取图片,需要获取数据库中的user_id
        user = UserModel.objects.get(pk=user_id)
        data['is_login'] = is_login
        # 获取图像,需要添加他存图片的路径+数据库中的图片前面的icon
        data['user_icon'] = '/static/upload/' + user.u_icon.url
        # 获取用户名
        data['username'] = user.u_name

    return render(request, 'mine/mine.html', context=data)

# 实现更能： 用户注册
def user_register(request):
    if request.method == 'GET':
        data = {
            'title': '用户注册'
        }
        return render(request, 'user/user_register.html', context=data)
    elif request.method == 'POST':
        username = request.POST.get('u_name')
        password = request.POST.get('u_password')
        email = request.POST.get('u_email')
        icon = request.FILES.get('u_icon')
        print(password)

        user = UserModel()
        user.u_name = username
        user.u_email = email
        user.u_icon = icon
        # 封装，设置密码
        user.set_password(password)
        user.save()
        # 实现自动登录,把用户的唯一标识存到session里,
        # 用的时候拿user.id跟session里的user_id进行对比.
        request.session['user_id'] = user.id
        # 邮箱
        send_mail_learn(username, email, user.id)
        return redirect(reverse('axf:mine'))

# 实现功能： 退出用户登录
def user_logout(request):
    # 删除session中的数据
    request.session.flush()
    return redirect(reverse('axf:mine'))

# 实现功能： 点击输入框进行输入,输完之后如果数据库中有想对应,有进行提示重复,反之,可用
def check_user(request):
    # 客户端想服务端输入数据,用GET方法,获取到输入的u_name
    username = request.GET.get('u_name')
    # 获取到u_name,然后从数据库中filter进行过滤筛选,
    users = UserModel.objects.filter(u_name=username)
    data = {
        'status': '200',
        'msg': 'ok',
    }
    # 进行判断,如果用户名存在,就返回用户名已存在,反之,可用
    if users.exists():
        data['status'] = '801'
        data['msg'] = 'already exists'
    else:
        data['msg'] = 'can use'

    return JsonResponse(data)

# 实现功能：邮箱校验
def check_email(request):
    email = request.GET.get('u_email')
    users = UserModel.objects.filter(u_email=email)
    data = {
        'status': '200',
        'msg': 'ok',
    }
    if users.exists():
        data['status'] = '801'
        data['msg'] = 'already exists'
    else:
        data['msg'] = 'can use'
    return JsonResponse(data)

# 实现功能：用户登录页面
def user_login(request):
    if request.method == 'GET':
        msg = request.session.get('msg')
        data = {
            'title': '用户登录',
            'msg': msg,
        }
        return render(request, 'user/user_login.html', context=data)
    # 当用户用POST方法请求时
    elif request.method == 'POST':
        # 服务端接收到用户请求登录的姓名.密码
            username = request.POST.get('u_name')
            password = request.POST.get('u_password')
            # 服务端拿客户端用户登录跟数据库中的进行匹配
            users = UserModel.objects.filter(u_name=username)
            # 如果用户存在
            if users.exists():
                # 用户只能是一个
                user = users.first()

                # 如果用户密码验证通过
                if user.cherk_password(password):
                    if not user.is_active:
                        request.session['msg'] = '用户未激活'
                        return redirect(reverse('axf:user_login'))
                    # 用户登录请求时,携带的session【user_id】= 数据库中的注册时生成的session【user.id】
                    request.session['user_id'] = user.id
                    # 验证通过,登录成功
                    return redirect(reverse('axf:mine'))
                else:
                    # 密码错误
                    request.session['msg'] = '密码错误'
                    return redirect(reverse('axf:user_login'))
            else:
                # 用户不存在
                request.session['msg'] = '用户不存在'
                return redirect(reverse('axf:user_login'))

# 实现功能,测试邮箱
'''
激活
    能找到用户的方式
        -根据用户的唯一标识
    修改用户的状态
'''


def send_mail_learn(username, email, userid):
    # 邮箱的标题
    subject = '爱鲜蜂VIP激活邮件'
    # 邮箱的内容
    message = ''
    # 收件人
    recpient_list = [email]
    # 获取模板
    temp = loader.get_template('user/user_active.html')
    token = str(uuid.uuid4())
    cache.set(token, userid, timeout=60*60)
    data = {
        'username': username,
        'active_url': 'http://127.0.0.1:8003/axf/activeuser/?utoken%s' % token,
    }
    # 渲染模板
    html = temp.render(data)
    # 发送
    send_mail(subject, message, 'amazing_awm@sina.com', recpient_list, html_message=html)

# 实现更能,用户激活
def active_user(request):
    # 用GET方法获取用户的userid
    user_token = request.GET.get('utoken')
    user_id = cache.get(user_token)
    cache.delete(user_token)
    if not user_id:
        return HttpResponse('激活已过期,请重新申请激活邮件')
    # 跟数据库进行匹配查询
    user = UserModel.objects.get(pk=user_id)
    # 修改激活状态
    user.is_active = True
    user.save()
    return HttpResponse('用户激活成功')

# 实现功能： 闪购向购物车添加商品
def add_to_cart(request):
    goodsid = request.GET.get('goodsid')
    userid = request.session.get('user_id')
    print(goodsid)
    data = {
        'status': '200',
        'msg': 'ok',
    }
    # 没有登录进行页面跳转登录
    if not userid:
        data['status'] = '302'
        data['msg'] = 'not login'
    else:
        # 购物数据添加
        goods = Goods.objects.get(pk=goodsid)
        user = UserModel.objects.get(pk=userid)
        cartmodels = CartModel.objects.filter(c_goods=goods).filter(c_user=user)

        # cartmodels = CartModel.objects.filter(c_goods_id=goodsid).filter(c_user_id=userid)
        # 如果商品存在进行添加操作
        if cartmodels.exists():
            cartmodel = cartmodels.first()
            cartmodel.c_goods_num = cartmodel.c_goods_num + 1
            cartmodel.save()
       # 没有进行创建操作
        else:
            cartmodel = CartModel()
            cartmodel.c_goods = goods
            cartmodel.c_user = user
            cartmodel.save()
        # 执行完,将数据返回给前端
        data['goods_num'] = cartmodel.c_goods_num

    return JsonResponse(data)