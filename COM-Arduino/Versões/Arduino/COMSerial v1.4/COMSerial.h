#ifndef tl
#define tl

#if (ARDUINO >= 100)
  #include "Arduino.h"
#else
  #include "WProgram.h"
#endif

class COMSerial{
  public:
    //Construtor
    COMSerial(bool displayMsg=false);

    //Métodos
    void begin(int baudRate=9600);
    void digital_Write(int porta, bool level);
    void servos(short int A=0, short int B=0, short int C=0, short int D=0, short int E=0);
    void porta_O(int porta);
    void porta_I(int porta);
    void concatenar(String comando);
    void executar(char prefixo, short int cmd);

    private:
    bool _msg;
    int _portasO[11], _portasI[11];
      
};
#endif
