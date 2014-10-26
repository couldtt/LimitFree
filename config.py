__author__ = 'couldtt'

DEBUG = True

config = {
    'duokan': {
        'url': 'www.duokan.com',
    },

    'taobao': {
        'url': 'ebook.taobao.com',
    },

    'dangdang': {
        'url': 'e.dangdang.com',
        'ajax_url': 'http://e.dangdang.com/Standard/Framework/Core/hosts/ajax_api.php?isajax=1&page_id=14456&component_map_id=74284&domain=shuzi.dangdang.com&path_name=index&areaid=0&page_type=3&areatype=0&static_type=0&mix=1&domain_flag=1'
    },
}

crawl_container = ['dangdang', 'duokan', 'taobao']
debug_container = ['duokan', 'dangdang', 'taobao']