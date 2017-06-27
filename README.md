ceph-rbd-fast-mirror


## TODO list
### 计划实现的功能

- [ ] 能够显示上传下载进度，比例
- [ ] 有已经上传列表和下载列表，以及失败的列表
- [ ] 能够设置缓冲盘的比例（两种比例）
- [ ] 支持多种底层设备
- [ ] 能够控制设置下载的速度（频率）
- [ ] 能够控制上传并发数目
- [ ] 可以支持传输结果校验
- [ ] 可以暂停，可以继续
- [ ] 最好可以图形显示进度
- [ ] 支持shell填写输入方式 指定集群的ip
- [ ] 支持对失败的列表进行重传
- [ ] 支持获取上传和下载集群状态
- [ ] 运行起来后并发主机数目（10s更新一次文件，如果节点不更新就认为节点失效了）
- [ ] 统计节点上传的对象数目
- [ ] 支持md5记录（会慢很多）



### 当前实现功能
- [x] 填写mon的地址，支持保存，修改反馈



### 预览图

已完成预览链接：
https://raw.githubusercontent.com/zphj1987/ceph-rbd-fast-mirror/master/preview.MP4

设计预览图：

![](https://raw.githubusercontent.com/zphj1987/ceph-rbd-fast-mirror/master/原型设计/oringin.png)