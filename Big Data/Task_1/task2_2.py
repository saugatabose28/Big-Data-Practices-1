from mrjob.job import MRJob
from mrjob.step import MRStep

class HighestSalesByArtist(MRJob):

    def steps(self):
          return [MRStep(mapper=self.mapper,reducer = self.reducer),
                MRStep(reducer=self.sort_by_year)] 

    def mapper(self, _, line):
        data = line.strip().split('\t')
        artist_year = eval(data[0])  
        sales = float(data[1].strip('"'))
        artist = artist_year[0]
        year = artist_year[1]
        yield artist, sales

    def reducer(self, artist, sales):
        total_sales = sum(sales)
        yield None, (artist, total_sales)

    def sort_by_year(self, _, data):
        for artist, total_sales in sorted(data, key=lambda x: x[1], reverse=True)[:5]:
             formatted_total_sales = "{:.3f}".format(total_sales)
             yield  artist, str(formatted_total_sales)
                
if __name__ == '__main__':
    HighestSalesByArtist().run()
