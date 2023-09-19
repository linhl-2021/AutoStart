import requests
import pytesseract
from PIL import Image
# 登录页面的URL地址
login_url = "https://example.com/login"
# 获取验证码的URL地址
captcha_url = "https://example.com/captcha"
# 会话对象，用于保持登录状态
session = requests.Session()
# 获取登录页面，获取cookie等信息
response = session.get(login_url)
# 获取验证码图片
captcha_response = session.get(captcha_url, stream=True)
# 保存验证码图片
with open("captcha.png", "wb") as f:
    for chunk in captcha_response.iter_content(chunk_size=128):
        f.write(chunk)
# 使用PIL库打开验证码图片
captcha_image = Image.open("captcha.png")
# 使用pytesseract库识别验证码
captcha_text = pytesseract.image_to_string(captcha_image)
# 提交登录请求，包括用户名、密码和验证码
payload = {"username": "your_username", "password": "your_password", "captcha": captcha_text}
response = session.post(login_url, data=payload)
# 打印响应内容
print(response.text)