import openai


from file_utils import load_gpt_conf


gpt_conf = load_gpt_conf()
api_base = gpt_conf['api_base']
api_key = gpt_conf['api_key']

# openai.log = "debug"
openai.api_key = api_key
openai.api_base = api_base



def gpt_35_api_completion(messages: list, model='gpt-3.5-turbo-0613'):
    """为提供的对话消息创建新的回答

    Args:
        messages (list): 完整的对话消息
        api_key (str): OpenAI API 密钥
    Returns:
        str: 回答内容
    """
    try:
        completion = openai.ChatCompletion.create(
            model=model, 
            messages=messages
        )
        return completion.choices[0].message.content
    except Exception as err:
        return f'OpenAI API 异常: {err}'


def gpt_35_api_stream(messages: list, model='gpt-3.5-turbo-0613'):
    """为提供的对话消息创建新的回答 (流式传输)

    Args:
        messages (list): 完整的对话消息
        api_key (str): OpenAI API 密钥

    Returns:
        tuple: (results, error_desc)
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            stream=True,
        )
        completion = {'role': '', 'content': ''}
        for event in response:
            if event['choices'][0]['finish_reason'] == 'stop':
                print(f'收到的完成数据: {completion}')
                break
            for delta_k, delta_v in event['choices'][0]['delta'].items():
                print(f'流响应数据: {delta_k} = {delta_v}')
                completion[delta_k] += delta_v
        messages.append(completion)  # 直接在传入参数 messages 中追加消息
        return (True, '')
    except Exception as err:
        return (False, f'OpenAI API 异常: {err}')


def get_models():
    """列出所有可用模型

    Returns:
        list: 模型列表
    """
    try:
        models = openai.Model.list()
        models = [model['id'] for model in models['data']]
        return models
    except Exception as err:
        return [f'OpenAI API 异常: {err}']


if __name__ == '__main__':
    # model = 'gpt-3.5-turbo-0613'
    # messages = [{'role': 'user','content': '你好'},]

    # # print(gpt_35_api_completion(messages))
    # gpt_35_api_stream(messages)

    # 列出所有可用模型
    models = openai.Model.list()
    models = [model['id'] for model in models['data']]

    print(models)
    


