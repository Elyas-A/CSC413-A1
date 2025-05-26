int X_PIN = A0;
int Y_PIN = A1;
int Z_PIN = A2;
int X_COOR;
int Y_COOR;
int Z_BUTTON;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(X_PIN, INPUT);
  pinMode(Y_PIN, INPUT);
  pinMode(Z_PIN, INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  X_COOR = analogRead(X_PIN);
  Y_COOR = analogRead(Y_PIN);
  Z_BUTTON = analogRead(Z_PIN);

  // print output
  Serial.print(X_COOR);
  Serial.print(",");
  Serial.print(Y_COOR);
  Serial.print(",");
  Serial.print(Z_BUTTON)
  Serial.print("\n");

  delay(10);
}
