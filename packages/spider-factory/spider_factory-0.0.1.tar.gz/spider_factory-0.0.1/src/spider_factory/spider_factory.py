from abc import ABC, abstractmethod
import os
import sys

from rusta_crawler.spiders import rusta_spider as rusta_spider


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from scrapy.crawler import CrawlerProcess
from scrapy.spiders import Spider
import argparse
import logging

# Step 1: Define the Spider interface
class Spider(ABC):
    @abstractmethod
    def create(self):
        pass

# Step 2: Create concrete classes
class NewSiteSpider(Spider):
    def create(self, *args, **kwargs) -> rusta_spider.NewEcomSpider:
        return rusta_spider.NewEcomSpider
    
# Step 3: Define the SpiderFactory class
class SpiderFactory(ABC):
    @abstractmethod
    def create_spider(self,  *args, **kwargs) -> Spider:
        pass

# Step 4: Implement concrete factories
class NewEcomSpiderFactory(SpiderFactory):

    def create_spider(self, *args, **kwargs) -> Spider:
        return NewSiteSpider()


# Client code
def create_spider(factory: SpiderFactory, *args, **kwargs) -> None:
    spider_factory = factory.create_spider(*args, **kwargs)
    if kwargs.get('ctr'):
        ctr = kwargs.get('ctr')
        for c in ctr:
            sp = spider_factory.create()
            process = CrawlerProcess()
            kwargs['ctr'] = c
            process.crawl(sp, **kwargs)
    else:
        sp = spider_factory.create()
        process = CrawlerProcess()
        process.crawl(sp, **kwargs)
    process.start()

def run_new_ecom_site_spider(scrape_type, ctr=None, load_epi=False, debug=None):
    
    if ctr:
        ctr = [c.upper() for c in ctr]
    kwargs = { "ctr": ctr, "scrape": scrape_type, "load_epi": load_epi, "debug": debug}
    new_site_factory = NewEcomSpiderFactory()  
    create_spider(new_site_factory, **kwargs)

def list_of_strings(arg):
    return arg.split(',')
 
def main():
    logger = logging.getLogger(__name__)
    parser = argparse.ArgumentParser(description='Run Scrapy spiders with common input.')
    parser.add_argument('--spider', type=str, help='Spider to run. new-site', required=True)
    parser.add_argument('--scrape', type=str, help='week rolling active', required=True)
    parser.add_argument('--ctr', type=list_of_strings, help='Countries. SE NO DE FI. For multiple countries seperate with "," ', required=False)
    parser.add_argument('--debug', type=str, required=False)


    
    args = parser.parse_args()
    if args.spider == 'new_site':
        if args.scrape in ['week', 'rolling']:
            logger.info(f"SPIDER FACTORY - Running spider for {args.scrape}")
            run_new_ecom_site_spider(scrape_type=args.scrape)
        elif args.scrape == 'active' and args.ctr:
            for ctr in args.ctr:
                if ctr.upper() not in ['SE', 'NO', 'FI', 'DE']:
                    parser.error(f"Invalid country code: {ctr}")
            logger.info(f"SPIDER FACTORY - Running spider for {ctr}")
            run_new_ecom_site_spider(ctr=args.ctr, scrape_type=args.scrape, load_epi=args.load_epi, debug=args.debug)
        else:
            parser.error("Please provide required arguments")

if __name__ == "__main__":
    main()
    