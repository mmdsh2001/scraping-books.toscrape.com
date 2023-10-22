# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        
        adoptor = ItemAdapter(item)


        field_names = adoptor.field_names()

        #availability str to int
        availability_str = adoptor.get('availability')[0]
        availability_spilited_arr = availability_str.split("(")
        if len(availability_spilited_arr) < 2 :
            adoptor['availability'] = 0
        else:
            availability = availability_spilited_arr[1].split(' ')[0]
            adoptor['availability'] = int(availability)

        #category str to lowercase
        category_str = adoptor.get('category')[0]
        adoptor['category'] = category_str.lower()  

        # rating str to int 
        rating_str = adoptor.get("rating")[0]
        if rating_str == "star-rating Five":
            adoptor['rating'] = 5   
        elif rating_str == "star-rating Four":
            adoptor['rating'] = 4
        elif rating_str == "star-rating Three":
            adoptor['rating'] = 3
        elif rating_str == "star-rating Two":
            adoptor['rating'] = 2
        elif rating_str == "star-rating One":
            adoptor['rating'] = 1
                
        #number_of_reviews str to int
        number_of_reviews_str = adoptor.get("number_of_reviews")[0]
        adoptor['number_of_reviews'] = int(number_of_reviews_str)         
        


        
        
        
        
        return item
