
# 程序接口示例(以零序保护为例)
实现从DM数据库读取保护定值、运行CloudPSS仿真、获取仿真输出结果、输出结果写回数据库等功能.
## 基本信息
- 输入参数: 保护定值、软压板
- 输出结果:日志记录、模拟量
- 模型链接 
  http://cloudpss-calculate.ddns.cloudpss.net/model/w864273603/SiChuanProectionTestSystem#/design/diagram/canvas/canvas_0 
- 示例:参见文件example.ipynb
- python版本：python 3.9.9 64位
- 依赖包配置:`pip install cloudpss`、`pip install plotly`、`pip install dmPython`


## CloudPSS模型
若模型链接无法打开，请配置 vpn，参加文件**vpn客户端及配置2024**,注意：要求用户具有内网账号。

若用户无内网账号，则可以本地导入测试系统、测试元件，已置于文件夹**cloudpssmodel**中。

## 数据库
- 本地初始化：相关数据库表初始化、数据导入sql脚本,参加文件目录**数据库建表相关**。
- 远程连接测试：可使用算例提供的数据库案例进行远程测试，Ip、用户名和密码见**数据库建表相关\数据库信息**。

## Simulink封装示例
参见simulink模型文件 **simulinkmodel**目录中的**SiChuanProtectionTest.slx**。

## Sfunction编译示例(https://latest.kb.cloudpss.net/documents/software/emtlab/emts/user-defined/s-function-control/)

**simulinkmodel**目录中的**protection2.so**为对应**示例测试元件**在linux64为系统下的编译产物。

## 示例测试元件
本示例的测试元件的代码实现部分由**simulink封装示例**中的测试元件生成sfunction代码后编译得到，接口实现部分在CloudPSS平台中设计完成，元件接口设计可通过导入**保护仿真接口测试元件**查看。
