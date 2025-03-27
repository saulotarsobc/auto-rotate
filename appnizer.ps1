pyinstaller `
    --onefile `
    --add-data "templates:templates" `
    --hidden-import "screeninfo" `
    --hidden-import "rotatescreen" `
    -i "icon.ico" `
    main.py;