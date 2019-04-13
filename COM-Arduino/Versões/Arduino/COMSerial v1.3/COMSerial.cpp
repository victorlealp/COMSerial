#include "COMSerial.h"
#include <Servo.h>

#define TAM 11

Servo servo[5];

//------------------------Funções de Instância------------------------//
COMSerial::COMSerial(bool displayMsg){
  _msg = displayMsg;
}

void COMSerial::begin(int baudRate){
  Serial.begin(baudRate);
  if(_msg)
    Serial.println("Biblioteca instanciada com sucesso!");
}

void COMSerial::digital_Write(int porta, bool level){
  porta_O(porta);
  digitalWrite(porta, level);
  return 1;
}

void COMSerial::servos(short int A, short int B, short int C, short int D, short int E){
  int aux = 0;

  //Contagem de variáveis válidas
  if(A != 0)
    aux++;
  if(B != 0)
    aux++;
  if(C != 0)
    aux++;
  if(D != 0)
    aux++;
  if(E != 0)
    aux++;

  //Instanciação
  switch(aux){
    case 5: servo[4].attach(E);
    case 4: servo[3].attach(D);
    case 3: servo[2].attach(C);
    case 2: servo[1].attach(B);
    case 1: servo[0].attach(A);
      if(_msg){
        Serial.print(aux);
        Serial.println(" servo(s) acoplados(s)!");
      }
      break;
    default:
    if(_msg)
      Serial.println("Nenhum servo acoplado!");
  }
}

void COMSerial::porta_O(int porta){
  for(int i = 0; i<TAM; i++){
    if(_portasO[i] == porta)
      break;
    else{
      _portasO[i] = porta;
      pinMode(porta, OUTPUT);
      if(_msg){
        Serial.print("Porta ");
        Serial.print(porta);
        Serial.println(" definida como OUTPUT!");
      }
      break;
    }
  }
}

void COMSerial::porta_I(int porta){
    for(int i = 0; i<TAM; i++){
    if(_portasI[i] == porta)
      break;
    else{
      _portasI[i] = porta;
      pinMode(porta, INPUT);
      if(_msg){
        Serial.print("Porta ");
        Serial.print(porta);
        Serial.println(" definida como INPUT!");
      }
      break;
    }
  }
}

//------------------------Funções de Controle-------------------------//

void COMSerial::executar(char prefixo, short int cmd){

  //Print Comando
  Serial.print(prefixo); Serial.print(" "); Serial.println(cmd);

  //Ligar e Desligar Portas
  if(prefixo == 'p')
    digital_Write(cmd, !digitalRead(cmd));

  //Comandar Servo 1
  if(prefixo == 'a')
    servo[0].write(cmd);

  //Comandar Servo 2
  if(prefixo == 'b')
    servo[1].write(cmd);

  //Comandar Servo 3
  if(prefixo == 'c')
    servo[2].write(cmd);

  //Comandar Servo 4
  if(prefixo == 'd')
    servo[3].write(cmd);

  //Comandar Servo 5
  if(prefixo == 'e')
    servo[4].write(cmd);
}

void COMSerial::concatenar(String comando){
  char cmd[3] = {};
  
  for(int i = 0; i<3; i++)
    cmd[i] = comando[i+1];
    
  Serial.println(comando);
  
  executar(comando[0], atoi(cmd));
}
