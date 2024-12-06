# pip install SimboloSiamese
# pip install myanmartools

from Siamese import BurmeseConverter
from myanmartools import ZawgyiDetector

def romanization_to_burmese(text):
  try:
      converter = BurmeseConverter()
      burmese_output = converter.romanization_to_burmese(text)
      return ("Burmese Output:", burmese_output)
  except Exception as e:
      return(f"Error in Romanization to Burmese: {e}")
text = "mc:,k lL kWA"
print(romanization_to_burmese(text))