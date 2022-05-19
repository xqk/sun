# 

<p align="center">
    <em>🏝 基于FastAPI和gRPC轻量级微服务开发框架</em>
</p>

---

## 简介

简化基于 FastAPI 和 gRPC 的云原生微服务开发。如果你想让你的项目同时支持 HTTP 和 gRPC ,那么 Sun 可以帮助你很轻松的完成。 

Sun 的特性：

* 项目结构简单。
* 融合了 `SQLAlchemy` 并提供了 model 生成的方法。
* 提供了工具类转换 model 成为 Pydantic 模式.
* 支持 GZip 解压缩.
* 🍻 **Resource** 层处理对外服务即支持 HTTP 又支持 gRPC
* 支持 Event 发送及监听


## 谁在使用 Sun 框架

<a href="https://www.360shuke.com/">
    <img width="200" src="https://raw.githubusercontent.com/xqk/sun/master/docs/img/cases/qfin.png" />
</a>

## 依赖

1. Python 3.7+
2. FastAPI 0.63+
3. grpcio>=1.32.0,<1.42

## 安装

```shell
# Sun framework
pip install sun-core 

# Sun command line tool 
pip install sun-cli  
```
