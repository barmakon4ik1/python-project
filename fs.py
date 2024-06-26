import PySimpleGUI as psg
import logic


psg.set_options(font=('Courier New, monospace', 20))


def main_window():
    cat_list = ['Action', 'Animation', 'Children', 'Classics', 'Comedy', 'Documentary', 'Drama',
             'Family', 'Foreign', 'Games', 'Horror', 'Music', 'New', 'Sci-Fi', 'Sports', 'Travel']
    layout = [
        [psg.Text('Категория', size=(15, 2)), psg.DropDown(expand_x=True, values=cat_list, key='category')],
        [psg.Text('Год выпуска', size=(15, 2)),
         psg.DropDown(size=(5, 2), values=[n for n in range(1980, 2024)], key='year_start'),
         psg.Text("-"),
         psg.DropDown(size=(5, 2), values=[n for n in range(1980, 2024)], key='year_end')],
        [psg.Text('Название', size=(15, 2)), psg.Input(expand_x=True, key='title')],
        [psg.Text('Описание', size=(15, 2)), psg.Input(expand_x=True, key='description')],
        [psg.Text('Сортировать по ', size=(15, 2)),
         psg.DropDown(size=(15,2),  values=['alphabetically', 'new_first', 'old_first'], key='sort'),
         psg.Text('Сколько названий показать? ', size=(25, 2)), psg.Input(key='qty', size=(3,2), expand_x=True)],
        [psg.OK(expand_x=True), psg.Exit(expand_x=True)]
    ]

    window = psg.Window('Поисковая система Киноша', layout, enable_close_attempted_event=True)
    # запускаем основной бесконечный цикл
    while True:
        # получаем события, произошедшие в окне
        event, values = window.read()
        if event == 'btn_q':
            logic.request_statistics()
        if event == psg.WIN_CLOSED or event == 'Exit':
            break
        else:
            data = [values[k] for k in values.keys()]
            return data

        # закрываем окно и освобождаем используемые ресурсы
    window.close()



