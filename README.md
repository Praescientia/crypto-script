Purpose of this project:

**Gain exposure to crypto market in a "smarter" way than a simple buy and hold**

제대로 된 trading system을 만든다고 하면 there's too many things to take care of infrastructure-wise, for example, 매일 여러 거래소에서 price data를 가져와서 하나의 security master로 consolidate하는 스크립틀도 짜야 하고, 이게 fail 할 경우의 alert system, decision on how to consolidate many prices, etc.  
단순하게 가격 데이터만 본다고 해도 위처럼 해야 할게 너무 많아.

그래서 개인적으로 하나씩 infrastructure을 만들고 있는데, 우선 시간도 너무 많이 걸리고 제대로 협업하기가 어려움 -> 빨리 crypto market에 exposure을 가져가고 싶어도 시간이 부족해

So my thought was that maybe we can work together on a stand alone script-based trading system that works as a light-weight solution that we can trust just enough to put a small amount of money in.

예를 들어, for the price data we just use the price data from one data source (Coinbase, Binance, etc)

데이터베이스도 제대로 된 데이터베이스 연결 X, 대신 sqlite 쓰고 데이터베이스 파일 자체를 github 통해서 연동하거나, 아님 간단하게 업데이트 할 수 있는 방법 찾기 -> 더 간단하게 그냥 text file이나 json 써도 돼.

개발환경 관리도 container 같이 제대로 하는 방법들은 시간 오래 걸리니까 패스하고 poetry로만 관리.

scheduler 같은 경우도 그냥 crontab으로 해버리는 것... 이지만 여기 같은 경우는 약간 더 신경 써서 airflow..를 쓰는 것도 괜찮을 거 같아. 하지만 일단은 간단하게 crontab으로 시작.

내가 여기 개발 용어 많이 써서 생소한 거 있을 수도 있는데, 만약에 개발보단 리서치에 더 치중하고 싶으면 위에 쓴 것 보다 더 간략하게 구현해도 괜찮을 거 같아. 내가 개발 같이 할 친구 한 명 더 구할 수도 있을 거 같고, 아님 내가 개발 쪽을 더 도맡아서 할 수도 있고.

어떻게 방향을 잡던 간에, 젠이 스스로 편한 방식으로 코딩하고 구조 짜나가면 나도 약간씩 거기에 의견 첨가 하는 식으로 할게. 내가 항상 플젝 하던 방식이 굳어져 있어서 예전에 협업 할 때 보면 내 방식에 적응하는 learning curve에서 다들 일단 흥미가 식더라고 ㅋㅋㅋㅋ

이 정도가 내가 생각했던 대략적인 플젝 그림이고, trading system이 어떤 부분들이 있어야 될지, 이런 것들은 나중에 더 적어둘게.

# Cursory Plan

Can make two strategies:

1. Long-only: 코인베이스 같은 곳에서 long only strategy

2. Market-netural: Phemex 같은 곳에서 crypto perpetual futures 통해서 롱숏

데이터 관리는 코인베이스나 Phemex에서 가격 다운 받아서 관리.

Base signal들은 https://github.com/twopirllc/pandas-ta 이런 곳에서 technical indicator들 만들고, 리서치는 대부분 이런 base signal들을 묶을 수 있는 ensemble method랑 백테스팅 코드 만드는 거에 포커스 두면 좋을거 같아. 

Universe selection은 백테스팅 가능한 히스토리가 있고, 웬만하면 de-list 안 될거 같은 코인 몇개 골라서 20~30개 정도로 일단 form 하는게 쉬울거야.

Execution engine은 최대한 간단하게, market order 위주로 그냥 원하는 quantity만큼 바로바로 사고 파는 알고리즘 만들어도 괜찮을 거 같아. 약간 더 복잡하게 하면 순식간에 많이 복잡해지는데, 그만큼 money save가 될 수도 있어서 나중에 더 복잡화 할까 고민하면 될듯.