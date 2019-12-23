from django.shortcuts import render, HttpResponse
import json
import re
import datetime
import random
from demo4.settings import APIKEY
from .models import UserProfile, Code
from .utils.yunpian import YunPian
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer


# Create your views here.
class SendCodeView(APIView):
    def get(self, request):
        phone = request.GET.get('phone')
        if phone:
            mobile_pat = re.compile('^(13\d|14[5|7]|15\d|166|17\d|18\d)\d{8}$')
            res = re.search(mobile_pat, phone)
            if res:
                has_register = UserProfile.objects.filter(phone=phone)
                if has_register:
                    msg = '手机号已被注册！'
                    result = {"status": "402", "data": {'msg': msg}}
                    return HttpResponse(json.dumps(result, ensure_ascii=False),
                                        content_type="application/json,charset=utf-8")
                else:
                    has_send = Code.objects.filter(phone=phone).last()
                    if has_send:
                        if has_send.add_time.replace(tzinfo=None) > \
                                (datetime.datetime.now() - datetime.timedelta(minutes=1)):
                            msg = '距离上次发送验证码不足一分钟'
                            result = {"status": "403", "data":{'msg': msg}}
                            return HttpResponse(json.dumps(result, ensure_ascii=False),
                                                content_type="application/json, charset=utf-8")
                        else:
                            code = Code()
                            code.phone = phone
                            c = random.randint(1000, 9999)
                            code.code = str(c)
                            code.end_time = datetime.datetime.now() + datetime.timedelta(minutes=20)
                            code.save()
                            code = Code.objects.filter(phone=phone).last().code
                            yunpian = YunPian(APIKEY)
                            sms_status = yunpian.send_sms(code=code, mobile=phone)
                            msg = sms_status
                            return HttpResponse(msg)
                    else:
                        code = Code()
                        code.phone = phone
                        c = random.randint(1000, 9999)
                        code.code = str(c)
                        code.end_time = datetime.datetime.now() + datetime.timedelta(minutes=20)
                        code.save()
                        code = Code.objects.filter(phone=phone).last().code
                        yunpian = YunPian(APIKEY)
                        sms_status = yunpian.send_sms(code=code, mobile=phone)
                        msg = sms_status
                        return HttpResponse(msg)
            else:
                msg = "手机号不合法"
                result = {"status": "403", "data": {'msg': msg}}
                return HttpResponse(json.dumps(result, ensure_ascii=False),
                                    content_type="application/json,charset=utf-8")
        else:
            msg = '手机号为空'
            result = {"status": "404", "data": {'msg': msg}}
            return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")
