# CloudKeyInspector

![Python Version](https://img.shields.io/badge/python-3.7%2B-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**CloudKeyInspector** 是一款专业的多云密钥检测工具，支持快速验证阿里云、AWS、腾讯云、华为云的AccessKey有效性及权限状态。

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
