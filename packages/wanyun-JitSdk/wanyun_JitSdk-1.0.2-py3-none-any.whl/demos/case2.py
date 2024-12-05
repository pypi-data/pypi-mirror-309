# -*-coding:utf-8-*-
"""
Created on 2024/11/16

@author: 臧韬

@desc: 默认描述
"""

from wanyun_JitSdk import JitApi
from wanyun_JitSdk import JitApiRequest
from wanyun_JitSdk import JitApiResponse

authApi = JitApi("http://127.0.0.1:5050/api/whwy/b")  # 授权方的api访问地址
authApi.setAccessKey("111111111111111111")  # api授权元素配置的accessKey
authApi.setAccessSecret("c58929c718f844abaaae2461ea1b2ff8024a96")  # api授权元素配置的accessSecret
authApi.setApi("services.iThinkItsIiui.switchesPlanned")  # 需要调用的api
req = JitApiRequest()
req.setMethod("POST")  # 接口请求方式，默认为POST
req.setParams({'itsABlowItsABlow': '123', 'space': 'dffd'})  # 接口参数
resp = req.execute(authApi)
print(resp.data)
