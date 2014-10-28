__author__ = 'couldtt'

DEBUG = True

config = {
    'duokan': {
        'platform_name': '多看',
        'url': 'http://www.duokan.com',
    },

    'taobao': {
        'platform_name': '淘宝',
        'url': 'http://ebook.taobao.com',
        'remark': '淘宝限免电子书电脑端只能在10:00~11:00领取，使用手机客户端领取时间到次日9点'
    },

    'dangdang': {
        'platform_name': '当当',
        'url': 'http://e.dangdang.com',
        'ajax_url': 'http://e.dangdang.com/Standard/Framework/Core/hosts/ajax_api.php?isajax=1&page_id=14456&component_map_id=74284&domain=shuzi.dangdang.com&path_name=index&areaid=0&page_type=3&areatype=0&static_type=0&mix=1&domain_flag=1'
    },
}

crawl_container = ['duokan', 'taobao', 'dangdang']
debug_container = ['duokan', 'taobao', 'dangdang']