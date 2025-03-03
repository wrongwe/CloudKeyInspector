import sys
import getpass
from enum import Enum
from typing import Dict, Callable

# 颜色定义
COLOR = {
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "END": "\033[0m"
}


class CloudProvider(Enum):
    ALIYUN = "阿里云"
    AWS = "AWS"
    TENCENT = "腾讯云"
    HUAWEI = "华为云"


# ==================== 阿里云检测逻辑 ====================
try:
    from aliyunsdkcore.client import AcsClient
    from aliyunsdkcore.acs_exception.exceptions import ServerException, ClientException
    from aliyunsdkram.request.v20150501 import GetUserRequest


    def check_aliyun(ak: str, sk: str) -> str:
        try:
            client = AcsClient(ak, sk, 'cn-hangzhou', timeout=5)
            request = GetUserRequest.GetUserRequest()
            client.do_action_with_exception(request)
            return f"{COLOR['GREEN']}✅ 有效密钥（基础权限正常）{COLOR['END']}"
        except (ServerException, ClientException) as e:
            if 'InvalidAccessKeyId' in str(e):
                return f"{COLOR['RED']}❌ 无效密钥{COLOR['END']}"
            elif 'Forbidden' in str(e):
                return f"{COLOR['YELLOW']}🟡 有效但无操作权限{COLOR['END']}"
            else:
                return f"{COLOR['RED']}⚠️  检测失败：{str(e)}{COLOR['END']}"
except ImportError:
    def check_aliyun(ak: str, sk: str) -> str:
        return f"{COLOR['RED']}❌ 未安装阿里云SDK（pip install aliyun-python-sdk-core）{COLOR['END']}"

# ==================== AWS检测逻辑 ====================
try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError


    def check_aws(ak: str, sk: str) -> str:
        try:
            client = boto3.client(
                'sts',
                aws_access_key_id=ak,
                aws_secret_access_key=sk
            )
            client.get_caller_identity()
            return f"{COLOR['GREEN']}✅ 有效密钥{COLOR['END']}"
        except (ClientError, NoCredentialsError) as e:
            error_code = e.response['Error']['Code'] if hasattr(e, 'response') else str(e)
            if error_code in ['InvalidClientTokenId', 'UnrecognizedClientException']:
                return f"{COLOR['RED']}❌ 无效密钥{COLOR['END']}"
            return f"{COLOR['YELLOW']}🟡 权限受限：{error_code}{COLOR['END']}"
except ImportError:
    def check_aws(ak: str, sk: str) -> str:
        return f"{COLOR['RED']}❌ 未安装AWS SDK（pip install boto3）{COLOR['END']}"

# ==================== 腾讯云检测逻辑 ====================
try:
    from tencentcloud.common import credential
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.cam.v20190116 import cam_client, models


    def check_tencent(ak: str, sk: str) -> str:
        try:
            cred = credential.Credential(ak, sk)
            client = cam_client.CamClient(cred, "ap-guangzhou")
            req = models.GetUserRequest()
            client.GetUser(req)
            return f"{COLOR['GREEN']}✅ 有效密钥{COLOR['END']}"
        except TencentCloudSDKException as e:
            if "InvalidCredential" in str(e):
                return f"{COLOR['RED']}❌ 无效密钥{COLOR['END']}"
            return f"{COLOR['YELLOW']}🟡 权限错误：{e.get_code()}{COLOR['END']}"
except ImportError:
    def check_tencent(ak: str, sk: str) -> str:
        return f"{COLOR['RED']}❌ 未安装腾讯云SDK（pip install tencentcloud-sdk-python）{COLOR['END']}"

# ==================== 华为云检测逻辑 ====================
try:
    from huaweicloudsdkcore.auth.credentials import BasicCredentials
    from huaweicloudsdkiam.v3 import IamClient, ShowUserRequest
    from huaweicloudsdkcore.exceptions import exceptions


    def check_huawei(ak: str, sk: str) -> str:
        try:
            credentials = BasicCredentials(ak, sk)
            client = IamClient.new_builder().with_credentials(credentials).build()
            client.show_user(ShowUserRequest())
            return f"{COLOR['GREEN']}✅ 有效密钥{COLOR['END']}"
        except exceptions.ClientRequestException as e:
            if "APIGW.0101" in str(e):
                return f"{COLOR['RED']}❌ 无效密钥{COLOR['END']}"
            return f"{COLOR['YELLOW']}🟡 权限错误：{e.error_code}{COLOR['END']}"
except ImportError:
    def check_huawei(ak: str, sk: str) -> str:
        return f"{COLOR['RED']}❌ 未安装华为云SDK（pip install huaweicloudsdkcore huaweicloudsdkiam）{COLOR['END']}"


# ==================== 主程序 ====================
def main():
    print(f"""
    {COLOR['GREEN']}**************************************
    *      多云密钥检测工具 (四厂商完整版)     *
    **************************************{COLOR['END']}
    """)

    providers = {
        1: (CloudProvider.ALIYUN, check_aliyun),
        2: (CloudProvider.AWS, check_aws),
        3: (CloudProvider.TENCENT, check_tencent),
        4: (CloudProvider.HUAWEI, check_huawei)
    }

    # 显示厂商列表
    print("支持厂商:")
    for num, (provider, _) in providers.items():
        print(f"{num}. {provider.value}")

    try:
        # 选择云厂商
        choice = int(input("\n请输入厂商编号: "))
        provider, check_func = providers.get(choice, (None, None))
        if not provider:
            print(f"{COLOR['RED']}错误：无效的编号{COLOR['END']}")
            return

        # 获取凭证
        ak = input(f"\n请输入{provider.value} AccessKey ID: ").strip()
        if not ak:
            print(f"{COLOR['RED']}错误：AccessKey ID不能为空{COLOR['END']}")
            return

        sk = getpass.getpass("请输入AccessKey Secret: ") if sys.stdin.isatty() else input("Secret: ")

        # 执行检测
        print(f"\n{COLOR['YELLOW']}⌛ 正在检测{provider.value}密钥...{COLOR['END']}")
        result = check_func(ak, sk)
        print(f"\n{result}")

    except (ValueError, KeyboardInterrupt):
        print(f"\n{COLOR['RED']}操作已取消{COLOR['END']}")


if __name__ == "__main__":
    main()