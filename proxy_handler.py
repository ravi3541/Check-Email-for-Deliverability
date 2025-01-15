class ProxyHandler:
    proxies = [
        # {"host": "195.3.220.223", "port": 9300},  # Example free proxy
        {"host": "195.3.223.88", "port": 1080},
        {"host": "108.181.11.193", "port": 3128},
    ]
    current_index = 0

    @classmethod
    def get_proxy(cls):
        print('getting proxy')
        proxy = cls.proxies[cls.current_index]
        print(f'got proxy  = {proxy}')
        cls.current_index = (cls.current_index + 1) % len(cls.proxies)
        print(f'cls.current_index = {cls.current_index}')
        return proxy
