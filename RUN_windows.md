# Instrukcja uruchomienia robota Waveshare Pircaer z poziomu komputera z systemem Windows
Do zdalnego sterowania robotem wymagany jest komputer podłączony do tej samej sieci WIFI co płytka Raspberry Pi obsługująca robota

## Uzyskanie adresu IP płytki
Celem uzyskania adresu płytki należy uruchomić pojazd, podłączyć płytkę do monitora i w terminalu uzyskać adres za pomocą komendy: 
```bash
ifconfig wlan0
```
lub 
```bash
ip -br a
```
 

## Połaczenie z pojazdem 

Mając adres płytki można połączyć się z nią korzystając z protokołu SSH z poziomu wiersza poleceń  za pomocą komendy: 
```bash
ssh piracer@<adres IP RaspberryPi>
```
Hasło umożliwiające zalogowanie się do RaspberryPi to:

```bash
raspberry
```
## Uruchomienie pojazdu 

W pierwszym roku należy wejść do folderu pojazdu: 
```bash
cd mycar
```
### Sterowanie za pomocą klawiatury 

Będąc w folderze należy wpisać komendę 

```bash
python manage.py drive 
```
Pojazd powinien się uruchomić i sterowanie nim będzie możliwe z poziomu aplikacji webowej po wpisaniu w przeglądarce 

```bash
<adres IP płytki>:8887
```
Do sterwaonia służą przyciski WASD 

### Sterowanie za pomocą kontrolera 

Do wejścia USB w płytce Raspberry Pi należy podłączyć wtyczkę od kontrolera a następnie włączyć kontroler przełącznikiem znajdującym się od spodu.
Można teraz uruchomić pojazd w trybie sterowania kontrolerem: 
```bash
python manage.py drive --js
```
Funkcje poszczególnych przycisków na kontrolerze opisuje poniższa grafika:
![image](https://github.com/killpopmusic/itwl-donkeycar/assets/132206771/1abf9c00-4fe2-48aa-b7c3-b038340440a6)

