import jieba
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction


def calculate_bleu(candidate_text: str, reference_texts: list) -> float:
    """
    计算中文对话任务的 BLEU 分数。

    参数:
        candidate_text (str): 生成的文本。
        reference_texts (list): 参考文本列表（可以有多个参考句子）。

    返回:
        float: BLEU 分数。
    """
    # 对生成文本和参考文本进行分词
    candidate_tokens = list(jieba.cut(candidate_text))
    reference_tokens = [list(jieba.cut(ref)) for ref in reference_texts]

    # 使用 nltk 的 sentence_bleu 计算 BLEU 分数
    smoothing = SmoothingFunction().method1  # 避免分数为零
    bleu_score = sentence_bleu(reference_tokens, candidate_tokens,
                               weights=(0.25, 0.25, 0.25, 0.25),  # 1-gram 到 4-gram 的权重
                               smoothing_function=smoothing)

    return bleu_score


# 示例测试
if __name__ == "__main__":
    candidate = "今天天气很好，我们去公园玩吧"
    references = [# 参考句子, 可以有多个参考句子
        "今天天气很好，我们去公园玩吧",
    ]

    bleu = calculate_bleu(candidate, references)
    print(f"BLEU 分数: {bleu:.4f}")
    candidate = "今天天气太好啦，我们一起去公园玩吧"
    references = [  # 参考句子
        "今天天气很好，我们去公园玩吧",
    ]

    bleu = calculate_bleu(candidate, references)
    print(f"BLEU 分数: {bleu:.4f}")
