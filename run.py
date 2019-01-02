from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from simulation.simulation.spiders import fara


process = CrawlerProcess(get_project_settings())
process.crawl(fara.FaraSpider)
process.start()
