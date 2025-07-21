


class CompressSkinName:
     phrases_compress = {
          "(Battle-Scared)": "BS",
          "(Well-Worn)": "WW",
          "(Field-Tested)": "FT",
          "(Minimal Wear)": "MW",
          "(Factory New)": "FN",
          "StatTrak™": "ST"
     }
     phrases_from_compress = {
          "BS": "(Battle-Scared)",
          "WW": "(Well-Worn)",
          "FT": "(Field-Tested)",
          "MW": "(Minimal Wear)",
          "FN": "(Factory New)",
          "ST": "StatTrak™"
     }
     
     @classmethod
     def compress(cls, name: str, from_compress: bool) -> str:
          strings_new_parts = []
          phrases = cls.phrases_compress if from_compress is False else cls.phrases_from_compress
          for part in name.split():
               phrase = phrases.get(part)
               strings_new_parts.append(phrase if phrase else part)
          return " ".join(strings_new_parts)