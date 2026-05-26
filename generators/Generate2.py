import json
import random
import uuid

# 一级分类、二级分类、意图和槽位
intents = [
    {"intent_name": "ConnectBlueTooth", "desc": "连接或断开蓝牙设备",
     "slots": ["DeviceType", "ActionType"], "examples": ["帮我把{DeviceType}蓝牙连上", "断开{DeviceType}的蓝牙"]},
    {"intent_name": "ConnectWiFi", "desc": "连接指定 WiFi", "slots": ["SSID", "Password"],
     "examples": ["帮我连接WiFi {SSID}", "用密码 {Password} 连接 {SSID}"]},
    {"intent_name": "SetVPN", "desc": "开启或关闭 VPN", "slots": ["VPNName", "ActionType"],
     "examples": ["开启 VPN {VPNName}", "关闭 VPN {VPNName}"]},
    {"intent_name": "SetAppPermission", "desc": "设置应用权限", "slots": ["AppName", "Permission", "ActionType"],
     "examples": ["允许 {AppName} 使用 {Permission}", "禁止 {AppName} 使用 {Permission}"]},
    {"intent_name": "SetLockScreen", "desc": "锁屏设置", "slots": ["ActionType"],
     "examples": ["启用锁屏", "禁用锁屏"]},
    {"intent_name": "SetPowerMode", "desc": "设置电源模式", "slots": ["Mode"],
     "examples": ["切换到 {Mode} 模式", "开启 {Mode} 电源模式"]},
    {"intent_name": "CheckBatteryHealth", "desc": "检查电池健康状态", "slots": [],
     "examples": ["检查电池健康", "帮我看看电池状况"]},
    {"intent_name": "AdjustVolume", "desc": "调整音量大小", "slots": ["VolumeLevel"],
     "examples": ["把音量调到 {VolumeLevel}%", "音量降低到 {VolumeLevel}%"]},
    {"intent_name": "SetNotification", "desc": "通知管理", "slots": ["AppName", "ActionType"],
     "examples": ["开启 {AppName} 通知", "关闭 {AppName} 通知"]},
    {"intent_name": "AdjustBrightness", "desc": "调整屏幕亮度", "slots": ["BrightnessLevel"],
     "examples": ["把亮度调到 {BrightnessLevel}%", "降低屏幕亮度到 {BrightnessLevel}%"]},
    {"intent_name": "RestartDevice", "desc": "重启设备", "slots": [],
     "examples": ["重启设备", "帮我重启一下"]},
    {"intent_name": "UpdateSystem", "desc": "系统更新", "slots": [],
     "examples": ["检查系统更新", "更新系统"]},
    {"intent_name": "OpenApp", "desc": "打开应用", "slots": ["AppName"],
     "examples": ["打开 {AppName}", "启动 {AppName}"]}
]

# 可选值
device_types = ["手机", "耳机", "音箱", "键盘", "鼠标", "车载", "打印机"]
app_names = ["微信", "QQ", "浏览器", "音乐", "邮件", "日历"]
vpn_names = ["公司VPN", "学校VPN"]
wifi_ssid = ["HomeWiFi", "OfficeWiFi"]
permissions = ["相机", "麦克风", "位置"]
modes = ["节能", "性能", "平衡"]

samples = []

for i in range(50):
    intent = random.choice(intents)
    slots_values = {}
    user_text = ""
    assistant_text = ""
    
    # 根据意图生成槽位
    if intent["intent_name"] == "ConnectBlueTooth":
        device = random.choice(device_types)
        action = random.choice([True, False])
        slots_values = {"DeviceType": device, "ActionType": action}
        user_text = random.choice(intent["examples"]).format(DeviceType=device)
        assistant_text = f'ConnectBlueTooth(DeviceType="{device}", ActionType={action})'
    elif intent["intent_name"] == "ConnectWiFi":
        ssid = random.choice(wifi_ssid)
        pwd = f"{random.randint(10000000,99999999)}"
        slots_values = {"SSID": ssid, "Password": pwd}
        user_text = random.choice(intent["examples"]).format(SSID=ssid, Password=pwd)
        assistant_text = f'ConnectWiFi(SSID="{ssid}", Password="{pwd}")'
    elif intent["intent_name"] == "SetVPN":
        vpn = random.choice(vpn_names)
        action = random.choice([True, False])
        slots_values = {"VPNName": vpn, "ActionType": action}
        user_text = random.choice(intent["examples"]).format(VPNName=vpn)
        assistant_text = f'SetVPN(VPNName="{vpn}", ActionType={action})'
    elif intent["intent_name"] == "SetAppPermission":
        app = random.choice(app_names)
        perm = random.choice(permissions)
        action = random.choice([True, False])
        slots_values = {"AppName": app, "Permission": perm, "ActionType": action}
        user_text = random.choice(intent["examples"]).format(AppName=app, Permission=perm)
        assistant_text = f'SetAppPermission(AppName="{app}", Permission="{perm}", ActionType={action})'
    elif intent["intent_name"] == "SetLockScreen":
        action = random.choice([True, False])
        slots_values = {"ActionType": action}
        user_text = random.choice(intent["examples"])
        assistant_text = f'SetLockScreen(ActionType={action})'
    elif intent["intent_name"] == "SetPowerMode":
        mode = random.choice(modes)
        slots_values = {"Mode": mode}
        user_text = random.choice(intent["examples"]).format(Mode=mode)
        assistant_text = f'SetPowerMode(Mode="{mode}")'
    elif intent["intent_name"] == "CheckBatteryHealth":
        user_text = random.choice(intent["examples"])
        assistant_text = "CheckBatteryHealth()"
    elif intent["intent_name"] == "AdjustVolume":
        level = random.randint(0,100)
        slots_values = {"VolumeLevel": level}
        user_text = random.choice(intent["examples"]).format(VolumeLevel=level)
        assistant_text = f'AdjustVolume(VolumeLevel={level})'
    elif intent["intent_name"] == "SetNotification":
        app = random.choice(app_names)
        action = random.choice([True, False])
        slots_values = {"AppName": app, "ActionType": action}
        user_text = random.choice(intent["examples"]).format(AppName=app)
        assistant_text = f'SetNotification(AppName="{app}", ActionType={action})'
    elif intent["intent_name"] == "AdjustBrightness":
        level = random.randint(0,100)
        slots_values = {"BrightnessLevel": level}
        user_text = random.choice(intent["examples"]).format(BrightnessLevel=level)
        assistant_text = f'AdjustBrightness(BrightnessLevel={level})'
    elif intent["intent_name"] == "RestartDevice":
        user_text = random.choice(intent["examples"])
        assistant_text = "RestartDevice()"
    elif intent["intent_name"] == "UpdateSystem":
        user_text = random.choice(intent["examples"])
        assistant_text = "UpdateSystem()"
    elif intent["intent_name"] == "OpenApp":
        app = random.choice(app_names)
        slots_values = {"AppName": app}
        user_text = random.choice(intent["examples"]).format(AppName=app)
        assistant_text = f'OpenApp(AppName="{app}")'
    
    # 构建样例
    sample = {
        "id": str(uuid.uuid4()),
        "intent_name": intent["intent_name"],
        "intent_description": intent["desc"],
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

# 保存为 JSON
with open("train_data_50.json", "w", encoding="utf-8") as f:
    json.dump(samples, f, ensure_ascii=False, indent=2)

print("✅ 已生成 50 条训练数据，保存为 train_data_50.json")
