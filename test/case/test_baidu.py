import time
import unittest
from utils.config import Config, DRIVER_PATH, DATA_PATH, REPORT_PATH
from utils.log import logger
from utils.file_reader import ExcelReader
from utils.HTMLTestRunner import HTMLTestRunner
from utils.mail import Email
from test.page.baidu_result_page import BaiDuMainPage, BaiDuResultPage

class TestBaiDu(unittest.TestCase):
    URL = Config().get('URL')
    excel = DATA_PATH + '/baidu.xlsx'

    def sub_setUp(self):
        self.page = BaiDuMainPage(browser_type='chrome').get(self.URL, maximize_window=False)

    def sub_tearDown(self):
        self.page.quit()

    def test_search(self):
        datas = ExcelReader(self.excel).data
        for d in datas:
            with self.subTest(data=d):    #在测试用例中使用subTest()重复测试某个用例
                self.sub_setUp()
                self.page.search(d['search'])
                time.sleep(2)
                self.page = BaiDuResultPage(self.page)  # 页面跳转到result page
                links = self.page.result_links
                for link in links:
                    logger.info(link.text)
                self.sub_tearDown()

if __name__ == '__main__':
    report = REPORT_PATH + '\\report.html'
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='从0搭建测试框架 灰蓝', description='修改html报告')
        runner.run(TestBaiDu('test_search'))

        # e = Email(title='百度搜索测试报告',
        #           message='这是今天的测试报告，请查收！',
        #           receiver='18151032084@163.com',
        #           server='smtp.163.com',
        #           sender='18151032084@163.com',
        #           password='xmxel9516.',
        #           path=report
        #           )
        # e.send()

