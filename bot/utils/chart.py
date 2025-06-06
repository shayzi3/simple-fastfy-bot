import matplotlib.pyplot as plt



class Chart:
     
     
     async def chart_generate(
          self,
          prices: list[int],
          filename: str,
          name: str
     ) -> str:
          path = f"data/charts/{filename}"
          # x = [i for i in range(1, len(prices) + 1)]
          
          if len(prices) == 1:
               prices.append(prices[0])
          
          with plt.style.context("https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle"):
               plt.plot(prices)
               plt.ylabel("Цена")
               plt.title(name)
               plt.savefig(path)
          return path