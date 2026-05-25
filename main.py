# main.py
import json
from agent import CustomAgent

if __name__ == "__main__":
    agent = CustomAgent()
    print("Model loaded successfully!\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        response = agent.chat(user_input)
        print(f"AI: {response}\n")

def run_interactive(agent):
    """交互模式：用户输入，模型生成响应"""
    print("输入 exit 退出交互模式")
    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            break
        response = agent.run([{"role": "user", "content": user_input}])
        print(f"AI: {response}")

def run_smoke_test(agent, filename):
    """冒烟集批量测试"""
    with open(filename, "r", encoding="utf-8") as f:
        test_cases = json.load(f)
    
    print(f"开始冒烟集测试，共 {len(test_cases)} 条指令...")
    success_count = 0
    
    for case in test_cases:
        user_msgs = case["data"]
        # 取用户发起的第一条消息
        user_content = [{"role": msg["role"], "content": msg["content"]} for msg in user_msgs if msg["role"]=="user"]
        expected = [msg["content"] for msg in user_msgs if msg["role"]=="assistant"]
        response = agent.run(user_content)
        
        # 简单对比是否包含预期输出
        if any(exp in response for exp in expected):
            success_count += 1
        else:
            print(f"❌ 测试未通过\n输入: {user_content}\n输出: {response}\n预期包含: {expected}\n")
    
    print(f"冒烟集完成，通过率: {success_count}/{len(test_cases)} = {success_count/len(test_cases):.2%}")

if __name__ == "__main__":
    # 初始化 Agent
    agent = CustomAgent()

    mode = input("选择模式: 1-交互模式  2-冒烟集测试: ").strip()
    if mode == "1":
        run_interactive(agent)
    elif mode == "2":
        run_smoke_test(agent, "data/smoke_test_100.json")
    else:
        print("无效选项，程序退出")
