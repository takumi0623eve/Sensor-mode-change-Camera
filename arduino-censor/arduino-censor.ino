const int E_1 = 2; //①のエコーが接続されているピン
const int T_1 = 3; //①のトリガーが接続されているピン

const int E_2 = 4; //②のエコーが接続されているピン
const int T_2 = 5; //②のトリガーが接続されているピン

int f = 0; //スライドの種類を判定するフラグ
//f: 0=スライド判定なし,1=右スライドの判定開始,2=左スライドの判定開始
int mode = 0; //現在のカメラのモード

int cnt = 0;
int sum = 0;

void setup(){
  Serial.begin(9600);
  pinMode(E_1,INPUT);
  pinMode(T_1,OUTPUT);
  pinMode(E_2,INPUT);
  pinMode(T_2,OUTPUT);
}

void loop(){
  float dur_1=0;
  float dis_1=0; //①の距離
  float dur_2=0; 
  float dis_2=0; //②の距離

  digitalWrite(T_1,LOW);
  delayMicroseconds(2);
  digitalWrite(T_1,HIGH);
  delayMicroseconds(20);
  digitalWrite(T_1,LOW);
  dur_1=pulseIn(E_1,HIGH);

  digitalWrite(T_2,LOW);
  delayMicroseconds(2);
  digitalWrite(T_2,HIGH);
  delayMicroseconds(20);
  digitalWrite(T_2,LOW);
  
  dur_2=pulseIn(E_2,HIGH);
  dis_1=dur_1/2*340.0/1000;
  dis_2=dur_2/2*340.0/1000;

  //Serial.print("dis1:");
  //Serial.print(dis_1);
  //Serial.print(" dis2:");
  //Serial.print(dis_2);
  //Serial.print(" f:");
  //Serial.print(f);
  //Serial.print(" mode:");
  Serial.println(mode);
  //Serial.println("");
  delay(60);

  if(dis_1 > 0.0 && dis_1 <= 100.0 && f == 0 && dis_2 > 100.0){ //10mm以下でスライド判定がなければ
    f = 1; //右スライドの判定開始
  }else if(dis_2 > 0.0 && dis_2 <= 100.0 && f == 0 && dis_1 > 100.0){ //10mm以下でスライド判定がなければ
    f = 2; //左スライドの判定開始
  }
  
  if(f == 1){                     //右スライド中で
    if(dis_2 <= 100.0) {          //②が10mm以下なら
      //Serial.println("L → R!");  //右スライドの判定完了
      mode++; //モードを１増加
      if(mode > 4) mode = 0;     //モード5より大きいならモード1に
      f = 0;                     //スライド判定をなくす
      //Serial.println(mode);
      delay(20);
    }
  }else if(f == 2){               //左スライド中で
    if(dis_1 <= 100.0){           //①が10mm以下なら
      Serial.println(mode);
      //Serial.println("R → L!");   //左スライドの判定完了
      mode--;                     //モードを1減少
      if(mode < 0) mode = 4;      //モード1より小さいならモード5に
      f = 0;                      //スライド判定をなくす
      //Serial.println(mode);
      delay(20);
    }
  }

  if ( f == 0){
    Serial.println(70);
  }else if(f == 1){
    Serial.println(71);
  }else if(f == 2){
    Serial.println(72);
  }
  delay(20);
  
  if(dis_1 > 150.0 && dis_1 <= 250.0 && dis_2 > 150.0 && dis_2 <= 250.0){ //両方のセンサが反応したら
    cnt ++;                             //回数カウント
    if(cnt > 2){                        //２回以上だったら
      sum = 10 + cnt;
      Serial.println(sum);
      delay(200);
      f = 0;
    }
    if(cnt > 12){
      Serial.println(50);
      cnt = 0;
      delay(600);
    }
  }else if(cnt > 0){
    cnt = 0;
    Serial.print(10);
  }
}
