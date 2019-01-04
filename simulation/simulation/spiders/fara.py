import scrapy
from difflib import SequenceMatcher
from ..items import ActiveForeignPrincipalItem,ActiveForeignPrincipalLoader

from ..helpers.common import parse_date


class FaraSpider(scrapy.Spider):
    name = 'fara'
    allowed_domains = ['fara.gov']
    start_urls = ['https://efile.fara.gov/pls/apex/'
                  'f?p=185:130:0::NO:RP,130:P130_DATERANGE:N']
    form_data = None

    def parse(self, response):
        self.form_data = self.get_form_data(response)
        yield scrapy.FormRequest(
            'https://efile.fara.gov/pls/apex/wwv_flow.show',
            formdata=self.form_data,
            callback=self.parse_principals,
            dont_filter=True
        )

    def parse_principals(self, response):
        country_name = None
        for tr in response\
                .xpath('//table[@class="apexir_WORKSHEET_DATA"]/tr'):
            country_name_selector = \
                tr.xpath('th[1]/span[@class="apex_break_headers"]')
            if tr.xpath('th') and country_name_selector:
                country_name = country_name_selector\
                    .xpath('./text()').extract_first()
                continue

            # Skip this row if it has a header but no country name
            if tr.xpath('th') and not country_name_selector:
                continue

            if tr.xpath('td'):
                il = ActiveForeignPrincipalLoader(
                    ActiveForeignPrincipalItem(),
                    tr)

                il.add_value('country', country_name)
                il.add_xpath('foreign_principal', 'td[2]/text()')
                il.add_xpath('address', 'td[4]')
                il.add_xpath('state', 'td[5]/text()')
                il.add_xpath('registrant', 'td[6]/text()')
                il.add_xpath('reg_num', 'td[7]/text()')
                il.add_xpath('date', 'td[3]/text()')
                il.add_value('url', response
                             .urljoin(tr.xpath('td[1]/a/@href')
                                      .extract_first()))

                partial_result = il.load_item()
                yield scrapy.Request(
                    partial_result['url'],
                    meta={'principal': partial_result},
                    dont_filter=True,
                    callback=self.parse_exhibit_url)

    def parse_exhibit_url(self, response):
        principal = response.meta['principal']
        exhibits = []
        for tr in response\
                .xpath('//table[@class="apexir_WORKSHEET_DATA"]/tr'):
            if tr.xpath('td'):
                exhibit_date = parse_date(tr.xpath('td[1]/text()')
                                          .extract_first())
                exhibit_url = tr.xpath('td[2]/a/@href').extract_first()
                document_name = tr.xpath('td[2]/a/span/text()')\
                    .extract_first().strip()

                # A measure of the similarity of the exhibit
                # document name and foreign principle name
                match_weight = SequenceMatcher(
                    None,
                    document_name.lower(),
                    principal['foreign_principal'].lower()
                ).quick_ratio()

                if exhibit_date and exhibit_url:
                    exhibit = {
                        'document_name': document_name,
                        'date': exhibit_date,
                        'url': exhibit_url,
                        'match_weight': match_weight
                    }
                    exhibits.append(exhibit)
        principal['exhibit_url'] = self.get_best_match_exhibit(exhibits)
        print(principal)
        yield principal

    @staticmethod
    def get_best_match_exhibit(exhibits):
        if not exhibits:
            return None
        if len(exhibits) == 1:
            return exhibits[0]['url']
        # First sort by date
        sorted_exhibits_by_date = sorted(
            exhibits,
            key=lambda exhibit: exhibit['date'])

        # Lastly sort by match weight
        sorted_exhibits_by_weight = sorted(
            sorted_exhibits_by_date,
            key=lambda exhibit: exhibit['match_weight']
        )

        # The last one in the list is the most recent.
        return sorted_exhibits_by_weight[-1]['url']

    def get_form_data(self, response):
        # e.g. 1 - 15 of 652
        pagination_text = response\
            .xpath('//td[@class="pagination"]/span/text()')\
            .extract_first()

        # Placeholder
        total_principals = 1000
        try:
            if pagination_text:
                pagination_text_array = pagination_text.strip().split()

                # Last text is the total number of records.
                total_principals = pagination_text_array[-1]
        except Exception as e:
            raise e

        self.logger.info(f'Total records: {total_principals}')

        form_div = response.xpath('*//form[@id="wwvFlowForm"]')
        form_data = {
            'p_request': 'APXWGT',
            'p_instance':
                form_div.xpath('input[@name="p_instance"]/@value')
                .extract_first(),
            'p_flow_id': form_div
                .xpath('input[@name="p_flow_id"]/@value')
                .extract_first(),
            'p_flow_step_id': form_div
                .xpath('input[@name="p_flow_step_id"]/@value')
                .extract_first(),
            'p_widget_num_return': total_principals,
            'p_widget_name': 'worksheet',
            'p_widget_mod': 'ACTION',
            'p_widget_action': 'PAGE',
            'x01': response
                .xpath('*//input[@id="apexir_WORKSHEET_ID"]/@value')
                .extract_first(),
            'x02': response
                .xpath('*//input[@id="apexir_REPORT_ID"]/@value')
                .extract_first()
        }
        return form_data
