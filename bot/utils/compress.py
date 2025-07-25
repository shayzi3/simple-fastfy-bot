


class CompressSkinName:
     phrases_compress = {
          "(Battle-Scarred)": "BS",
          "(Well-Worn)": "WW",
          "(Field-Tested)": "FT",
          "(Minimal Wear)": "MW",
          "(Factory New)": "FN",
          "StatTrak™": "ST"
     }
     phrases_from_compress = {
          "BS": "(Battle-Scarred)",
          "WW": "(Well-Worn)",
          "FT": "(Field-Tested)",
          "MW": "(Minimal Wear)",
          "FN": "(Factory New)",
          "ST": "StatTrak™"
     }
     
     @classmethod
     def compress(cls, name: str, from_compress: bool) -> str:
          phrases = cls.phrases_from_compress if from_compress else cls.phrases_compress
          for key, value in phrases.items():
               name = name.replace(key, value)
          return name