$(function () {
    // 全部类型
    $('#all_type').click(function () {
        console.log('全部类型');
        $('#all_type_container').show();
        $(this).find('span').find('span').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
        //  点击全部类型的时候综合排序的下拉框收上去
        $("#sort_rule_container").slideUp();
        $('#sort_rule').find('span').find('span').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down')
    });

    $('#all_type_container').click(function () {
        $(this).hide();
        $('#all_type').find('span').find('span').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');

    });
    // 综合排序
    $("#sort_rule").click(function () {
        console.log('排序规则');
        $("#sort_rule_container").show();
        $(this).find('span').find('span').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
        //  点击综合排序的时候全部类型的下拉框收上去
        $("#all_type_container").hide();
        $('#all_type').find('span').find('span').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');

    });

    $("#sort_rule_container").click(function () {
        $(this).slideUp();
        $('#sort_rule').find('span').find('span').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
    });
    // 购物车增删商品
    $('.addShopping').click(function () {
        // 获取属性 提供两种方式  attr  prop
        // attr 可以获取任意属性, prop只能获取内置属性
        var $addShopping = $(this);
        var goodsid = $addShopping.attr('goodsid');
        console.log(goodsid);
        $.getJSON('/axf/addtocart/', {'goodsid': goodsid}, function (data) {
            console.log(data);
            if (data['status'] == '200'){
                var goods_num = data['goods_num'];
                // 设置上一个元素进行添加prev
                $addShopping.prev().html(goods_num)
            }else if(data['status'] == '302'){
                window.open('/axf/userlogin/', target='_self')
            }
        })

    });
    $('.subShopping').click(function () {

    })
});