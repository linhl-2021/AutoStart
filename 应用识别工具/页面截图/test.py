from selenium import webdriver

# 创建Chrome浏览器实例
driver = webdriver.Chrome()

# 打开页面
url = 'http://example.com'
driver.get(url)

# 截图并保存为example.png
driver.save_screenshot('example.png')

# 关闭浏览器
driver.quit()