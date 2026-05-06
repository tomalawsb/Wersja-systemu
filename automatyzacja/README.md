# Automatyzacja

Katalog przeznaczony na projekt programu **Automatyzacja / Wersja 8**.

Źródłem importu jest oczyszczona paczka:

`Wersja_8_ETAP_12_TESTY_RELEASE.zip`

Docelowo w tym katalogu mają znajdować się rozpakowane pliki programu, bez archiwum ZIP oraz bez danych prywatnych/runtime.

## Zasady repozytorium

Do repozytorium nie wrzucać:

- `token.json`
- `google_token.json`
- `client_secret*.json`
- `*.sqlite3`
- `*.sqlite3-wal`
- `*.sqlite3-shm`
- `error.log`
- `__pycache__/`
- prywatnych ustawień z realnymi ścieżkami użytkownika
- plików kolejki runtime

## Ostatni przygotowany etap

Etap 12 — testy techniczne i kontrola paczki release.

W paczce były przygotowane między innymi:

- `unified_app.py`
- `gemini_pipeline.py`
- `task_queue.py`
- `gemini_sender_polskie_menu/`
- `synchro_out/`
- `wspolne/`
- `tools/release_check.py`
- `data/settings/`
- `data/logs/`
- `data/queue/`
- `data/runtime/`

## Status importu

Ten plik tworzy katalog roboczy `automatyzacja/` w repozytorium. Pełny import rozpakowanych plików wymaga masowego uploadu plików projektu albo działania z lokalnego Git-a.