#include <Servo.h>
Servo servo;

String comando = "";
char leitura;
bool recebe = true;

void setup(){
  Serial.begin(9600);
  servo.attach(9);
  for(int i = 13; i>2; i--)
    pinMode(i, OUTPUT);
}

int concatenar(){
  char cmd[3] = {};
  for(int i = 0; i<=3; i++)
    cmd[i] = comando[i+1];
  Serial.println(comando);
  Serial.println(atoi(cmd));
  comando = "";
  return atoi(cmd);
}

void loop(){
  if(Serial.available()){
    while(Serial.available()){
      leitura = Serial.read();
      comando += leitura;
      delay(10);
    }
    if(comando[0] == 's'){
      servo.write(concatenar());
    }
    if(comando[0] == 'p'){
      short int porta = concatenar();
      digitalWrite(porta, !digitalRead(porta));
    }

  }
}
