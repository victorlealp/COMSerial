#include "COMSerial.h"

COMSerial comserial(true);

String comando = "";
char leitura;

void setup(){
  comserial.begin(9600);
  comserial.servos();
}
void loop(){
  if(Serial.available()){
    while(Serial.available()){
      leitura = Serial.read();
      if(leitura != '\n')
        comando += leitura;
      else{
        comserial.concatenar(comando);
        comando = "";
      }
      delay(10);
    }
  }
}
