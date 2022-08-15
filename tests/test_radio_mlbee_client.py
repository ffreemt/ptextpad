"""Test  radio_mlbee_client

radio_mlbee_client('test 1 \n test2', "测试 1\n我爱你\n 更多测试")
[['test 1', '测试 1', 0.96], ['', '我爱你', ''], ['test2', '更多测试', 0.55]]
"""
from radio_mlbee_client import radio_mlbee_client


def test_radio_mlbee_client():
    """Test radio_mlbee_client simple."""
    res = radio_mlbee_client('test 1 \n test2', "测试 1\n我爱你\n 更多测试")
    assert res[0][2] > 0.9
    assert res[2][2] > 0.5
