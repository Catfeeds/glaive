# GlaiveServer
***
### API
1. /server/devices  
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 得到该服务器连接的设备数量                                       |
	| url    | http://localhost:4000/server/devices                             |
	| method | GET                                                              |
	| 参数   | 无                                                               |
	
	| 返回   | **data域**                 | **类型**    | **说明**              |
	| ------ |:-------------------------- | ----------- | --------------------- |
	|        | devices                    | integer     | 连接的设备数量        |
	
2. /server/servers 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 得到连接到该服务器的其它服务器数量                               |
	| url    | http://localhost:4000/server/servers                             |
	| method | GET                                                              |
	| 参数   | 无                                                               |
	
	| 返回   | **data域**                 | **类型**    | **说明**              |
	| ------ |:-------------------------- | ----------- | --------------------- |
	|        | servers                    | integer     | 连接的服务器数量      |

3. /device/&lt;imei&gt; 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 获取设备的信息，包括位置、电量、在线状态等                       | 
	| url    | http://localhost:4000/device/&lt;imei&gt;                        | 
	|        | &lt;imei&gt;是被查询设备的IMEI号                                 |
	| method | GET                                                              |
	| 参数   | 无                                                               |
	
	| 返回   | **data域**                 | **类型**    | **说明**              |
	| ------ |:-------------------------- | ----------- | --------------------- |
	|        | location                   | object      |                       |
	|        | location.lat               | float       | 纬度                  |
	|        | location.lng               | float       | 经度                  |
	|        | location.time              | timestamp   | 定位时间              |
	|        | active                     | integer     |0: 离线 1: 在线        |
	|        | power                      | integer     |电量百分比数值 0-100   |
    
4. /device/&lt;imei&gt;/host 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 获取设备的服务器信息                                             |
	| url    | http://localhost:4000/device/&lt;imei&gt;/host                   |
	|        | &lt;imei&gt;是被查询设备的IMEI号                                 |
	| method | GET                                                              |
	| 参数   | 无                                                               |
	
	| 返回   | **data域**                 | **类型**    | **说明**              |
	| ------ |:-------------------------- | ----------- | --------------------- |
	|        | mqtt                       | object
	|        | mqtt.host                  | string      | 设备连接的mqtt broker地址
	|        | mqtt.port                  | integer     | 设备连接的mqtt broker 端口
	|        | web                        | object
	|        | web.host                   | string      | 设备的API服务器地址
	|        | web.port                   | integer     | 设备的API服务器端口
	|        | server                     | string      | 设备连接的服务器ID

5. /device/&lt;imei&gt;/loc 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   |获取设备的位置信息                                                |
	| url    | http://localhost:4000/device/&lt;imei&gt;/loc                    |
	|        | &lt;imei&gt;是被查询设备的IMEI号                                 |
	| method | GET                                                              |
	| 参数   | 无                                                               |
	
	| 返回   | **data域**                 | **类型**    | **说明**              |
	| ------ |:-------------------------- | ----------- | --------------------- |
	|        | lat                        | float       | 纬度
	|        | lng                        | float       | 经度
	|        | time                       | timestamp   | 定位时间
	
6. /device/&lt;imei&gt;/active 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   |获取设备的在线状态                                                |
	| url    | http://localhost:4000/device/&lt;imei&gt;/active                 |
	|        | &lt;imei&gt;是被查询设备的IMEI号                                 |
	| method | GET                                                              |
	| 参数   | 无                                                               |
	
	| 返回   | **data域**                 | **类型**    | **说明**              |
	| ------ |:-------------------------- | ----------- | --------------------- |
	|        | active                     | integer     | 0: 离线  1: 在线
	
7. /device/&lt;imei&gt;/power 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   |获取设备的电量                                                    |
	| url    | http://localhost:4000/device/&lt;imei&gt;/power                  |                
	|        | &lt;imei&gt;是被查询设备的IMEI号                                 |
	| method | GET                                                              |
	| 参数   | 无                                                               |
	
	| 返回   | **data域**                 | **类型**    | **说明**              |
	| ------ |:-------------------------- | ----------- | --------------------- |
	|        | power                      | integer     |电量百分比数值 0-100   |
	
8. /device/&lt;imei&gt;/users 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 通知服务器更新设备的绑定用户                                     |
	| url    | http://localhost:4000/device/&lt;imei&gt;/users                  |
	|        | &lt;imei&gt;是设备的IMEI号                                       |
	| method | POST                                                             |
	| 参数   | 无                                                               |
	| 返回   | 无                                                               |
	
9. /device/&lt;imei&gt;/fences 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 通知服务器更新设备的围栏
	| url    | http://localhost:4000/device/&lt;imei&gt;/fences                 |
	|        | &lt;imei&gt;是设备的IMEI号
	| method | POST                                                             |
	| 参数   | 无                                                               |
	| 返回   | 无                                                               |
	
10. /device/&lt;imei&gt;/config 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 通知服务器更新设备的设置
	| url    | http://localhost:4000/device/&lt;imei&gt;/config                 |
	|        | &lt;imei&gt;是设备的IMEI号
	| method | POST                                                             |
	| 参数   | 无                                                               |
	| 返回   | 无                                                               |
	
11. /device/&lt;imei&gt;/phonebook 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 通知服务器更新设备的电话本
	| url    | http://localhost:4000/device/&lt;imei&gt;/phonebook              |
	|        | &lt;imei&gt;是设备的IMEI号
	| method | POST                                                             |
	| 参数   | 无                                                               |
	| 返回   | 无                                                               |
	
12. /device/&lt;imei&gt;/family 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 通知服务器更新设备的家庭成员
	| url    | http://localhost:4000/device/&lt;imei&gt;/family                 |
	|        | &lt;imei&gt;是设备的IMEI号
	| method | POST                                                             |
	| 参数   | 无                                                               |
	| 返回   | 无                                                               |
	
13. /device/&lt;imei&gt;/nodisturb 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 通知服务器更新设备的免打扰设置
	| url    | http://localhost:4000/device/&lt;imei&gt;/nodisturb              |
	|        | &lt;imei&gt;是设备的IMEI号
	| method | POST                                                             |
	| 参数   | 无                                                               |
	| 返回   | 无                                                               |
	
20. /device/&lt;imei&gt;/alarm 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 通知服务器更新设备的闹钟设置
	| url    | http://localhost:4000/device/&lt;imei&gt;/alarm                  |
	|        | &lt;imei&gt;是设备的IMEI号
	| method | POST                                                             |
	| 参数   | 无                                                               |
	| 返回   | 无                                                               |
	
14. /device/&lt;imei&gt;/voice/&lt;fromuser&gt;/&lt;voiceid&gt; 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 通知服务器向设备发送语音
	| url    | http://localhost:4000/device/&lt;imei&gt;/voice/&lt;fromuser&gt;/&lt;voiceid&gt;
	|        | &lt;imei&gt;是设备的IMEI号
	|        | &lt;fromuser&gt;是发送者的电话号码
	|        | &lt;voiceid&gt;是语音的ID
	| method | POST                                                             |
	| 参数   | 无                                                               |
	| 返回   | 无                                                               |
	
15. /device/&lt;imei&gt;/monitor/&lt;fromuser&gt; 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 通知服务器向设备发送监控指令
	| url    | http://localhost:4000/device/&lt;imei&gt;/monitor/&lt;fromuser&gt;
	|        | &lt;imei&gt;是设备的IMEI号
	|        | &lt;fromuser&gt;是发送者的电话号码
	| method | POST                                                             |
	| 参数   | 无                                                               |
	| 返回   | 无                                                               |
	
16. /device/&lt;imei&gt;/shutdown 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 通知服务器关闭设备
	| url    | http://localhost:4000/device/&lt;imei&gt;/shutdown               |
	|        | &lt;imei&gt;是设备的IMEI号
	| method | POST                                                             |
	| 参数   | 无                                                               |
	| 返回   | 无                                                               |
	
17. /device/&lt;imei&gt;/find 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 通知服务器发送设备响铃
	| url    | http://localhost:4000/device/&lt;imei&gt;/find                   |
	|        | &lt;imei&gt;是设备的IMEI号
	| method | POST                                                             |
	| 参数   | 无                                                               |
	| 返回   | 无                                                               |
	
18. /device/&lt;imei&gt;/factory 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 通知服务器恢复设备出厂设置
	| url    | http://localhost:4000/device/&lt;imei&gt;/factory                |
	|        | &lt;imei&gt;是设备的IMEI号
	| method | POST                                                             |
	| 参数   | 无                                                               |
	| 返回   | 无                                                               |
	
19. /device/&lt;imei&gt;/loc 
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 通知服务器发送定位指令
	| url    | http://localhost:4000/device/&lt;imei&gt;/loc                    |
	|        | &lt;imei&gt;是设备的IMEI号
	| method | POST                                                             |
	| 参数   | 无                                                               |
	
	| 返回   | **data域**                 | **类型**    | **说明**              |
	| ------ |:-------------------------- | ----------- | --------------------- |
	|        | lat                        | float       | 纬度
	|        | lng                        | float       | 经度
	|        | time                       | timestamp   | 定位时间
	
20. /device/&lt;imei&gt;/takephoto/&lt;fromuser&gt;/&lt;sid&gt;
	
	| 项目   | 内容                                                             |
	| ------ |:---------------------------------------------------------------- |
	| 说明   | 通知服务器发送定位指令
	| url    | http://localhost:4000/device/&lt;imei&gt;/takephoto/&lt;fromuser&gt;/&lt;sid&gt;
	|        | &lt;imei&gt;是设备的IMEI号
	|        | &lt;fromuser&gt;是发送者的电话号码
	|        | &lt;sid&gt;是客户创建的会话id，回传时发送给用户
	| method | POST                                                             |
	| 参数   | 无                                                               |
	| 返回   | 无                                                               |