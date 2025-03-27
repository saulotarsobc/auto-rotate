# Auto Rotate - SC

## Sobre o Projeto

**Auto Rotate - SC** é uma aplicação desenvolvida em Python para controlar a orientação dos monitores de um sistema Windows. Ele fornece uma interface web e um ícone na bandeja do sistema para facilitar o acesso e controle da rotação das telas.

## Recursos

- Exibe informações detalhadas dos monitores conectados.
- Permite alterar a orientação dos monitores para **paisagem**, **retrato**, **paisagem invertida** e **retrato invertido**.
- Disponibiliza uma API para controle remoto da orientação.
- Interface na bandeja do sistema para acesso rápido.

## Instalação

### Requisitos

- Python 3.9+
- Pip

### Instalação das dependências

Execute o comando abaixo no terminal para instalar todas as dependências necessárias:

```sh
pip install -r requirements.txt
```

### Executando a Aplicação

Para iniciar o servidor Flask e o ícone da bandeja, execute:

```sh
python main.py
```

Isso iniciará um servidor local na porta `5410`, acessível via navegador em:

```
http://127.0.0.1:5410
```

## API Endpoints

### **Obter informações dos monitores**

**GET** `/monitors`

**Resposta:**

```json
{
  "status": "success",
  "data": [
    {
      "id": 0,
      "name": "Monitor 1",
      "width": 1920,
      "height": 1080,
      "is_primary": true
    }
  ]
}
```

### **Alterar a orientação de um monitor**

**POST** `/monitor`

**Corpo da requisição:**

```json
{
  "monitor": 0,
  "position": "portrait"
}
```

**Posições válidas:**

- `landscape`
- `portrait`
- `landscape_flipped`
- `portrait_flipped`

## Construindo o Executável

Para gerar um executável `.exe`, use o **PyInstaller**:

```sh
pyinstaller --onefile --windowed --add-data "templates;templates" --hidden-import "screeninfo" --hidden-import "rotatescreen" --add-data "icon.ico;." --icon "icon.ico" --name "Auto_Rotate_SC" main.py
```

O executável será gerado na pasta `dist/`.

## Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do repositório.
2. Crie um branch com sua feature: `git checkout -b minha-feature`
3. Commit suas alterações: `git commit -m 'Adicionei uma nova feature'`
4. Faça um push do seu branch: `git push origin minha-feature`
5. Abra um Pull Request.
