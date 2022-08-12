# magical_spider
神奇的蜘蛛🕷，一个几乎适用于所有web端站点的采集方案。


### 诞生背景
纯属瞎扯：2022年全球变暖，各行业内卷严重，爬虫届更是入门抖音起步瑞数，为了减缓人才流失，推出magical_spider。

真实原因：一时兴起，吾辈当自强，重铸selenium荣光！ 

博客地址： [lxspider](http://www.lxspider.com)  爬虫逆向工具站：[lxtools](http://www.cnlans.com/lx/tools)


### 项目简介
- 非常规derver.pageSource。
- 通过Flask远程调用chromederver实现xmlHttpRequest。
- 通过sqlit记录任务状态。
- 通过undetected_selenium+stealth.min.js绕过一些校验。
- 目前适用于瑞数、加速乐等cookie加密，以及头条系的请求过程加密。


### 项目声明
- 项目仅供学习参考。
- 如有风控校验需自行解决，滑块可参考middlerware.py。
- 方案适用于应急场景或数据量要求不高时，若时间充裕建议通过逆向处理。推荐阅读：[《爬虫逆向进阶实战》](https://github.com/lixi5338619/lxBook)



### 部署
[linux部署文档](static/docs/部署.txt)

---

## 使用说明

1、配置settings.py，启动 flask 服务

2、运行方法参考demo文件内容,主要借助runflow.py。

3、测试代码

```python
from demo.runflow import magical_start,magical_request,magical_close

project_name = 'cnipa'
base_url = 'https://www.cnipa.gov.cn'

session_id,process_url = magical_start(project_name,base_url)

print(len(magical_request(session_id, process_url,'https://www.cnipa.gov.cn/col/col57/index.html')))

magical_close(session_id,process_url,project_name)
```

4、index页可以查看和管理当前运行中的任务，也能查看系统内存和磁盘使用情况。

5、demo文件夹中有任务流程汇总runflow.py，以及抖音、药监局案例，单任务和多任务示例。

![Alt](./static/image/index2.png)
