todos hoje

## escolher uma estrategia que funciona pra crip e tem alta frequencia
## backtestes
    - Fazer um backtest com - cross validation nos 5 anos de analise, para escolher alguma estrategia e papel bons

## colocar a estegia em AWS EC2 para rodar live
    - tem que estar em container 
    - tem que mandando email quando faz paper trade
## Fazer uma tela de visualizacao do 
    - live pnl
    - live exposicao
    - live ordens executadas




# resultados ate agora - USANDO TIMEFRAME HORAS, e BTS de 1 ano

## MACrossover
### na tesla
<Strategy MACrossover(short_window=17,long_window=80,buffer_pct=0.002)>
<Strategy MACrossover(short_window=5,long_window=60,buffer_pct=0.01)>

### na apple
 <Strategy MACrossover(short_window=5,long_window=60,buffer_pct=0.01)>

### na nvidia
 <Strategy MACrossover(short_window=5,long_window=60,buffer_pct=0.01)>

### na META
 <Strategy MACrossover(short_window=5,long_window=60,buffer_pct=0.01)>

### no XLF
 <Strategy MACrossover(short_window=5,long_window=60,buffer_pct=0.01)>


### o SPY
 <Strategy MACrossover(short_window=5,long_window=60,buffer_pct=0.01)>

## MACrossoverADX

### na META

MACrossoverADX(short_window=23,long_window=40,adx_threshold=35)
MACrossoverADX(short_window=11,long_window=70,adx_threshold=20)
MACrossoverADX(short_window=7,long_window=85,adx_threshold=30) 4.16


## MACrossoverADXStopLoss
### na tesla
MACrossoverADXStopLoss(short_window=25,long_window=40,adx_threshold=30) 2.61
MACrossoverADXStopLoss(short_window=17,long_window=75,adx_threshold=35,stop_loss_pct=0.05) 3.01

### na microsoft
MACrossoverADXStopLoss(short_window=13,long_window=60,adx_threshold=25,stop_loss_pct=0.01)

### na META
MACrossoverADXStopLoss(short_window=13,long_window=45,adx_threshold=25,stop_loss_pct=0.05)


# usando timeframe de 1 minuto
## MACrossover

### ETHER
MACrossover(short_window=20,long_window=80,buffer_pct=0.001)


