#include <Adafruit_NeoPixel.h>
Adafruit_NeoPixel strip(288, 5, NEO_GRB + NEO_KHZ800);
#include "data.h"

void setup() {
  strip.begin();
  strip.show();

}
uint8_t frame=0;
void loop() {

  frame=(frame+1)%image_number_frames;
  for(int i=0;i<16*18;i++)
  {
    strip.setPixelColor(i, strip.Color(pgm_read_byte(&image_data[frame][i*3]), pgm_read_byte(&image_data[frame][i*3+1]), pgm_read_byte(&image_data[frame][i*3+2])));
  }
  strip.show();
  delay(1000/image_fps);

}