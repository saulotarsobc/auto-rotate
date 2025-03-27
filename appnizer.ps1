pyinstaller `
    --onefile `
    --add-data         "templates:templates" `
    --hidden-import    "screeninfo" `
    --hidden-import    "rotatescreen" `
    --icon             "icon.ico" `
    --name             "Auto Rotate - Oluas" `
    --nowindowed       `
    main.py;