import os

from scrapy.http import HtmlResponse, Request

from ..spiders.fara import FaraSpider


def load_local_html_mock(page_file, page_location):
    request = Request(page_location)

    test_root = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(test_root, page_file)
    with open(path) as f:
        html_body = f.read()

    return HtmlResponse(
        page_location,
        request=request,
        body=html_body,
        encoding='utf-8'
    )


class TestFaraSpider:
    begin_url = 'https://efile.fara.gov/pls/apex/'
    test_exhibit_url = 'https://efile.fara.gov/pls/apex/f?p=185:200:0::NO:RP' \
                       ',200:P200_REG_NUMBER,P200_DOC_TYPE,P200_COUNTRY:' \
                       '2244,Exhibit%20AB,AFGHANISTAN'

    def test_form_data_setup(self):
        """Should correctly populate form data"""
        mock_response = load_local_html_mock('page.html',
                                             self.begin_url)

        spider = FaraSpider()

        actual_form_data = spider.get_form_data(mock_response)

        expected_form_data = {
            'p_request': 'APXWGT',
            'p_instance': '11656374762462',
            'p_flow_id': '185',
            'p_flow_step_id': '130',
            'p_widget_num_return': '653',
            'p_widget_name': 'worksheet',
            'p_widget_mod': 'ACTION',
            'p_widget_action': 'PAGE',
            'x01': '555215554758934859',
            'x02': '555216849652934863'
        }

        assert actual_form_data == expected_form_data

    def test_page_data(self):
        """
        Should correctly load data from the page.
        """
        mock_response = load_local_html_mock(
            'page.html', self.begin_url)

        spider = FaraSpider()
        page_data = spider.parse_principals(mock_response)
        main_page_first_result = next(page_data)

        actual = main_page_first_result.meta['principal']
        expected = {
            'url': self.test_exhibit_url,
            'foreign_principal': 'Islamic Republic of Afghanistan',
            'address': None,
            'state': None,
            'registrant': 'Hogan Lovells US LLP',
            'reg_num': '2244',
            'date': '2018-09-26T00:00:00-04:00',
            'country': 'AFGHANISTAN'}
        assert actual == expected
