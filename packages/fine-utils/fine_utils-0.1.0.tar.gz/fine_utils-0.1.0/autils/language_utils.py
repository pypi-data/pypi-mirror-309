import asyncio
import functools
import json
import sys
from functools import partial

from async_lru import alru_cache
from deep_translator import GoogleTranslator
from fast_langdetect import detect
from langchain_core.messages import HumanMessage, SystemMessage
from langdetect import detect_langs
from pytictoc import TicToc

from src.core.ais import get_llm
from src.core.standards.logger import logger

# 缓存配置
CACHE_SIZE = 1000

# 翻译服务配置
TRANSLATORS = {
    "azure_gpt": lambda: get_llm("gpt-4-assistant"),  # 使用我们自己的 Azure OpenAI 配置
    "google": lambda: GoogleTranslator(),  # 作为备选的免费服务
}

# 添加支持的语言列表
SUPPORTED_LANGUAGES = {
    "en": "English",
    "fr": "French",
    "it": "Italian",
    "pt": "Portuguese",
    "de": "German",
    "tr": "Turkish",
    "vi": "Vietnamese",
    "zh-CN": "Simplified Chinese",
    "zh-TW": "Traditional Chinese",
    "ja": "Japanese",
    "ko": "Korean"
}


def tictoc(func):
    """同步函数计时装饰器"""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t = TicToc()
        t.tic()
        result = func(*args, **kwargs)
        t.toc(f"{func.__name__}")
        return result

    return wrapper


def async_tictoc(func):
    """异步函数计时装饰器"""

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        t = TicToc()
        t.tic()
        result = await func(*args, **kwargs)
        t.toc(f"{func.__name__}")
        return result

    return wrapper


async def run_sync(func, *args, **kwargs):
    """运行同步函数"""
    if sys.version_info >= (3, 9):
        return await asyncio.to_thread(func, *args, **kwargs)
    else:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, partial(func, *args, **kwargs))


@alru_cache(maxsize=CACHE_SIZE)
async def detect_language(text: str) -> str:
    """
    检测文本语言
    :param text: 待检测文本
    :return: 语言代码 (en, zh, ja, etc.)
    """
    try:
        # 预处理文本
        text = text.replace("\n", " ").strip()

        # 使用 fast_langdetect
        result = await run_sync(detect, text)
        if result["score"] >= 0.8:
            lang = result["lang"]
        else:
            # 使 langdetect 作为备选
            langs = await run_sync(detect_langs, text)
            lang = langs[0].lang

        # 统一中文代码
        if lang.startswith("zh"):
            return "zh"

        return lang

    except Exception as e:
        logger.error(f"Language detection failed: {e}")
        return "en"  # 默认返回英语


async def translate_with_service(
    text: str,
    target_lang: str,
    source_lang: str | None = None,
    service: str = "azure_gpt",  # 默认使用 Azure GPT
    timeout: int = 30,  # 添加超时参数
) -> str | None:
    """使用指定服务翻译文本"""
    try:
        # 创建一个任务
        async def translation_task(target: str = target_lang):  # 将 target_lang 作为参数传入
            translator_factory = TRANSLATORS.get(service)
            if not translator_factory:
                logger.error(f"Unsupported translation service: {service}")
                return None

            if service == "google":
                translator = translator_factory()
                # 复制一个新的目标语言变量
                google_target = target
                if google_target == "zh-CN":
                    google_target = "zh-cn"
                elif google_target == "zh-TW":
                    google_target = "zh-tw"
                result = await run_sync(translator.translate, text, target=google_target)
            else:  # Azure GPT translator
                llm = translator_factory()
                messages = [
                    SystemMessage(
                        content=f"You are a professional translator. Translate the following text to {target}. Keep the translation accurate and natural."
                    ),
                    HumanMessage(content=text),
                ]
                response = await llm.ainvoke(messages)
                result = response.content
            return result

        # 使用 asyncio.wait_for 添加超时控制
        return await asyncio.wait_for(translation_task(), timeout=timeout)

    except asyncio.TimeoutError:
        logger.error(f"Translation timed out after {timeout} seconds with {service}")
        return None
    except Exception as e:
        logger.error(f"Translation failed with {service}: {e}")
        return None


@alru_cache(maxsize=CACHE_SIZE)
async def translate_to_language(text: str, target_lang: str, retries: int = 3) -> str:
    """
    增强的翻译功能，优先使用 ChatGPT，失败时使用 Google Translate
    :param text: 待翻译文本
    :param target_lang: 目标语言
    :param retries: 重试次数
    :return: 翻译后的文本
    """
    if not text.strip():
        return text

    source_lang = await detect_language(text)
    if source_lang == target_lang:
        return text

    # 优先使用 ChatGPT，失败使用 Google Translate
    services = ["azure_gpt", "google"]

    for attempt in range(retries):
        for service in services:
            try:
                result = await translate_with_service(
                    text, target_lang, source_lang, service
                )
                if result:
                    logger.info(f"Successfully translated with {service}")
                    return result
            except Exception as e:
                logger.error(
                    f"Translation attempt {attempt + 1} with {service} failed: {e}"
                )
                continue

        if attempt < retries - 1:
            await asyncio.sleep(1)  # 重试前等待

    logger.error(f"All translation attempts failed for text: {text}")
    return text  # 所有尝试都失败时返回原文


async def detect_language_with_confidence(text: str) -> tuple[str, float]:
    """
    使用多种服务检测语言并返回置信度
    :param text: 要检测的文本
    :return: (语言代码, 置信度)

    1. 多层检测策略：
        首先使用 GPT 进行高质量检测
        然后使用 fast_langdetect 作为快速备选
        最后使用 langdetect 作为保底方案

    2. 置信度处理：
        GPT 提供的置信度直接使用
        fast_langdetect 的 score 作为置信度
        langdetect 的概率值经过归一化处理

    3. 错误处理：
        完善的错误处理和日志记录
        服务降级机制
        默认返回值处理

    4. API 设计：
        简单明了的接口
        详细的响应信息
        符合 REST 规范
    """
    try:
        # 预处理文本
        text = text.replace("\n", " ").strip()

        # 1. 首先使用 GPT 检测
        llm = TRANSLATORS["azure_gpt"]()
        messages = [
            SystemMessage(
                content="""You are a language detection expert. Detect the language of the following text and return ONLY a JSON with two fields:
            'language_code' (ISO 639-1 code, for Chinese use 'zh-CN' for Simplified Chinese or 'zh-TW' for Traditional Chinese) and 'confidence' (0-1).
            You must differentiate between Simplified Chinese (zh-CN) and Traditional Chinese (zh-TW) based on the characters used.
            Example for Simplified Chinese: {"language_code": "zh-CN", "confidence": 0.95}
            Example for Traditional Chinese: {"language_code": "zh-TW", "confidence": 0.95}"""
            ),
            HumanMessage(content=text),
        ]

        try:
            response = await llm.ainvoke(messages)
            content = response.content
            if "```" in content:
                content = (
                    content.replace("```", "").replace("```", "").replace("json", "")
                )
            result = json.loads(content)
            if result.get("confidence", 0) > 0.8:
                return result["language_code"], result["confidence"]
            else:
                return "en", 0.5
        except Exception as e:
            logger.error(f"GPT language detection failed: {e}")

        # 2. 使用 fast_langdetect 作为备选
        result = await run_sync(detect, text)
        if result["score"] >= 0.5:
            lang = result["lang"]
            score = result["score"]

            # 改进中文检测逻辑
            if lang.startswith("zh"):
                # 使用字符特征判断简繁体
                traditional_chars = "繁體國說壹貳參肆伍陸柒捌玖拾"
                simplified_chars = "繁体国说一二三四五六七八九十"
                trad_count = sum(1 for char in text if char in traditional_chars)
                simp_count = sum(1 for char in text if char in simplified_chars)
                lang = "zh-TW" if trad_count > simp_count else "zh-CN"

            return lang, score

        # 3. 使用 langdetect 作为最后的备选
        langs = await run_sync(detect_langs, text)
        if langs:
            lang = langs[0].lang
            confidence = min(langs[0].prob + 1, 1.0)

            # 同样改进中文检测逻辑
            if lang.startswith("zh"):
                traditional_chars = "繁體國說壹貳參肆伍陸柒捌玖拾"
                simplified_chars = "繁体国说一二四五六七八九十"
                trad_count = sum(1 for char in text if char in traditional_chars)
                simp_count = sum(1 for char in text if char in simplified_chars)
                lang = "zh-TW" if trad_count > simp_count else "zh-CN"

            return lang, confidence

    except Exception as e:
        logger.error(f"Language detection failed: {e}")
        return "en", 0.5  # 默认返回英语，低置信度


@alru_cache(maxsize=CACHE_SIZE)
async def translate_to_all_languages(
    text: str,
    is_key_value: bool = False,
    target_languages: tuple[str, ...] | None = None
) -> dict[str, dict[str, str]] | dict[str, str]:
    """
    将文本翻译成指定的语言列表，并包含源语言文本
    """
    try:
        # 处理 key:value 格式
        if is_key_value and ":" in text:
            key, raw_text = text.split(":", 1)
            key = key.strip()
            raw_text = raw_text.strip()
        else:
            key = None
            raw_text = text.strip()

        # 检测原文语言
        source_lang, confidence = await detect_language_with_confidence(raw_text)
        logger.info(f"Detected language: {source_lang} with confidence: {confidence}")

        # 初始化结果字典，先添加源语言文本
        translations = {
            source_lang: raw_text  # 添加源语言文本
        }

        # 确定要翻译的目标语言列表
        languages_to_translate = (
            target_languages if target_languages is not None
            else tuple(SUPPORTED_LANGUAGES.keys())
        )

        # 验证目标语言的有效性
        invalid_langs = [lang for lang in languages_to_translate if lang not in SUPPORTED_LANGUAGES]
        if invalid_langs:
            logger.warning(f"Unsupported languages found: {invalid_langs}")
            languages_to_translate = tuple(lang for lang in languages_to_translate if lang in SUPPORTED_LANGUAGES)

        # 对每种目标语言进行翻译（跳过源语言，因为已经添加）
        for target_lang in languages_to_translate:
            if target_lang == source_lang:
                continue  # 跳过源语言，因为已经添加过了
            try:
                translated_text = await translate_to_language(raw_text, target_lang)
                translations[target_lang] = translated_text
            except Exception as e:
                logger.error(f"Failed to translate to {target_lang}: {e}")
                translations[target_lang] = raw_text  # 翻译失败时使用原文

            # 添加日志记录
            logger.info(f"Translated to {target_lang}: {translations[target_lang]}")

        # 根据是否是 key:value 格式返回不同的结果结构
        if key:
            return {key: translations}
        return translations

    except Exception as e:
        logger.error(f"Translation to languages failed: {e}")
        if key:
            return {key: {lang: text for lang in languages_to_translate}}
        return {lang: text for lang in languages_to_translate}


@alru_cache(maxsize=CACHE_SIZE)
async def translate_json_content_cached(
    content_str: str,
    is_nested: bool = False,
    target_languages: tuple[str, ...] | None = None,
    timeout: int = 60,  # 添加总体超时控制
) -> dict:
    """翻译 JSON 格式的内容到指定的语言（缓存版本）"""
    try:
        # 使用 asyncio.wait_for 添加总体超时控制
        async def translation_task():
            content = json.loads(content_str)
            result = {}
            tasks = []

            # 创建所有翻译任务
            for key, value in content.items():
                if isinstance(value, dict) and not is_nested:
                    task = translate_json_content(
                        value,
                        is_nested=True,
                        target_languages=target_languages
                    )
                    tasks.append((key, task))
                elif isinstance(value, str):
                    task = translate_to_all_languages(
                        value,
                        target_languages=target_languages
                    )
                    tasks.append((key, task))
                else:
                    result[key] = value

            # 并发执行所有翻译任务
            for key, task in tasks:
                try:
                    result[key] = await asyncio.wait_for(task, timeout=30)  # 单个任务超时控制
                except asyncio.TimeoutError:
                    logger.error(f"Translation for key {key} timed out")
                    result[key] = content[key]  # 超时时使用原始值
                except Exception as e:
                    logger.error(f"Translation for key {key} failed: {e}")
                    result[key] = content[key]  # 失败时使用原始值

            return result

        return await asyncio.wait_for(translation_task(), timeout=timeout)

    except asyncio.TimeoutError:
        logger.error(f"JSON translation timed out after {timeout} seconds")
        return json.loads(content_str)  # 返回原始内容
    except Exception as e:
        logger.error(f"JSON translation failed: {e}")
        return json.loads(content_str)  # 返回原始内容


async def translate_json_content(
    content: dict | str,
    target_languages: tuple[str, ...] | None = None,
    is_nested: bool = False,
    timeout: int = 60,  # 添加超时参数
) -> dict:
    """翻译 JSON 格式的内容到指定的语言"""
    try:
        # 将输入内容转换为 JSON 字符串
        if isinstance(content, dict):
            content_str = json.dumps(content, sort_keys=True)
        else:
            content_str = content

        # 调用缓存版本的函数
        return await translate_json_content_cached(
            content_str,
            is_nested=is_nested,
            target_languages=target_languages,
            timeout=timeout
        )

    except Exception as e:
        logger.error(f"JSON translation failed: {e}")
        return content


# 使用示例
async def example_usage():
    # 指定要翻译的语言列表
    target_langs = (
        "fr",     # 法语
        "it",     # 意大利语
        "pt",     # 葡萄牙语
        "de",     # 德语
        "tr",     # 土耳其语
        "vi",     # 越南语
        "zh-CN",  # 简体中文
        "zh-TW",  # 繁体中文
        "ja",     # 日语
        "ko",     # 韩语
    )

    # 示例1: 普通文本翻译（指定语言）
    text = "This is HashKey Bot, I am here at your service, how can I help you today?"
    result = await translate_to_all_languages(text, target_languages=target_langs)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 示例2: JSON 格式翻译（指定语言）
    simple_json = {
        "solved": "Thank you! My issue has been resolved.",
        "apply_human": "A human agent will assist you shortly."
    }
    result = await translate_json_content(simple_json, target_languages=target_langs)
    print(json.dumps(result, indent=2, ensure_ascii=False))

async def example_json_usage():
    # 示例1: 简单的 JSON 格式
    simple_json = {
        "solved": "Thank you! My issue has been resolved.",
        "apply_human": "A human agent will assist you shortly.",
        "more_help": "Please let us know how we can assist further."
    }
    result = await translate_json_content(simple_json)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 示例2: 嵌套的 JSON 格式
    nested_json = {
        "greetings": {
            "welcome": "Welcome to HashKey support!",
            "goodbye": "Thank you for using our service!"
        },
        "errors": {
            "not_found": "Resource not found",
            "server_error": "Internal server error"
        }
    }
    result = await translate_json_content(nested_json)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    # 示例3: JSON 字符串输入
    json_str = '''
    {
        "feedback": {
            "question": "Did this answer your question?",
            "options": {
                "yes": "Yes",
                "no": "No",
                "need_human": "I need human help"
            }
        }
    }
    '''
    result = await translate_json_content(json_str)
    print(json.dumps(result, indent=2, ensure_ascii=False))

# 保留其他辅助函数...

async def zendesk_trans():
    target_langs = (
        "fr",     # 法语
        "it",     # 意大利语
        "pt",     # 葡萄牙语
        "de",     # 德语
        "tr",     # 土耳其语
        "vi",     # 越南语
        "zh-CN",  # 简体中文
        "zh-TW",  # 繁体中文
        "ja",     # 日语
        "ko",     # 韩语
    )

    # 示例1: 普通文本翻译（指定语言）
    text = "This is HashKey Bot, I am here at your service, how can I help you today?"
    result = await translate_to_all_languages(text, target_languages=target_langs)
    print(json.dumps(result, indent=2, ensure_ascii=False))



async def zendesk_trans_2():
    """示例用法"""
    target_langs = (
        "fr",     # 法语
        "it",     # 意大利语
        "pt",     # 葡萄牙语
        "de",     # 德语
        "tr",     # 土耳其语
        "vi",     # 越南语
        "zh-CN",  # 简体中文
        "zh-TW",  # 繁体中文
        "ja",     # 日语
        "ko",     # 韩语
    )

    simple_json = {
        "solved": "Thank you! My issue has been resolved.",
        # "apply_human": "A human agent will assist you shortly.",
        # "more_help": "Please let us know how we can assist further.",
        # "feedback_question": "Did this answer your question?",
        # "feedback_no": "No",
        # "feedback_ok": "Yes",
        # "feedback_ask_human": "I need human help",
    }

    logger.info("Starting translation...")
    try:
        result = await translate_json_content(
            content=simple_json,
            target_languages=target_langs,
            timeout=120  # 设置较长的超时时间用于测试
        )
        print(json.dumps(result, indent=2, ensure_ascii=False))
        logger.info("Translation completed successfully")
    except Exception as e:
        logger.error(f"Translation failed: {e}")


if __name__ == "__main__":
    asyncio.run(zendesk_trans())
    # asyncio.run(zendesk_trans_2())
