# Debug Logs

Use este script para observar o disparo/acionamento das tags de eventos e screenviews, ajudando você a verificar imediatamente se os eventos estão sendo enviados.

O script apenas habilita o registro detalhado permitindo verificar se os eventos estão sendo registrados corretamente pelo SDK. Isso inclui eventos registrados manual e automaticamente.

## **Dependências**:
* [Python](https://www.python.org/)
* [Android Debug Bridge (adb)](https://developer.android.com/studio/command-line/adb)

## **Como utilizar**:
Inicialize seu emulador(Android Studio) ou dispositivo físico conectado, em seguida execute o script Python:

Android:
`python android_debug_logs.py` ou `python3 android_debug_logs.py`

iOS:
`python ios_debug_logs.py` ou `python3 ios_debug_logs.py`

Após executar esse script, será solicitado que você selecione uma das plataformas. Por exemplo, digite 0 para Firebase, 1 para Universal Analytics, etc.

Obs.: Adicione a flag Execute `-v` para receber mais detalhes ao iniciar a execução do script. Por exemplo: `python android_debug_logs.py -v`

#### Função secundária: Filtro
Execute no seu terminal: `python android_debug_logs.py -h` ou `python ios_debug_logs.py -h`

Nele verá as informações dos argumentos que você pode especificar.
* `python android_debug_logs.py -p1 "termo de busca 1" -p2 "termo de busca 2"`

    Exemplo (Firebase):
    `python android_debug_logs.py -p1 "select_item" -p2 "item_name=produto1"`

    O exemplo acima retornará logs que sejam de um evento chamado select_item e tenha como parâmetro item_name = produto1.

O filtro também pode ser realizado por RegEx.

* `python android_debug_logs.py -t1 "Add\ To\ Cart"`

   Você também pode buscar por apenas um termo. Nesse exemplo, você receberá o retorno do evento que tiver o valor "Add To Cart" atribuído a um de seus parâmetros.

No exemplo abaixo, você pode ainda buscar por dois ou mais termos usando ReGex da seguinte forma:

 * `python android_debug_logs.py -t1 "Add\ To\ Cart|select_content"`

   Nesse exemplo, você receberá como retorno o log contendo um evento chamado 'select_content' ou evento que contém "Add To Cart" como valor atribuído a um dos parâmetros.

    **O mesmo vale para o script relacionado ao Google Analytics Universal.**

### **Alguns comandos utilizados internamente no script**:
Firebase
```
adb shell setprop log.tag.FA-SVC VERBOSE
adb logcat -v time -s FA FA-SVC
```
Universal Analytics
```
adb shell setprop log.tag.GAv4-SVC DEBUG"
adb logcat -s GAv4-SVC"
```

### **Ferramentas sugeridas (Opcional)**:

[asdf](https://asdf-vm.com/guide/getting-started.html) -- Manage multiple runtime versions with a single CLI tool

[tmux](https://github.com/tmux/tmux/wiki) -- is a terminal multiplexer. It lets you switch easily between several programs in one terminal, detach them (they keep running in the background) and reattach them to a different terminal.
