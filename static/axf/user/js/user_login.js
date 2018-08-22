function data_security() {
    // 声明一个变量,获取用户注册时的密码
    var $password = $('#u_password');
    // 让登录的密码加上一层md5,跟用户注册时加上md5的密码保持一致
    $password.val(md5($password.val()));
    return true;

}
