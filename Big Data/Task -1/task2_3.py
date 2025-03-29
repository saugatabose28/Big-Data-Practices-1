from mrjob.job import MRJob
from mrjob.step import MRStep

class TopSellingArtistsByDecade(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   reducer=self.reducer),
            MRStep(reducer=self.sort_by_sales),
              MRStep(reducer=self.sort_by_decade)
        ]

    def mapper(self, _, line):
        data = line.strip().split('\t')
        artist_year = eval(data[0])
        sales = float(data[1].strip('"'))
        artist = artist_year[0]
        year = int(artist_year[1].strip('"'))
        decade = (year // 10) * 10  
        # 2019//10 =201*10 = 2010
        yield (decade, artist), sales

    def reducer(self, decade_artist, sales):
        decade, artist = decade_artist
        total_sales = sum(sales)
        yield decade, (total_sales, artist)

    def sort_by_sales(self, decade, sales_artists):
        top_artists = sorted(sales_artists, key=lambda x: x[0], reverse=True)[:3]
        for total_sales, artist in top_artists:
            yield None, (decade, artist, total_sales)
    
    def sort_by_decade(self, _, info):
        sorted_info = sorted(info, key=lambda x: (x[0], x[2]), reverse=True)
        for decade, artist, total_sales in sorted_info:
            formatted_total_sales = "{:.3f}".format(total_sales)
            yield str(decade) + "-" + str(decade + 9), [artist, formatted_total_sales]

    
if __name__ == '__main__':
    TopSellingArtistsByDecade().run()

