import matplotlib.pyplot as plt

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from bot.log.logging_ import logging_



class Chart:
     
     
     async def chart_generate(
          self,
          prices: list[int],
          filename: str,
          name: str
     ) -> str:
          path = f"/data/charts/{filename}"
          
          logging_.chart.info(f"GENERATE CHART {filename} FOR ITEM {name}")
          
          if len(prices) == 1:
               prices.append(prices[0])
          
          with plt.style.context("https://github.com/dhaitz/matplotlib-stylesheets/raw/master/pitayasmoothie-dark.mplstyle"):
               plt.plot(prices)
               plt.ylabel("Цена")
               plt.title(name)
               plt.savefig(path)
               plt.close()
          return await self._chart_watermark(input_image=path)

     
     async def _chart_watermark(
          self,
          input_image: str
     ) -> str:
          photo = Image.open(input_image)
          drawing = ImageDraw.Draw(photo)
          
          pos = (0, 0)
          text = "@fastfy_bot"
          
          font = ImageFont.truetype("bot/utils/fonts/SFProText-Regular.ttf", 20)
          drawing.text(pos, text, font=font)
          photo.save(input_image)
          
          logging_.chart.info(f"WATERMARK FOR {input_image}")
          
          return input_image