W repozytorium znajduje się projekt zaliczeniowy, pozwalający wyświetlić dane pomiarowe z wybranej stacji

## wymagania

- zainstalowany python3
- zainstalowany manager paczek pip
- zainstalowane paczki wypisane w pliku requirements.txt 

```
pip install -r requirements.txt
```

## uruchomienie programu

Program uruchamiamy, uruchamiając skrypt main.py z poziomu folderu glównego projektu:
```
python src/main.py 
```
Pomiary będa wyświetlone po dwukrotnym kliknięciu w wybraną stacje pomiarową (lista z lewej strony) i następnie dwukrotnym kliknięciu w interesujący nas pomiar (lista z prawej strony). Dodatkowo, można ustawić zakres czasowy od 0 do 48 godzin poprzedzających zapytanie.

W przypadku braku polączenia z internetem używane sa dane historyczne zapisane w bazie danych

## uruchomienie testów

Testy jednostkowe można uruchomić poleceniem (z poziomu folderu glównego):
```
python src/test.py 
```
Testy wykorzystują bazę danych test.db w celu przetestowania procedury zapisywania danych i pobierania ich