# Coin Trading Bot

[프로젝트 설명 링크](https://www.notion.so/632308649c88426f86483baa76538e3a)
---

## Summary
코인 트레이딩 봇
## Description
<br>
코인에 항상 집중할 수 없는 상황에 있는 사람들을 위한 프로그램입니다. 사용자가 직접 원하는 코인과 코인의 하한가를 지정해 놓음으로써 텔레그램으로 알림이 울리고 텔레그램 팝업이 뜹니다. 팝업창을 누름과 동시에 원하는 코인의 이름과 가격을 누름으로써 손 쉽게 코인을 매수 및 매도를 할 수 있도록 도와주는 프로그램입니다. 

(주의 : 투자에 대한 책임은 프로그램 개발자가 아닌 투자자 본인에게 있습니다.)

## Setting
- 텔레그램 봇을 만들어야 합니다. 만드는 법은 [여기](https://www.notion.so/telegram-bot-setting-b1733a3ee8a645338803727436b4faa4)를 참고해 주세요.


- 파이썬 프로그램이 실행되고 있어야 합니다.

1. terminal 또는 cmd를 실행합니다.

2. "git clone" 으로 본 프로젝트를 클론합니다.
![ex_screenshot](./images/clone.jpg)

3. 현재 디렉토리에 "coin-trading-bot"이라는 이름의 폴더가 생성되었을 것입니다. 해당 폴더로 이동해 줍니다. (cd coin-trading-bot)

4. "python3 -m pip install -r requirements.txt" 으로 필요한 라이브러리를 설치한다. 파이썬3이 설치되어 있지 않다면 [여기](https://wikidocs.net/8)를 눌러주세요.

5. [telegram_token.txt](https://www.notion.so/telegram-bot-setting-b1733a3ee8a645338803727436b4faa4), [access_key.txt, secret_key.txt](https://www.notion.so/access-key-secret-key-e62a10d1ba05490b90b3a2f2eb7a4973)가 필요합니다. 링크를 통해 토큰 및 키를 발급 받은 후 프로젝트 폴더(coin-trading-bot 폴더 안)에서 각각의 txt파일에 각각 키 정보를 넣어 생성해 줍니다.

6. "python3 telegram_bot.py"를 통해 파일을 실행시킨다.


## How To Use
<br>

* telegram bot token이 필요하므로, /start 명령어를 필수적으로 입력해 줍니다. 해당 명령어를 입력하면, bot_id.txt가 프로젝트 폴더에 자동적으로 생성이 됩니다.




### 사용 가능한 명령어 화면에 출력

- 사용 예시

### 프로세스가 잘 작동중인지 확인

- 사용 예시


###  하한가 지정 및 코인 알림

- 사용 예시

![ex_screenshot](./images/limitsetup.jpg)

명령어 : /limitsetup [코인 심볼] [하한가(%)]

`원하는 코인이 지정한 하한가에 도달했을 경우 위 사진 처럼 알람이 울립니다.`

<br><br>

### 원하는 코인을 원하는 가격 만큼 시장 가격으로 매수

- 사용 예시

![ex_screenshot](./images/buy.jpg)

명령어 : /buy [코인 심볼] [원하는 총 가격]

`원하는 코인을 원하는 총 가격 만큼 시장 가격으로 매수합니다.`
  
<br><br>


### 원하는 코인을 원하는 수량 만큼 시장 가격으로 매도

- 사용 예시

![ex_screenshot](./images/sell.jpg)

명령어 : /sell [코인 심볼] [원하는 코인의 총 수량]

`원하는 코인을 원하는 총 수량만큼 시장 가격으로 매도합니다.`


### 현재 코인 가격 체크

- 사용 예시

![ex_screenshot](./images/price.jpg)

`원하는 코인의 현재 시장가를 보여줍니다.`

### 작동중인 프로그램 stop

- 사용 예시

![ex_screenshot](./images/stop.jpg)

`현재 작동중인 프로그램을 멈춤`
