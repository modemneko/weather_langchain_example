# weather_langchain_example
一个利用Langchain agents实现天气查询LLM的简单用例  
具体实现方法可以看代码  
# First
使用Ollama作为LLM Models，需要先安装好Ollama  
  
拉取qwen2.5模型作为测试模型（个人觉得效果还行）：    
`ollama pull qwen2.5`  
  
然后安装需要用到的库：  
`pip install -U langchain langchain-community httpx`  

# Second
运行 `weather_agents.py`   
