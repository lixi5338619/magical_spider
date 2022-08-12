# MagicalSpider Settings

# 隐藏界面
headless_enable = True

# 高匿模式、可能影响创建时间
stealth_enable = True

# 代理设置
proxy = None

# 无痕访问
incognito_enable = False

# 分离模式
detach_enable = False

plugin_enable = False

logging_enable = False


driverpath = './config/chromedriver.exe'

magicalpath = './config/magical.db'

stealth_path = './config/stealth.min.js'

host = '0.0.0.0'

port = 5000

# 让 Selenium 在 Linux 中以有头模式运行
# xvfb-run python3 test.py -s -screen 0 1920x1080x16
