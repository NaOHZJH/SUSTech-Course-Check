import requests
from bs4 import BeautifulSoup
from config import Config
import logging

logger = logging.getLogger(__name__)

def cas_login(username, password):
    """
    模拟CAS登录，返回已认证的requests.Session对象
    """

    logger.debug(f'当前使用的用户名：{Config.USERNAME}, 当前使用的密码：{Config.PASSWORD}')

    session = requests.Session()

    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36 Edg/152.0.0.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })

    try:
        # GET登录页面，获取execution
        logger.info("正在获取登录页面...")
        resp = session.get(Config.CAS_LOGIN_URL)
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text, 'lxml')
        execution_input = soup.find('input', {'name': 'execution'})
        if not execution_input:
            raise Exception("未获取到execution值")

        execution_value = execution_input.get('value')

        # 构造登陆数据
        login_data = {
            'username': Config.USERNAME,
            'password': Config.PASSWORD,
            'execution': execution_value,
            '_eventId': 'submit',
            }

        # POST登录数据
        logger.info("提交登录数据")
        login_resp = session.post(Config.CAS_LOGIN_URL, data=login_data, allow_redirects=True)
        login_resp.raise_for_status()
        logger.debug(login_resp.text[:500])
        logger.debug(login_resp.url)

        # 检查登录状态并返回session
        if 'tis.sustech.edu.cn' in login_resp.url:
            logger.info('CAS登录成功')
            return session
        else:
            raise Exception(f"登录过程异常：{e}")

    except Exception as e:
        logger.error(f'登录过程异常：{e}')
        raise