#include <SoftwareSerial.h>
#include <ArduinoJson.h>
#define WeatherRxD 6
#define WeatherTxD 7

SoftwareSerial WeatherSerial(WeatherRxD,WeatherTxD);
char                 Weatherbuffer[35];
double               temp;

void getWeatherBuffer()                                                                    //Get weather status data
{
  int index;
  for (index = 0;index < 35;index ++)
  {
    if(WeatherSerial.available())
    {
      Weatherbuffer[index] = WeatherSerial.read();
      if (Weatherbuffer[0] != 'c')
      {
        index = -1;
      }
    }
    else
    {
      index --;
    }
  }
}

int transCharToInt(char *_buffer,int _start,int _stop)                               //char to int
{
  int _index;
  int result = 0;
  int num = _stop - _start + 1;
  int _temp[num];
  for (_index = _start;_index <= _stop;_index ++)
  {
    _temp[_index - _start] = _buffer[_index] - '0';
    result = 10*result + _temp[_index - _start];
  }
  return result;
}

int WindDirection()                                                                  //Wind Direction
{
  return transCharToInt(Weatherbuffer,1,3);
}

float WindSpeedAverage()                                                             //air Speed (1 minute)
{
  temp = 0.44704 * transCharToInt(Weatherbuffer,5,7);
  return temp;
}

float WindSpeedMax()                                                                 //Max air speed (5 minutes)
{
  temp = 0.44704 * transCharToInt(Weatherbuffer,9,11);
  return temp;
}

float Temperature()                                                                  //Temperature ("C")
{
  temp = (transCharToInt(Weatherbuffer,13,15) - 32.00) * 5.00 / 9.00;
  return temp;
}

float RainfallOneHour()                                                              //Rainfall (1 hour)
{
  temp = transCharToInt(Weatherbuffer,17,19) * 25.40 * 0.01;
  return temp;
}

float RainfallOneDay()                                                               //Rainfall (24 hours)
{
  temp = transCharToInt(Weatherbuffer,21,23) * 25.40 * 0.01;
  return temp;
}

int Humidity()                                                                       //Humidity
{
  return transCharToInt(Weatherbuffer,25,26);
}

float BarPressure()                                                                  //Barometric Pressure
{
  temp = transCharToInt(Weatherbuffer,28,32);
  return temp / 10.00;
}

uint8_t checkValue(uint8_t *thebuf, uint8_t leng)
{  
  uint8_t receiveflag=1;
  uint16_t receiveSum=0;
  uint8_t i=0;

  for(i=0;i<leng;i++)
  {
  receiveSum=receiveSum+thebuf[i];
  }
  
  if(receiveSum==((thebuf[leng-2]<<8)+thebuf[leng-1]+thebuf[leng-2]+thebuf[leng-1]))  //check the serial data 
  {
    receiveSum=0;
  receiveflag=1;
//  Serial.print(receiveflag);
  return receiveflag;
  }
}
//transmit PM Value to PC
uint16_t transmitPM01(uint8_t *thebuf)
{

  uint16_t PM01Val;

  PM01Val=((thebuf[4]<<8) + thebuf[5]); //count PM1.0 value of the air detector module
  return PM01Val;
}

void setup()
{
  Serial.begin(9600);
  WeatherSerial.begin(9600);
}

void loop()
{
  float sensorVoltage; 
  float sensorValue;
 
  sensorValue = analogRead(A0);
  sensorVoltage = sensorValue/1024*5;
  /*
  Serial.print("sensor reading = ");
  Serial.print(sensorValue);
  Serial.println("");
  Serial.print("sensor voltage = ");
  Serial.print(sensorVoltage);
  Serial.println(" V");
  */
  //WeatherSerial.listen();
  getWeatherBuffer();
  /*
  Serial.print("Wind Direction: ");
  Serial.print(WindDirection());
  Serial.println("  ");
  Serial.print("Average Wind Speed (One Minute): ");
  Serial.print(WindSpeedAverage());
  Serial.println("m/s");
  Serial.print("Max Wind Speed (Five Minutes): ");
  Serial.print(WindSpeedMax());
  Serial.println("m/s");
  Serial.print("Rain Fall (One Hour): ");
  Serial.print(RainfallOneHour());
  Serial.println("mm  ");
  Serial.print("Rain Fall (24 Hour): ");
  Serial.print(RainfallOneDay());
  Serial.println("mm");
  Serial.print("Temperature: ");
  Serial.print(Temperature());
  Serial.println("C  ");
  Serial.print("Humidity: ");
  Serial.print(Humidity());
  Serial.println("%  ");
  Serial.print("Barometric Pressure: ");
  Serial.print(BarPressure());
  Serial.println("hPa");
  Serial.println("");
  Serial.println("");
  */

  StaticJsonBuffer<500> jsonBuffer;
  JsonObject& root = jsonBuffer.createObject();
  root["UV"] = sensorValue;
  root["UV_voltage"] = sensorVoltage;
  root["wind_direction"] = WindDirection();
  root["avg_wind_speed"] = WindSpeedAverage();
  root["max_wind_speed"] = WindSpeedMax();
  root["pressure"] = BarPressure();
  root.printTo(Serial);
  Serial.println();
  //delay(1000);
}
