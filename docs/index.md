# 


<p align="center">
    <em>🏝 基于FastAPI和gRPC轻量级微服务开发框架</em>
</p>

---


## Introduction

Sun is a framework integrate FastAPI and gRPC. 
If you want to provide both HTTP and RPC, it can improve development efficiency.

It gives you the following features:

* A simple layout of file structure rule.
* Integrated `SQLAlchemy` ORM and provide generic model methods.
* Utilities of transform models to Pydantic schemas.
* GZipMiddleware included and GZip decompression enabled.
* 🍻 **Resource** layer to write code once support both HTTP and RPC

## Who's using sun framework

<a href="https://www.360shuke.com/">
    <img width="200" src="https://raw.githubusercontent.com/xqk/sun/master/docs/img/cases/qfin.png" />
</a>

## Requirements

1. Python 3.7+
2. FastAPI 0.63+
3. grpcio>=1.32.0,<1.42

## Installation

```shell
# Sun framework
pip install sun-core 

# Sun command line tool 
pip install sun-cli  
```
