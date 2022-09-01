"""Wake up mlbee service."""
from logzero import logger
from radio_mlbee_client import radio_mlbee_client
from tenacity import retry, stop_after_attempt


@retry(stop=stop_after_attempt(3))
def wakeup_mlbee(*args, **kwargs):
    """Wake up mlbee service.

    api_url: service api, if None, set to default url_hf
        https://hf.space/embed/mikeee/radio-mlbee/+/api/predict/
    """
    if not args:
        args = [
            "test 1 \n test2",
            "测试 1\n我爱你\n 更多测试",
        ]
    if len(args) < 2:
        args.append("测试 1\n我爱你\n 更多测试")

    try:
        # res = radio_mlbee_client(*args, **kwargs)
        # res = radio_mlbee_client(*args, **kwargs)
        res = radio_mlbee_client(
            *args,
            **kwargs,
        )
    except Exception as exc:
        logger.error(exc)
        raise

    # [['test 1', '测试 1', 0.96], ['', '我爱你', ''], ['test2', '更多测试', 0.55]]
    return res
