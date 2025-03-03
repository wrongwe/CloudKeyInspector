
## 功能亮点
- 🚩 **四大云厂商支持**  
  ☁️ 阿里云 | 🌩️ AWS | 🐧 腾讯云 | 🔥 华为云
- 🚦 **三级状态检测**  
  识别有效/无效/权限受限等密钥状态
- 🛡️ **安全检测**  
  仅调用只读API，不修改云资源
- 🎨 **彩色终端输出**  
  红/黄/绿三色警示系统

## 快速开始

### 1. 下载脚本
```bash
wget https://raw.githubusercontent.com/wrongwe/CloudKeyInspector/main/CloudKeyInspector.py
```

### 2. 运行检测
```bash
python CloudKeyInspector.py
```

### 3. 按提示操作
```text
**************************************
*      多云密钥检测工具 (四厂商完整版)     *
**************************************

支持厂商:
1. 阿里云
2. AWS
3. 腾讯云
4. 华为云

请输入厂商编号: 2

请输入AWS AccessKey ID: AKIAxxxxxxxxxxxx
请输入AccessKey Secret: 

⌛ 正在检测AWS密钥...

✅ 有效密钥
```

## 安装依赖
```bash
# 基础依赖
pip install requests

# 按需安装云厂商SDK
pip install aliyun-python-sdk-core boto3 tencentcloud-sdk-python huaweicloudsdkcore
```

## 检测结果说明
| 状态显示                 | 响应动作建议               |
|-------------------------|--------------------------|
| ✅ 有效密钥               | 正常使用，建议定期轮换      |
| 🟡 有效但无操作权限        | 检查IAM权限策略           |
| ❌ 无效密钥               | 立即吊销并重新生成         |
| ⚠️ 检测失败              | 检查网络或API可用性        |

## 项目结构
```bash
CloudKeyInspector/
├── CloudKeyInspector.py    # 主检测脚本
├── LICENSE                 # 开源协议
└── README.md               # 说明文档
```

---
**注意**：使用前请确保已阅读并同意各云厂商的API调用条款。  
```
