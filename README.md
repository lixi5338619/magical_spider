# magical_spider
神奇的蜘蛛🕷，一个几乎适用于所有web端站点的采集方案。


### 诞生背景
纯属瞎扯：2022年全球变暖，各行业内卷严重，爬虫届更是入门抖音起步瑞数，为了减缓人才流失，推出magical_spider。

真实原因：一时兴起，吾辈当自强，重铸selenium荣光！ 

博客地址： [lxspider.com](http://www.lxspider.com)

爬虫逆向工具站：[lxtools](http://www.cnlans.com/lx/tools)


### 项目简介
- 非常规derver.pageSource。
- 通过Flask远程调用chromederver实现xmlHttpRequest。
- 通过sqlit记录任务状态。
- 通过undetected_selenium+stealth.min.js绕过一些校验。
- 目前适用于瑞数、加速乐等cookie加密，以及头条系的请求过程加密。


### 项目声明
- 项目仅供学习参考。
- 百千万采集量勿需尝试。
- 如有风控校验需自行解决，滑块可参考middlerware.py。




### 部署
[linux部署文档](./docs/部署.txt)

注意：使用时需要在settings中配置驱动路径。

---

## 使用说明

index页可以查看和管理当前运行中的任务，也能查看系统内存和磁盘使用情况。

demo文件夹中有任务流程汇总runflow.py，以及抖音、药监局案例，单任务和多任务示例。



![Alt](./static/image/index.png)
