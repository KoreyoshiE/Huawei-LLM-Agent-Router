import json
import copy

# 读取训练数据
with open("train_data_50.json", "r", encoding="utf-8") as f:
    train_samples = json.load(f)

smoke_tests = []

for sample in train_samples:
    # 单轮-单指令
    single_turn = copy.deepcopy(sample)
    single_turn["eval_type"] = "single_turn"
    smoke_tests.append(single_turn)
    
    # 多轮-单指令
    multi_turn = copy.deepcopy(sample)
    multi_turn["eval_type"] = "multi_turn"
    
    # 添加模拟对话上下文
    user_prev = {"role": "user", "content": "请帮我处理一些设备设置。"}
    assistant_prev = {"role": "assistant", "content": "好的，请告诉我具体操作。"}
    multi_turn["data"] = [user_prev, assistant_prev] + multi_turn["data"]
    smoke_tests.append(multi_turn)

# 保存评测冒烟集
with open("smoke_test_100.json", "w", encoding="utf-8") as f:
    json.dump(smoke_tests, f, ensure_ascii=False, indent=2)

print("✅ 已生成评测冒烟集 100 条，保存为 smoke_test_100.json")
