
import os

os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

from transformers import pipeline
from tqdm import tqdm
import torch

from codecon.utils.FileReader import FileReader


def cl_nlp(data_pred, method = 'financial_sentiment', language = 'chn'):

    dataloader = FileReader(data_pred = data_pred)
    df = dataloader.read_pred_file()
    texts = df['text'].astype(str).tolist()


    chn_pipline_dic = {
        'financial_sentiment': ['bardsai/finance-sentiment-zh-base', 'label', 'score'],
        'reviews_sentiment': ['liam168/c2-roberta-base-finetuned-dianping-chinese', 'label', 'score'],
        'guwen_sentiment': ['ethanyt/guwen-sent', 'label', 'score'],
        'news_classification': ['myml/toutiao', 'label', 'score']
    }

    eng_pipline_dic = {
        'financial_sentiment': ['ProsusAI/finbert', 'label', 'score'],
        'reviews_sentiment': ['cardiffnlp/twitter-roberta-base-sentiment-latest', 'label', 'score'],
        'news_classification': ['cardiffnlp/tweet-topic-21-multi', 'score', 'label']
    }

    if language == 'chn':
        try:
            select_model = chn_pipline_dic[method][0]
        except:
            print('模型名称错误，或者codecon还未收录该模型')
    elif language == 'eng':
        try:
            select_model = eng_pipline_dic[method][0]
        except:
            print('模型名称错误，或者codecon还未收录该模型')
    else:
        raise ValueError("语言选择错误")

    # Print the selected model
    print(f"使用模型: {select_model}")

    # Initialize the pipeline with truncation and max_length set to 512
    device = 0 if torch.cuda.is_available() else -1
    print('如果这是你第一次使用这个方法，需要下载预训练模型，这可能需要一会儿....')
    model = pipeline(model=select_model, truncation=True, max_length=512, device = device)
    print('模型下载完毕，开始处理数据...')

    # Use tqdm to track progress
    texts_label = []
    texts_score = []

    for txt in tqdm(texts, desc="Processing texts"):
        try:
            # Perform prediction for each text
            result = model(txt)
            texts_label.append(result[0]['label'])
            texts_score.append(result[0]['score'])
        except Exception as e:
            # Handle any errors gracefully
            texts_label.append(None)
            texts_score.append(None)
            print(f"在处理一段文本时出现异常，该文本对应label将输出为空值。异常为 {str(e)}")

    df[f"{method}_label"] = texts_label
    df[f"{method}_score"] = texts_score

    directory = os.path.dirname(data_pred)
    output_path = os.path.join(directory, f'pred_results_{method}.csv')
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"预测结果已保存至：{output_path}")

    return df