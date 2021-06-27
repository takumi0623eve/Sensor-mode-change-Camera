const int E_1 = 2; //センサ①のエコーが接続されているピン
const int T_1 = 3; //センサ①のトリガーが接続されているピン

const int E_2 = 4; //センサ②のエコーが接続されているピン
const int T_2 = 5; //センサ②のトリガーが接続されているピン

const float UtoD_top_1 = 240.0;    //上下スライド範囲①の最長判定距離[mm]
const float UtoD_bottom_1 = 200.0; //上下スライド範囲①の最短判定距離[mm]
const float UtoD_top_2 = 190.0;    //上下スライド範囲②の最長判定距離[mm]
const float UtoD_bottom_2 = 150.0; //上下スライド範囲②の最短判定距離[mm]
const float LorR_top = 80.0;       //左右スライドの最長判定距離[mm]
const float LorR_bottom = 30.0;    //左右スライドの最長判定距離[mm]

int f = 0; //スライドの種類を判定するフラグ
int f_prev = 0;
int f_cnt =0;
//f: 0=スライド判定なし,1=右スライドの判定開始,2=左スライドの判定開始
int mode = 0; //現在のカメラのモード

int ave_range = UtoD_top_1 + 1.0; //2つのセンサの平均距離(UtoD_bottom_2)
int down_f = 0;                   //上下スライド判定のフラグ

void Shutter_start_check(float dis_1,float dis_2);
void Shutter_end_check(float dis_1,float dis_2);

void setup(){
  Serial.begin(9600);
  pinMode(E_1,INPUT);
  pinMode(T_1,OUTPUT);
  pinMode(E_2,INPUT);
  pinMode(T_2,OUTPUT);
}

void loop(){
  float dur_1=0;
  float dis_1=0; //センサ①の検出距離
  float dur_2=0; 
  float dis_2=0; //センサ②の検出距離

  digitalWrite(T_1,LOW);
  delayMicroseconds(2);
  digitalWrite(T_1,HIGH);
  delayMicroseconds(20);
  digitalWrite(T_1,LOW);
  dur_1 = pulseIn(E_1,HIGH);

  digitalWrite(T_2,LOW);
  delayMicroseconds(2);
  digitalWrite(T_2,HIGH);
  delayMicroseconds(20);
  digitalWrite(T_2,LOW);
  
  dur_2 = pulseIn(E_2,HIGH);
  dis_1 = dur_1/2*340.0/1000;
  dis_2 = dur_2/2*340.0/1000;

  Serial.println(mode);
  delay(60);

  if(dis_1 >= LorR_bottom && dis_1 <= LorR_top && f == 0 && dis_2 > LorR_top){ //10mm以下でスライド判定がなければ
    f = 1; //右スライドの判定開始
  }else if(dis_2 >= LorR_bottom && dis_2 <= LorR_top && f == 0 && dis_1 > LorR_top){ //10mm以下でスライド判定がなければ
    f = 2; //左スライドの判定開始
  }

  if(f != f_prev){
    if (f == 0){
      Serial.println(5);
    }else if(f == 1){
      Serial.println(6);
    }else if(f == 2){
      Serial.println(7);
    }
    delay(20);
    f_prev = f;
  }else if(f != 0){
    f_cnt++;
    if(f_cnt == 5){
      f = 0;
      f_cnt = 0;
    }
  }
  
  mode_change(dis_1,dis_2);    //モード判定

  if(down_f == 0) {                   //上下スライド判定がないなら
    Shutter_start_check(dis_1,dis_2); //上下スライドの開始判定
  }else{                              //あるなら
    Shutter_end_check(dis_1,dis_2);   //上下スライドの終了判定
  }
}

void mode_change(float dis_1,float dis_2){
  if(f == 1){                     //右スライド中で
    if(dis_1 > LorR_top && dis_2 >= LorR_bottom && dis_2 <= LorR_top) {          //②が10mm以下なら
      mode--;                    //モードを１減少
      if(mode < 0) mode = 4;     //モード1より小さいならモード5に 
      f = 0;                     //スライド判定をなくす
    }
  }else if(f == 2){               //左スライド中で
    if(dis_1 >= LorR_bottom && dis_1 <= LorR_top && dis_2 > LorR_top){           //①が10mm以下なら
      mode++;                     //モードを1増加
      if(mode > 4) mode = 0;      //モード5より大きいならモード1
      f = 0;                      //スライド判定のリセット
    }
  } 
}


void Shutter_start_check(float dis_1,float dis_2){
  if(dis_1 >= UtoD_bottom_1 && dis_1 <= UtoD_top_1 && dis_2 >= UtoD_bottom_1 && dis_2 <= UtoD_top_1){ //両方のセンサが反応したら
    f = 0;
    if(ave_range > (int)(dis_1 + dis_2)/2){
      ave_range = (int)(dis_1 + dis_2)/2 * 100;
      Serial.println(ave_range);
      down_f = 1;
      delay(30);
    }else{
      down_f = 0;
      ave_range = UtoD_top_1 + 1.0;
    }
  }
}

void Shutter_end_check(float dis_1,float dis_2){
  if(dis_1 >= UtoD_bottom_2 && dis_1 <= UtoD_top_2 && dis_2 >= UtoD_bottom_2 && dis_2 <= UtoD_top_2){ //両方のセンサが反応したら
    ave_range = (int)(dis_1 + dis_2)/2 * 100;
    Serial.println(ave_range);
    down_f = 0;
    delay(30);
    ave_range = UtoD_top_1 + 1.0;
  }
}
