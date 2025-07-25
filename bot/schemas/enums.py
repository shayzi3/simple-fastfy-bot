from enum import Enum, auto


class SkinUpdateMode(Enum):
     HIGH = auto()
     MEDIUM_WELL = auto()
     MEDIUM = auto()
     LOW = auto()
     
     
     
     @classmethod
     def new_update_mode(
          cls, 
          volume: int, 
          last_price: float | None, 
          new_price: float
     ) -> "SkinUpdateMode":
          mode = SkinUpdateMode.LOW
          if volume >= 10000:
               mode = SkinUpdateMode.HIGH
          
          elif volume >= 3000:
               mode = SkinUpdateMode.MEDIUM_WELL
          
          elif volume >= 500:
               mode = SkinUpdateMode.MEDIUM
               
          elif last_price is not None:
               if ((new_price - last_price) / last_price)*100 >= 20:
                    mode = SkinUpdateMode.HIGH
          return mode