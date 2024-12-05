import json
import zlib

from Jce import JceInputStream, JceStruct

from AndroidQQ.struct.head import *


def DelDevLoginInfo(info, key):
    """删除登录信息"""
    key = bytes.fromhex(key)
    _data = JceWriter().write_bytes(key, 0)

    jce = JceWriter()
    jce.write_bytes(info.Guid, 0)
    jce.write_string('com.tencent.mobileqq', 1)
    jce.write_jce_struct_list([_data], 2)
    jce.write_int32(1, 3)
    jce.write_int32(0, 4)
    jce.write_int32(0, 5)
    _data = jce.bytes()
    _data = JceWriter().write_jce_struct(_data, 0)
    _data = JceWriter().write_map({'SvcReqDelLoginInfo': _data}, 0)
    _data = PackHeadNoToken(info, _data, 'StatSvc.DelDevLoginInfo', 'StatSvc', 'SvcReqDelLoginInfo')
    _data = Pack_(info, _data, Types=11, encryption=1, sso_seq=info.seq)
    return _data


def DelDevLoginInfo_res(data):
    """似乎没有明确的返回信息"""
    # 78508586932311d7c68de3bd2a27688a80734dee86300ca37085afb7568a0d68ff8a802375158ecd633518aa3e7756a6cc9f18e10dc2d2f3a8a3e5b7a246b197504d4582a9e19b4c28dad9d30461f5131fd264ff6b48692e88bcc1b54873ace52c80dcd2e6a67270
    """
    - 消息
    1. a7eb596ed0a7d77097ae32958ec28ada82376735c25fe8b43b5dcdcd33e4fc9f1bb974a3f082336477b0449e48e7e26dff4f0987fa0cdfe1060483afe05675af85318913651e990a050ac0e2c3784f3a55f2e810ac191bd0a2ba2b0d0d51d2bbd3856f70d6fbb26070858142ba6d9596830f2d5b0a53b4c041ddd9a4d7d86f9ac4e3aa3938b0de5a
    2. 9ce7fe8510c88e1ecffef921cc92c060d92f1301564f97fdb13f4bf5354165b1bb3913c2cd43b6ad259a5fd2997b566ec4b526517a76d2a1cd52fb4c7cb52fc87c8597742440a6e2b6e167061c07432dbc63beb411053092efbd6c15c032094766b61c69157536d340d14fb6881f281653761a4797a6fd486f0a2d3d77c4f2f9c776dca0e1a0b1d0
    3. 5585af650ba57e77eefb25a59935bf0a3cd21c0f3c8870a83f349b6ef0c2638130f0ff375b3a83ce40f3adea52747976902bd9eb096598b529581aeb1794a016184ad3d7dfd7c3398c64666ea38eedb00158d3e113cd36ad7a6d070724dfd3ff5c401e383e8f81ff076b130236685c57083101c7778ef2208a0bec0e44d6a3bd111d1a6ef87a1d1f177625e31758a2a7
    4. ef2434f61d0f0b3012aa0720308891e5cb7e8f0521c1a976bbaea78152170810c1ff7725245f7e456ba71a1db1c6b94fd589b18426b92cf78880c9c450e17100de483973fcf70c0cd2271f2efb2f4c2b87ff93041e0dc051338ffe3222ba4145f4c65368f5050b8bdca2a548041700cf43e745d966928cc79d17bef0462be6ca46aebe69ad607fe09ea91958e5db5f9a
    5. fd176f0adce8e26a991be3fc67e290f69a2cfd8ad78d8ae1415b84b435a9558123f3cec7c431039e90111119d6d39f2da9bf950c74a630b137615ee734fd079a8ee04e36d5e1aec9cdf4140f62364fefac483cd68014a74548856452a1014f9b964e6a34b1e504f9d86c2f829162dcca26d812afe5145b44e5b77ad9ac997a807202af63f9349d242eb3916f6c4c055e9f06e3aa8003efd2
    """

    data = Un_jce_Head(data)
    data = Un_jce_Head_2(data)
    stream = JceInputStream(data)
    jce = JceStruct()
    jce.read_from(stream)
    return jce.to_json()
