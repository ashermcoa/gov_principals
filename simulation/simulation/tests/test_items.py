from ..items import (
    ActiveForeignPrincipalItem,
    ActiveForeignPrincipalLoader
)


class TestActiveForeignPrincipalItem:
    def test_item_loader(self):
        """Should output correct result"""
        mock_test = {
            'country': "Indonesia",
            'state': 'CA',
            'reg_num': "899",
            'foreign_principal': 'The secrets',
            'registrant': "test",
            'url': 'https://example.com',
            'date': '10/15/2018',
            'exhibit_url': 'https://example.com/exhibit_url',
            'address': ''
        }

        mock_tem_loader = ActiveForeignPrincipalLoader(
            ActiveForeignPrincipalItem())

        mock_tem_loader.add_value(None, mock_test)
        actual = mock_tem_loader.load_item()

        expected = {
            'country': "Indonesia",
            'state': 'CA',
            'reg_num': "899",
            'foreign_principal': 'The secrets',
            'registrant': "test",
            'url': 'https://example.com',
            'date': '2018-10-15T00:00:00-04:00',
            'exhibit_url': 'https://example.com/exhibit_url',
            'address': None
        }

        assert actual == expected

    def test_address_parser(self):
        """Address should pasrse correctly"""
        mock_test = {
            'country': "Indonesia",
            'state': 'CA',
            'reg_num': "899",
            'foreign_principal': 'The secrets',
            'registrant': "test",
            'url': 'https://example.com',
            'date': '10/15/2018',
            'exhibit_url': 'https://example.com/exhibit_url',
            'address': 'Breeze moon       900 <b> Seven Street'
        }

        mock_tem_loader = ActiveForeignPrincipalLoader(
            ActiveForeignPrincipalItem())
        mock_tem_loader.add_value(None, mock_test)

        actual = mock_tem_loader.load_item()

        assert actual['address'] == 'Breeze moon 900 Seven Street'
