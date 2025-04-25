
---

# ROS2 传感器集成项目说明
需要给权限 配置节点
## 节点概览

### 1. `sensor_node`
- **功能**：定时读取并发布以下传感器数据：
  - `temperature` （温度，Float32）
  - `humidity` （湿度，Float32）
  - `mq2` （烟雾报警，Bool）
- **硬件支持**：
  - AHT10 温湿度传感器（I2C）
  - MQ2 烟雾传感器（GPIO）

### 2. `human_detector_client`
- **功能**：检测红外人体传感器信号
- **行为**：当检测到人体靠近时，请求 ROS2 服务 `/do_something`
- **传感器引脚**：GPIO2_10（编号 474）

### 3. `do_something_server`
- **功能**：响应来自 `human_detector_client` 的服务请求
- **服务类型**：`std_srvs/srv/Trigger`
- **可扩展行为**：可根据实际需求实现如拍照、报警、灯光控制等功能

---

