from mrjob.job import MRJob 

class AnnualSales(MRJob): 

    def mapper(self, _, line):
        data = eval(line)
        artist = data[0]
        year = data[1]
        sales = data[2]
        yield (artist, str(year)), sales

    def reducer(self, key, values):
        total_sales = sum(values)
        total_sales = f"{total_sales:.3f}" 
        yield key, str(total_sales)
        
if __name__ == '__main__': 
    AnnualSales.run()