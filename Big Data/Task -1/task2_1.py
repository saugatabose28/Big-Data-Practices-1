from mrjob.job import MRJob
from mrjob.step import MRStep

class HighestSalesByYear(MRJob):

    def steps(self):
          return [MRStep(mapper=self.mapper,reducer = self.reducer),
                MRStep(reducer=self.sort_by_year)] 

    def mapper(self, _, line):
        data = line.strip().split('\t')
        artist_year = eval(data[0])  
        sales = float(data[1].strip('"'))
        artist = artist_year[0]
        year = artist_year[1]
        yield year, (artist,sales)

    def reducer(self, year, sales_artists):
        max_sales_artist = max(sales_artists, key=lambda x: x[1])  
        yield None, (year, max_sales_artist)
        # (year,(artist,sales))

    def sort_by_year(self, _, data):
        for year, data in sorted(data, key=lambda x: x[0], reverse=True):
            yield  str(year), data

if __name__ == '__main__':
    HighestSalesByYear().run()
