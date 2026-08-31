import requests
from config import Config
import logging

logger = logging.getLogger(__name__)

def query_selected_course(session, xn=None, xq=None):
    """
    查询已选课程信息
    """

    logger.info(f'当前session对象的cookies:{session.cookies.get_dict()}')

    # 默认设置为当前学期，在.env中修改
    xn = Config.XN
    xq = Config.XQ
    xnxq = xn.replace('-', '') + xq

    # 构建请求负载
    payload = {
        'cxsfmt': '0',
        'p_pylx': '1',
        'mxpylx': '1',
        'p_sfgldjr': '0',
        'p_sfredis': '0',
        'p_sfsyxkgwc': '0',
        'p_xktjz': '',
        'p_chaxunxh': '',
        'p_gjz': '',
        'p_skjs': '',
        'p_xn': xn,
        'p_xq': xq,
        'p_xnxq': xnxq,
        'p_dqxn': xn,
        'p_dqxq': xq,
        'p_dqxnxq': xnxq,
        'p_xkfsdm': 'yixuan',
        'p_xiaoqu': '',
        'p_kkyx': '',
        'p_kclb': '',
        'p_xkxs': '',
        'p_dyc': '',
        'p_kkxnxq': '',
        'p_id': '',
        'p_sfhlctkc': '0',
        'p_sfhllrlkc': '0',
        'p_kxsj_xqj': '',
        'p_kxsj_ksjc': '',
        'p_kxsj_jsjc': '',
        'p_kcdm_js': '',
        'p_kcdm_cxrw': '',
        'p_kcdm_cxrw_zckc': '',
        'p_kc_gjz': '',
        'p_xzcxtjz_nj': '',
        'p_xzcxtjz_yx': '',
        'p_xzcxtjz_zy': '',
        'p_xzcxtjz_zyfx': '',
        'p_xzcxtjz_bj': '',
        'p_sfxsgwckb': '1',
        'p_skyy': '',
        'p_sfmxzj': '',
        'p_chaxunxkfsdm': '',
        'pageNum': '1',
        'pageSize': '200',
        }

    # 更新请求头
    session.headers.update({
        'Refer': Config.TIS_BASE + '/Xsxk/query/1',
        'X-Requested-With': 'XMLHttpRequest',
        'RoleCode': '01',
        'Origin': Config.TIS_BASE,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36 Edg/152.0.0.0',
        })

    try:
        logger.info("正在查询已选课程信息")
        resp = session.post(Config.QUERY_YXKC_URL, data=payload)
        resp.raise_for_status()
        data = resp.json()

        if data:
            courses = data['yxkcList']
            logger.info(f'查询到{len(courses)}门课程')
            return courses
        else:
            logger.info(resp.text)
            raise Exception(f"未知的相应格式")
    except Exception as e:
        logger.error(f'查询过程遇到错误: {e}')
        with open('resp.txt', 'w', encoding='utg-8') as f:
                f.write(resp.text)
        if Config.DEBUG:
            logger.dubug(resp.text[:500])
        raise