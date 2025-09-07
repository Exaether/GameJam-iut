pyinstaller --onefile \
  --add-data "assets:assets" \
  --add-data "data:data" \
  --windowed main.py

# Pour executer le file merci de faire ./dist/main