* Instruções para instalar todas as dependências

Para garantir que o sistema tem todas as bibliotecas e importações necessárias, conceda privilégio de execução para o arquivo install.sh e o execute para iniciar a interface. Na pasta raíz do trabalho:

    chmod +x install.sh
    ./install.sh


* Instruções para execução do experimento

1. Para se conectar com a placa, utilizamos o openocd e os scripts escritos, digitando na pasta raíz do projeto. O argumento após -l é o nome do arquivo em que se deseja armazenar os logs, a interface apenas procura os arquivos dentro do path "interface/data/", então pode escolher qualquer nome para o log desde que esteja dentro deste diretório.

    riscv-openocd/bin/openocd -f scripts/olimex-arm-usb-tiny-h.cfg -f scripts/digilent.cfg -l interface/data/log

2. Para enviar comandos e receber as respostas que serão armazenadas no arquivo utilizado pela interface, em outro terminal iniciamos o telnet e o conectamos a porta 4444, onde o openocd espera por padrão para receber comandos. De forma a fazer as respostas da placa serem escritas no arquivo de log, utilizamos tee, passando append (-a) como argumento e o mesmo path para o log utilizado no comando anterior do openocd.
 
    telnet localhost 4444 | tee -a -i interface/data/log

3. Para iniciar a interface gráfica, conceda privilégio de execução para o arquivo launch.sh e o execute para iniciar a interface. Na pasta raíz do trabalho, onde está o arquivo launch.sh:

    chmod +x launch.sh
    ./launch.sh
