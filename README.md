# Bugly 接入 Slack

将 Bugly 的消息转发到 Slack 上。

## 接入

配置环境

```shell
pip install requests; pip install Werkzeug
```

启动服务

```shell
python3.7 wsgi.py
```

设置启动服务代理域名到Bugly

```
http://127.0.0.1:18078/xxx/xxx/xxx
```

可通过下面命令测试

```shell
curl -X POST \
-H "Content-Type: application/json" \
-d '{"eventType":"bugly_crash_trend","timestamp":1462780713515,"isEncrypt":0,"eventContent":{"datas":[{"accessUser":12972,"crashCount":21,"crashUser":20,"version":"1.2.3","url":"http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"},{"accessUser":15019,"crashCount":66,"crashUser":64,"version":"1.2.4","url":"http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"},{"accessUser":15120,"crashCount":1430,"crashUser":1423,"version":"1.2.4","url":"http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"}],"appId":"1104512706","platformId":1,"appName":"AF","date":"20160508","appUrl":"http://bugly.qq.com/issueIndex?app=1104512706&pid=1&ptag=1005-10000"},"signature":"ACE346A4AE13A23A52A0D0D19350B466AF51728A"}' \
http://127.0.0.1:18078/xxx/xxx/xxx
```



### Bugly json data
```json
{
  "eventType": "bugly_crash_trend",
  "timestamp": 1462780713515,
  "isEncrypt": 0,
  "eventContent": {
    "datas": [
      {
        "accessUser": 12972,//联网用户数
        "crashCount": 21,//crash次数
        "crashUser": 20,//crash影响用户数
        "version": "1.2.3",//app版本号
        "url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
      },
      {
        "accessUser": 15019,
        "crashCount": 66,
        "crashUser": 64,
        "version": "1.2.4",
        "url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
      },
      {
        "accessUser": 15120,
        "crashCount": 1430,
        "crashUser": 1423,
        "version": "1.2.4",
        "url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
      }
    ],
    "appId": "1104512706", //appId
    "platformId": 1   //平台
"appName": "AF", //app名称
    "date": "20160508",
"appUrl":"http://bugly.qq.com/issueIndex?app=1104512706&pid=1&ptag=1005-10000" 
  },
  "signature": "ACE346A4AE13A23A52A0D0D19350B466AF51728A"
}

```

slack 接收json格式
```json
{
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "每日崩溃统计(2021-03-12)\n22",
				"emoji": true
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*V3.1.1*"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*联网用户数:*\n12972"
				},
				{
					"type": "mrkdwn",
					"text": "*崩溃次数*\n21"
				},
				{
					"type": "mrkdwn",
					"text": "*崩溃用户数*\n20"
				},
				{
					"type": "mrkdwn",
					"text": "*崩溃率*\n0.5%"
				}
			]
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*V 3.1.2*"
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*联网用户数:*\n12972"
				},
				{
					"type": "mrkdwn",
					"text": "*崩溃次数*\n21"
				},
				{
					"type": "mrkdwn",
					"text": "*崩溃用户数*\n20"
				},
				{
					"type": "mrkdwn",
					"text": "*崩溃率*\n0.5%"
				}
			]
		}
	]
}
```