import json
import random
import uuid

# 指令模板
intents = [
    {
        "intent_name": "ConnectBlueTooth",
        "intent_description": "连接或断开蓝牙设备",
        "slots": ["DeviceType", "ActionType"],
        "examples": ["帮我把{DeviceType}蓝牙连上", "断开{DeviceType}的蓝牙"]
    },
    {
        "intent_name": "AdjustVolume",
        "intent_description": "调整音量大小",
        "slots": ["VolumeLevel"],
        "examples": ["把音量调到{VolumeLevel}%", "音量降低到{VolumeLevel}%"]
    },
    {
        "intent_name": "RestartDevice",
        "intent_description": "重启设备",
        "slots": [],
        "examples": ["重启手机", "帮我重启一下设备"]
    },
    {
        "intent_name": "OpenApp",
        "intent_description": "打开指定应用",
        "slots": ["AppName"],
        "examples": ["帮我打开{AppName}", "启动{AppName}"]
    }
]

# 可选参数
device_types = ["手机", "耳机", "音箱", "键盘", "鼠标", "车载", "打印机"]
app_names = ["微信", "QQ", "浏览器", "音乐", "邮件", "日历"]

samples = []

for i in range(50):
    intent = random.choice(intents)
    data_entry = {"role": "user", "content": ""}
    # 填充槽位
    slots_values = {}
    if intent["intent_name"] == "ConnectBlueTooth":
        device = random.choice(device_types)
        action = random.choice([True, False])
        slots_values["DeviceType"] = device
        slots_values["ActionType"] = action
        user_text = random.choice(intent["examples"]).format(DeviceType=device)
        assistant_text = f'ConnectBlueTooth(DeviceType="{device}", ActionType={action})'
    elif intent["intent_name"] == "AdjustVolume":
        level = random.randint(0, 100)
        slots_values["VolumeLevel"] = level
        user_text = random.choice(intent["examples"]).format(VolumeLevel=level)
        assistant_text = f'AdjustVolume(VolumeLevel={level})'
    elif intent["intent_name"] == "RestartDevice":
        user_text = random.choice(intent["examples"])
        assistant_text = "RestartDevice()"
    elif intent["intent_name"] == "OpenApp":
        app = random.choice(app_names)
        slots_values["AppName"] = app
        user_text = random.choice(intent["examples"]).format(AppName=app)
        assistant_text = f'OpenApp(AppName="{app}")'

    # 构建 sample
    sample = {
        "id": str(uuid.uuid4()),
        "intent_name": intent["intent_name"],
        "intent_description": intent["intent_description"],
        "slots": intent["slots"],
        "category_Level1": "示例一级分类",
        "category_Level2": "示例二级分类",
        "category_Level3": "示例三级分类",
        "data": [
            {"role": "user", "content": user_text},
            {"role": "assistant", "content": assistant_text},
            {"role": "tool", "tool_name": intent["intent_name"], "reply": "工具执行成功"}
        ]
    }
    samples.append(sample)

# 保存到 JSON 文件
with open("train_data.json", "w", encoding="utf-8") as f:
    json.dump(samples, f, ensure_ascii=False, indent=2)

print("✅ 已生成 50 条训练数据，保存为 train_data.json")
