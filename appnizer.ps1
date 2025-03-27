pyinstaller `
    --onefile `
    --windowed `
    --add-data      "templates:templates" `
    --hidden-import "screeninfo" `
    --hidden-import "rotatescreen" `
    --add-data      "icon.ico;." `
    --icon          "icon.ico" `
    --name          "Auto Rotate - SC" `
    main.py;