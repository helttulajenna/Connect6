# Connect6 engine

This project implements a Connect6 engine that communicates through standard input and output, following the official Connect6 text protocol.

## Requirements
- At least Python 3.10 or newer
- Install the necessary dependencies
  ```bash
  pip install -r requirements.txt

How to play?
First start the engine:
```bash
  python main.py
  ```

Example commands:
name
new black
next
print
exit

Command decription:
name - this will print the engine name
new black / new white - this will start a new game
black XXXX / white XXXX - apply given moves
move XXXX - opponent move and enfgine response
next - engine will play next move
depth d - sets time per move 
print - display ASCII board
exit - exit the engine

Important points to know before playing:
- The first black move is always the center
- Later turns place two stones near existing ones
- For the "tournament" in the class the GUI handles graphics and this engine only provides text-based logic

Extra!!
If you want to creat a standlone version for ubuntu, you can use this command:
pyinstaller --onefile main.py -n connect6_engine