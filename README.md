# chatengine goal

The chatengine provide a way to init and start the chat web system with several type of LLMs. which can run only of the major public cloud.

The init ideal is to support the following models:

1. LLama 2 chat
2. Qwen
3. GPT3, GPT4


The major cloud provider include:

1. Amazon public cloud
2. Google cloud
3. Aliyun

# why to do

As far as we know there are more and more LLMs published recent months, some of them provided the public api, 
others publish the code and weights.however, each one has its own visit link and style, it is hard to combine 
them into one UI, for the following cases:

1. compare the two LLMs with the same context and prompt.
2. to get more options.
3. chat each others to make a sence design.
4. prompt optimization.


# Get Started

install the requirements

```
pip install -r requirements.txt

```

start the server

```
python server.py --model_path "meta-llama/Llama-2-7b-chat-hf" --server_name "0.0.0.0"
```

note: remove the 'server_name' parameter if run on localhost.


# Status


This repository is under development. it may occur error when trying to run it, please feel free to open issue if any question.

