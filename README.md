# Recruitment task / Zadanie rekrutacyjne 

Wymagania:
- python 3.7 (lub wyżej, nie testowano)
- pip

Instalacja

Aby zainstalować należy sklonować [repozytorium](https://github.com/FilipFl/profil_software_recruitment) w wybranej lokalizacji. Następnie z wiersza poleceń w lokalizacji instalacji Pythona należy wpisać "python -m venv path/to/venv" gdzie 'path/to/venv' to lokalizacja gdzie chcemy umieścić wirtualne środowisko. Następnie wpisujemy "path/to/venv/Scripts/avtivate", w konsoli powinna przed znakiem zachęty pojawić się nazwa środowiska. Następnie należy wpisać "pip install requests" i "pip install peewee". Po zakończonej instalacji w wierszu poleceń idziemy do lokalizacji z repozytorium i można korzystać ze skryptu wpisując "python main.py --komenda". Lista komend znajduje się poniżej. W repozytorium znajduje się gotowa baza ponieważ wypełnianie całej na podstawie pliku jest całkiem czasochłonne. Aby przetestować uzupełnianie danych z pliku wystarczy skasować plik "recruitment_db.db" i zastosować odpowiednią komendę ze skryptu.

Installation

To install clone the git [repository](https://github.com/FilipFl/profil_software_recruitment) in the destination of Your choice. Next go to Your Python installation destination and in the command line type "python -m venv path/to/venv" then got to path/to/venv location and in command line type "Scripts/activate" if succesfull type "pip install requests" and "pip install peewee". Go to the cloned repository location and You can use the script typing in command line "python main.py --command" List of commands is below. Repository contains prepared database because of long dumping from file time.

# List of commands:
- "-\-percentage" - shows the percentage of male/female amount of records in database
- "-\-average_age" - shows average age of people, use it with "female" "male"  or "general" flag
- "-\-most_common_cities" - shows most common cities, use it with "N" integer parameter which determines returned amount
- "-\-most_common_passwords" - same as above 
- "-\-best_password" - returns best password along with the score, if multiple exist retrieve first alphabetically
- "-\-born_between" - get people born between two dates specified as parameter in format "YYYY-MM-DD:YYYY-MM-DD"
- "-\-how_many" - get amount of People in database
- "-\-init" - initialise database with the "persons.json"
- "-\-load_from_api" - insert into database "N" integer amount of records from the API, used with "-\-api_init" will initialise tables (use it as first initialization instead of "-\-init"), otherwise it just appends into the database