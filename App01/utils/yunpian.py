import requests


class YunPian():
    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        parmas = {
            'apikey': self.api_key,
            'mobile': mobile,
            'text': '"jinghuashuiyue"正在进行登陆操作，您的验证码是{code}'.format(code=code)
        }
        r = requests.post(self.single_send_url, data=parmas)
        print(r.text)


if __name__ == "__main__":
    yun_pian = YunPian('cd3c1f3289668b61794ffd3af5abf791')
    yun_pian.send_sms('1234', '17521691263')
