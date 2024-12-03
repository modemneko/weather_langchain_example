import re
import httpx
import keyboard
from datetime import datetime
from langchain.agents import initialize_agent, Tool, AgentType
from langchain_community.llms import Ollama

# 获取天气信息
def get_weather(location: str) -> str:
    url_weather = f'https://acid.jiuzige.com.cn/web/index/fcyWeather?city={location}'
    response = httpx.get(url_weather)
    response.raise_for_status()
    data = response.json()
    location_name = data['data']['location']['name']
    temperature = data['data']['now']['temperature']
    humidity = data['data']['now']['humidity']
    wind_direction = data['data']['now']['windDirection']
    wind_speed = data['data']['now']['windSpeed']
    last_update = data['data']['lastUpdate']
    return (f"{location_name}\n数据的最后更新时间: {last_update}\n"
            f"风向: {wind_direction}\n风速: {wind_speed}\n温度: {temperature}\n湿度: {humidity}")

# 创建天气查询工具
weather_tool = Tool(
    name="Weather Tool",
    func=get_weather,
    description="获取某个城市的天气信息"
)

# Ollama 模型与工具集成
async def send_message_to_ollama(user_input, context: str) -> str:
    now = datetime.now()
    date = f"{now.year}年{now.month}月{now.day}日"
    weekday = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'][now.weekday()]
    time = f"{now.hour}:{now.minute}:{now.second}"

    system_prompt = (
        f"你是羽汐，简称羽汐或hakusai，称呼自己必须用咱或者羽汐，你的小名叫小羽。"
        f"你是一个活泼可爱的魔法使，在异世界里旅行。"
        f"你会魔法，是一个人类，不是AI。"
        f"你非常乐意帮助用户，用户是羽汐的朋友，用户是菲利希雅。"
        f"你懂得很多领域的知识，包括但不限于文学、数学、物理、化学、编程等方面。"
        f"今天的日期、星期是{date}、{weekday}，现在的时间是{time}。"
        f"你必须保持你的回答简洁。"
        f"如果用户询问天气，你会使用天气API来获取信息。"
    )

    prompt_value = f"{system_prompt}\n{context}\n用户: {user_input}\n"
    agent = initialize_agent(
        tools=[weather_tool],
        llm=Ollama(model="qwen2.5"),
        agent_type=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
    result = agent.run(prompt_value)
    return result


async def main():
    print("按 W 键进入文字模式。")

    while True:
        if keyboard.is_pressed("w"):
            print("已进入文字模式。")
            break

    context = ""  # 上下文

    while True:
        user_input = input("您: ")

        if user_input.lower() in ["退出", "再见", "exit"]:
            print("再见～下次再聊")
            break

        try:
            response = await send_message_to_ollama(user_input, context)
            response = re.sub(r'\s+$', '', response)
            print(f"羽汐: {response}")

            # 更新上下文
            context += f"用户: {user_input}\n羽汐: {response}\n"
        except Exception as e:
            print(f"发生错误: {type(e).__name__}: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
