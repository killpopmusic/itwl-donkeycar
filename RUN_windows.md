# Instrukcja uruchomienia robota Waveshare Pircaer z poziomu komputera z systemem Windows 10/ 11

Do zdalnego sterowania robotem wymagany jest komputer podłączony do tej samej sieci WIFI co płytka Raspberry Pi obsługująca robota. Komputer ze starszą wersją windowsa wymaga instalacji zewnętrznnego oprogramowania do obsługi komunikacji za pomocą protokołu SSH.

## Uzyskanie adresu IP płytki
Adres IP płytki podłaczonej do sieci powinien automatycznie wyśiwtlić się na ekranie OLED z tyłu pojazdu. Jeśli adres nie wyświetla się należy  podłączyć płytkę do monitora i w terminalu uzyskać adres za pomocą komendy: 
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
Aby ruszyć należy kliknąć spację. Do sterwaonia służą przyciski WASD. Za pomocą przycisku POHTO lub "P" n klawiaturze mozliwe jest wykonanie zdjęcie w rozdzielczości 1920x1080. 
Kliknięcie przycisku RECORD lub "R" na klawiaturze uruchamia seknwecję robienia zdjęć w niskiej rozdzielczości co 1 skenudę bez zatrzymywania streama. Zdjęcia są zapisaywane lokalnie na RaspberryPikolejno w folderach mycar/NDT_photos i mycar/data/tub 


### Sterowanie za pomocą kontrolera 

Do wejścia USB w płytce Raspberry Pi należy podłączyć wtyczkę od kontrolera a następnie włączyć kontroler przełącznikiem znajdującym się od spodu.
Można teraz uruchomić pojazd w trybie sterowania kontrolerem: 
```bash
python manage.py drive --js
```
Funkcje poszczególnych przycisków na kontrolerze opisuje poniższa grafika. Zmodyfikowano sterowanie tak, aby naciśnięcie przycisku X wywoływało zrobienie zdjęcia, identycznie jak w przypadku sterowania z klawiatury. 
Należy pamiętać, że aby zrobić zdjęcie należy naciznąć przycisk X i gdy checmy jechać dalej kliknąć go ponownie:
![image](https://github.com/killpopmusic/itwl-donkeycar/assets/132206771/1abf9c00-4fe2-48aa-b7c3-b038340440a6)

