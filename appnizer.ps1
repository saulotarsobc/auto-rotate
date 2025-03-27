pyinstaller `
    --onefile `
    --add-data         "templates:templates" `
    --hidden-import    "screeninfo" `
    --hidden-import    "rotatescreen" `
    --add-data "icon.ico;." `
    --icon             "icon.ico" `
    --name             "Auto Rotate - Oluas" `
    --nowindowed `
    main.py;