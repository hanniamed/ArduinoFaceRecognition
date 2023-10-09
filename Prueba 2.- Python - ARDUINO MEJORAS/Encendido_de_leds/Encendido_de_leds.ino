int ledv=2, ledr=3;

void setup() {
  pinMode(ledv, OUTPUT);
  pinMode(ledr, OUTPUT);
  Serial.begin(9600);
}

void loop() {
    if (Serial.available()) { 
        char c = Serial.read();
        if (c == '1') {
            digitalWrite(ledv, HIGH);  // Enciende el LED en el pin 2
            digitalWrite(ledr, LOW);  
            Serial.println("BIENVENIDO");
        }
        if (c == '0') {
            digitalWrite(ledr, HIGH);  // Enciende el LED en el pin 3
            digitalWrite(ledv, LOW);
            Serial.println("ALTO");
        }
        if (c == '2') {
            digitalWrite(ledv, LOW);
            digitalWrite(ledr, LOW);
            Serial.println("APAGADO");
        }
    }
}
