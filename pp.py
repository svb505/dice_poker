import sqlite3
from datetime import datetime, timedelta
from tkinter import *
from tkinter import messagebox, simpledialog, ttk, colorchooser
from random import randint
import random
import tabulate

# Глобальные переменные
call_count = 0
turn = 0
dice_canvas_ids = []
check_vars = []
roll_count = 0
players = []
scores = []
obligatory_scores = []
matches_played = []
chosen_nominals = []
chosen_combinations = []
phase = "obligatory"  # "obligatory" или "main"
background_color = "White"
color_dice = "Red"
activefill_dice = "Yellow"
color = None
last_booster_activation_time = None
booster_active = False
dialog_roll = None
dialog_combination = None

dice_values = [random.randint(1, 6) for _ in range(5)]  # Переместил сюда для общей доступности
points0 = [random.randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6), randint(1, 6)]
def main_window():

    # Комбинации и их очки
    combinations = {
        "Покер": lambda dice: 5 in [dice.count(i) for i in range(1, 7)],
        "Пара": lambda dice: 2 in [dice.count(i) for i in range(1, 7)],
        "Две пары": lambda dice: [dice.count(i) for i in range(1, 7)].count(2) == 2,
        "Тройка": lambda dice: 3 in [dice.count(i) for i in range(1, 7)],
        "Малый стрит": lambda dice: [dice.count(i) for i in range(1, 7)].count(1) == 5 and
                                    [dice.count(i) for i in range(1, 7)][5] == 0,
        "Большой стрит": lambda dice: [dice.count(i) for i in range(1, 7)].count(1) == 5 and
                                      [dice.count(i) for i in range(1, 7)][0] == 0,
        "Чет": lambda dice: sum(1 for val in dice if val % 2 == 0) == 5,
        "Нечет": lambda dice: sum(1 for val in dice if val % 2 != 0) == 5,
        "Фулл-хаус": lambda dice: 3 in [dice.count(i) for i in range(1, 7)] and 2 in [dice.count(i) for i in
                                                                                      range(1, 7)],
        "Каре": lambda dice: 4 in [dice.count(i) for i in range(1, 7)],
        "Шанс": lambda dice: sum(dice)
    }



    def on_resize(event=None):
        global points0, dice_values

        canvas.delete("all")  # Очистка холста
        if event is None:
            # Используем текущий размер окна
            ChirinaWin = Win.winfo_width()
            VisotaWin = Win.winfo_height()
        else:
            # Используем размер окна из события изменения
            ChirinaWin = event.width
            VisotaWin = event.height

        # Определяем размер кубиков
        a = (ChirinaWin - 20 - 4 * 10) // 5

        # Вычисляем центр окна
        centr = ChirinaWin // 2

        # Перерисовываем кубики с новыми размерами и координатами
        draw_dice(a, centr - 2 * a - 10 * 2, VisotaWin // 2, dice_values[0])
        draw_dice(a, centr - a - 10, VisotaWin // 2, dice_values[1])
        draw_dice(a, centr, VisotaWin // 2, dice_values[2])
        draw_dice(a, centr + a + 10, VisotaWin // 2, dice_values[3])
        draw_dice(a, centr + 2 * a + 10 * 2, VisotaWin // 2, dice_values[4])

        canvas.update()  # Обновление холста после перерисовки

    def draw_dice(a, x, y, n):
        # Удаляем старое изображение кубика
        canvas.create_rectangle(x - a // 2, y - a // 2, x + a // 2, y + a // 2, fill=color_dice,
                                activefill=activefill_dice)
        # Рисуем точки на кубиках
        if n == 1:
            canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="black")
        elif n == 2:
            canvas.create_oval(x - a // 2 + 10, y + a // 2 - 10, x - a // 2 + 30, y + a // 2 - 30, fill="black")
            canvas.create_oval(x + a // 2 - 10, y - a // 2 + 10, x + a // 2 - 30, y - a // 2 + 30, fill="black")
        elif n == 3:
            canvas.create_oval(x - a // 2 + 10, y + a // 2 - 10, x - a // 2 + 30, y + a // 2 - 30, fill="black")
            canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="black")
            canvas.create_oval(x + a // 2 - 10, y - a // 2 + 10, x + a // 2 - 30, y - a // 2 + 30, fill="black")
        elif n == 4:
            canvas.create_oval(x - a // 2 + 10, y - a // 2 + 10, x - a // 2 + 30, y - a // 2 + 30, fill="black")
            canvas.create_oval(x - a // 2 + 10, y + a // 2 - 10, x - a // 2 + 30, y + a // 2 - 30, fill="black")
            canvas.create_oval(x + a // 2 - 10, y - a // 2 + 10, x + a // 2 - 30, y - a // 2 + 30, fill="black")
            canvas.create_oval(x + a // 2 - 10, y + a // 2 - 10, x + a // 2 - 30, y + a // 2 - 30, fill="black")
        elif n == 5:
            canvas.create_oval(x - a // 2 + 10, y - a // 2 + 10, x - a // 2 + 30, y - a // 2 + 30, fill="black")
            canvas.create_oval(x - a // 2 + 10, y + a // 2 - 10, x - a // 2 + 30, y + a // 2 - 30, fill="black")
            canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="black")
            canvas.create_oval(x + a // 2 - 10, y - a // 2 + 10, x + a // 2 - 30, y - a // 2 + 30, fill="black")
            canvas.create_oval(x + a // 2 - 10, y + a // 2 - 10, x + a // 2 - 30, y + a // 2 - 30, fill="black")
        elif n == 6:
            canvas.create_oval(x - a // 2 + 10, y - a // 2 + 10, x - a // 2 + 30, y - a // 2 + 30, fill="black")
            canvas.create_oval(x - a // 2 + 10, y - 10, x - a // 2 + 30, y + 10, fill="black")
            canvas.create_oval(x - a // 2 + 10, y + a // 2 - 10, x - a // 2 + 30, y + a // 2 - 30, fill="black")
            canvas.create_oval(x + a // 2 - 10, y - a // 2 + 10, x + a // 2 - 30, y - a // 2 + 30, fill="black")
            canvas.create_oval(x + a // 2 - 10, y - 10, x + a // 2 - 30, y + 10, fill="black")
            canvas.create_oval(x + a // 2 - 10, y + a // 2 - 10, x + a // 2 - 30, y + a // 2 - 30, fill="black")



    def apply_changes(dialog):
        global roll_count, dice_values, call_count, turn
        selected_dice = [var.get() for var in check_vars]
        for i, selected in enumerate(selected_dice):
            if selected:
                dice_values[i] = random.randint(1, 6)
        on_resize()  # Перерисовываем кубики после переброса
        roll_count += 1
        if roll_count >= 3:
            dialog.destroy()
            if phase == "obligatory":
                select_nominal()
            else:
                select_combination()
        else:
            dialog.destroy()
            open_roll_dialog()

    def askinteger(win, title, prompt, minvalue=None, maxvalue=None):
        def on_ok():
            try:
                value = int(entry.get())
                if (minvalue is not None and value < minvalue) or \
                        (maxvalue is not None and value > maxvalue):
                    raise ValueError
                result[0] = value
                dialog.destroy()
            except ValueError:
                messagebox.showwarning("Ошибка",
                                       f"Введите целое число от {minvalue} до {maxvalue}" if minvalue is not None and maxvalue is not None else "Введите целое число")

        def on_cancel():
            result[0] = None
            dialog.destroy()

        result = [None]

        dialog = Toplevel(win)
        dialog.title(title)
        askint_x = Win.winfo_x() + Win.winfo_width() // 2 - 135
        askint_y = Win.winfo_y() - Win.winfo_height() // 2 + 135
        if askint_x < 0:
            askint_x = 100
        if askint_y < 0:
            askint_y = 100
        dialog.geometry(f"+{askint_x}+{askint_y}")  # Устанавливаем положение окна
        dialog.resizable(False,False)
        Label(dialog, text=prompt).grid(row=0, column=0, padx=10, pady=10)
        entry = Entry(dialog)
        entry.grid(row=1, column=0, padx=10, pady=10)

        Button(dialog, text="OK", command=on_ok).grid(row=2, column=0, padx=10, pady=10)
        Button(dialog, text="Cancel", command=on_cancel).grid(row=2, column=1, padx=10, pady=10,sticky = W)

        dialog.transient(win)
        dialog.grab_set()
        win.wait_window(dialog)

        return result[0]
    def select_nominal():
        global turn, roll_count, scores, obligatory_scores, call_count, chosen_nominals, phase
        roll_count = 0
        available_nominals = [i for i in range(1, 7) if i not in chosen_nominals[turn]]
        nominal = askinteger(Win,"Выбор номинала",
                                          f"{players[turn]}, выберите номинал ({', '.join(map(str, available_nominals))}):",
                                          1, 6)


        if nominal and nominal in available_nominals:
            chosen_nominals[turn].append(nominal)
            count = dice_values.count(nominal)
            score = count - 3
            scores[turn] += score
            obligatory_scores[turn] += score
            matches_played[turn] += 1
            if matches_played[turn] == 6 and all(match == 6 for match in matches_played):
                show_obligatory_results()
                phase = "main"
                for i in range(len(matches_played)):
                    matches_played[i] = 0
                automatic_roll()
            else:
                next_turn()
        else:
            messagebox.showerror("Ошибка", "Недопустимый или уже выбранный номинал. Пожалуйста, выберите другой.")
            select_nominal()

    def show_obligatory_results():
        results = "\n".join(f"{players[i]}: {obligatory_scores[i]}" for i in range(len(players)))
        messagebox.showinfo("Обязаловка окончена", f"Этап обязаловки окончен. Очки:\n{results}")
        # Уничтожение окна в конце обязаловки не происходит
        # Закрытие всех открытых диалоговых окон

    def select_combination():
        global turn, roll_count, scores, call_count, phase, dialog_combination
        if dialog_combination:
            dialog_combination.destroy()  # Закрываем предыдущее окно выбора комбинации, если оно существует

        roll_count = 0
        available_combinations = [comb for comb in combinations.keys() if comb not in chosen_combinations[turn]]
        dialog_combination = Toplevel(Win)
        dialog_combination.title(f"{players[turn]}")
        dialog_combination.geometry("200x400")
        dialog_combination.transient(Win)
        dialog_combination.grab_set()
        center_child(dialog_combination, Win)
        dialog_combination.protocol("WM_DELETE_WINDOW", lambda: dismiss(dialog_combination))

        Label(dialog_combination, text=f"{players[turn]}, выберите комбинацию:").pack(pady=10)

        selected_combination = StringVar()
        for comb in available_combinations:
            ttk.Radiobutton(dialog_combination, text=comb, variable=selected_combination, value=comb).pack(anchor='w')

        def on_ok():
            combination = selected_combination.get()
            if combination in available_combinations:
                score = combinations[combination](dice_values)
                if score > 0:
                    scores[turn] += score
                    matches_played[turn] += 1
                    chosen_combinations[turn].append(combination)
                    dialog_combination.destroy()
                    if matches_played[turn] == 6 and all(match == 6 for match in matches_played):
                        show_final_results()
                        return
                    next_turn()
                else:
                    messagebox.showerror("Ошибка",
                                         "Выбранная комбинация не соответствует значениям костей. Пожалуйста, выберите другую.")
            else:
                messagebox.showerror("Ошибка",
                                     "Недопустимая или уже выбранная комбинация. Пожалуйста, выберите другую.")

        ttk.Button(dialog_combination, text="ОК", width=7, command=on_ok).pack(pady=10)
        Win.wait_window(dialog_combination)

    def show_final_results():
        global dialog_roll, dialog_combination
        results = "\n".join(
            f"{players[i]}: {scores[i]} (в т.ч. за обязаловку: {obligatory_scores[i]})" for i in range(len(players)))

        # Создаем окно с результатами
        Resulttt_win = Toplevel(Win)
        Resulttt_win.title("Игра окончена")
        Resulttt_win.geometry("250x250")
        Resulttt_win.resizable(False, False)
        center_child(Resulttt_win, Win)

        # Устанавливаем обработчик закрытия окна
        Resulttt_win.protocol("WM_DELETE_WINDOW", lambda: dismiss(Resulttt_win))

        # Создаем и размещаем виджеты в окне
        lbl = Label(Resulttt_win, text=f"Игра окончена. Итоговые очки:\n{results}")
        lbl.pack()

        btn = ttk.Button(Resulttt_win, text="Выйти", command=on_closing)
        btn.pack()

        # Устанавливаем захват ввода для окна
        Resulttt_win.grab_set()

        # Не блокируем выполнение программы, а просто ждем закрытия окна
        Win.wait_window(Resulttt_win)

    def dismiss(window):
        window.grab_release()
        window.destroy()

    def next_turn():
        global call_count, turn, roll_count, phase
        # Очистка холста перед рисованием новых кубиков
        canvas.delete("all")

        if phase == "obligatory" and all(match == 6 for match in matches_played):
            phase = "main"
            for i in range(len(matches_played)):
                matches_played[i] = 0
            show_obligatory_results()
            automatic_roll()
        else:
            turn = (turn + 1) % len(players)
            roll_count = 0
            status_label.config(text=f"Ход {players[turn]}")
            automatic_roll()
            if phase == "main" and all(
                    len(chosen_combinations[turn]) == len(combinations) for turn in range(len(players))):
                show_final_results()
                return
            if matches_played[turn] < 6:
                open_roll_dialog()
            else:
                next_turn()
    def center_up(Win,parent):
        Win.update_idletasks()  # Обновление размеров окна
        parent.update_idletasks()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()

        child_width = Win.winfo_width()
        child_height = Win.winfo_height()

        x = parent_x + parent_width // 2 - child_width // 2
        y = parent_y - child_height // 2

        Win.geometry(f'{child_width}x{child_height}+{x}+{y}')
    def center_child(Win, parent):
        Win.update_idletasks()  # Обновление размеров окна
        parent.update_idletasks()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()

        child_width = Win.winfo_width()
        child_height = Win.winfo_height()

        x = parent_x + parent_width // 2 - child_width // 2
        y = parent_y + parent_height // 2 - child_height // 2

        Win.geometry(f'{child_width}x{child_height}+{x}+{y}')

    def automatic_roll():
        global dice_values
        dice_values = [random.randint(1, 6) for _ in range(5)]

        # Пример вызова draw_dice для каждого кубика
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        a = (width - 20 - 4 * 10) // 5
        centr = width // 2

        for i, value in enumerate(dice_values):
            x = centr - 2 * a + i * (a + 10)  # Примерный расчет x
            y = height // 2
            draw_dice(a, x, y, value)
        open_roll_dialog()

    def open_roll_dialog():
        global roll_count, check_vars, phase, dialog_roll
        if dialog_roll:
            dialog_roll.destroy()  # Закрываем предыдущее окно переброса, если оно существует

        dialog_roll = Toplevel(Win)
        dialog_roll.title(f"Перебросить: {players[turn]}")
        dialog_roll.transient(Win)
        dialog_roll.geometry("240x200")
        dialog_roll.grab_set()
        center_up(dialog_roll, Win)
        dialog_roll.protocol("WM_DELETE_WINDOW", lambda: dismiss(dialog_roll))

        top_frame = Frame(dialog_roll)
        top_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        checkbox_frame = Frame(top_frame)
        checkbox_frame.pack(side="left", fill="y", anchor="n")

        label_frame = Frame(top_frame)
        label_frame.pack(side="right", fill="both", anchor="n", expand=True)

        button_frame = Frame(dialog_roll)
        button_frame.pack(side="bottom", fill="both", expand=True)

        available_nominals = [i for i in range(1, 7) if i not in chosen_nominals[turn]]
        avaible_combination = ""
        if phase == "main":
            for comb in combinations.keys():
                if comb not in chosen_combinations[turn]:
                    avaible_combination += comb + '\n'
            Label(label_frame, text=f"Доступные комбинации: \n {avaible_combination}", justify="left").pack(anchor="e")
        else:
            Label(label_frame, text=f"Доступные номиналы: \n {', '.join(map(str, available_nominals))}",
                  justify="left").pack(anchor="e")

        check_vars = [BooleanVar() for _ in range(5)]
        for i, var in enumerate(check_vars):
            ttk.Checkbutton(checkbox_frame, text=f"Кубик {i + 1}", variable=var).pack(anchor="w")

        ttk.Button(button_frame, text="Перебросить", command=lambda: apply_changes(dialog_roll)).pack(side="left",
                                                                                                      padx=10,
                                                                                                      pady=10)
        ttk.Button(button_frame, text="Не перебрасывать", command=lambda: [dialog_roll.destroy(),
                                                                           select_nominal() if phase == "obligatory" else select_combination()]).pack(
            side="right", padx=10, pady=10)

        Win.wait_window(dialog_roll)

    def parametr():
        global color_dice, activefill_dice, color, background_color,theme

        parametrs_window = Toplevel(Win)
        parametrs_window.title("Параметры")
        parametrs_window.geometry("450x350")
        parametrs_window.resizable(False, False)
        center_child(parametrs_window, Win)
        parametrs_window.protocol("WM_DELETE_WINDOW",
                                  lambda: dismiss(parametrs_window))  # Перехватываем нажатие на крестик

        # Фрейм для выбора цвета квадрата
        frmcolor = LabelFrame(parametrs_window, borderwidth=0.5, relief=SOLID, text="Цвет квадрата")
        frmcolor.grid(row=0, column=0, padx=5, pady=5, sticky=NW)

        # Кнопка для вызова диалогового окна выбора цвета
        choose_color_button = ttk.Button(frmcolor, text="Выбрать", command=lambda: choose_color(parametrs_window))
        choose_color_button.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        # Фрейм для выбора цвета активного квадрата
        frmcolor = LabelFrame(parametrs_window, borderwidth=0.5, relief=SOLID, text="Цвет активного квадрата")
        frmcolor.grid(row=0, column=1, padx=5, pady=5, sticky=NW)

        # Кнопка для вызова диалогового окна выбора цвета
        choose_color_button1 = ttk.Button(frmcolor, text="Выбрать", command=lambda: choose_color1(parametrs_window))
        choose_color_button1.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # Фрейм для выбора цвета фона
        frmcolor = LabelFrame(parametrs_window, borderwidth=0.5, relief=SOLID, text="Цвет фона")
        frmcolor.grid(row=0, column=2, padx=5, pady=5, sticky=NW)

        color_var = StringVar()
        # Устанавливаем значение по умолчанию для цвета фона
        if background_color is None:
            background_color = "White"  # Устанавливаем белый цвет по умолчанию, если еще не установлен
        color_var.set(background_color)

        # Кнопки радиокнопок для выбора цвета
        white = ttk.Radiobutton(frmcolor, text="Белый", variable=color_var, value="White")
        white.grid(row=0, column=0, sticky=W)
        black = ttk.Radiobutton(frmcolor, text="Черный", variable=color_var, value="Black")
        black.grid(row=1, column=0, sticky=W)
        gray = ttk.Radiobutton(frmcolor, text="Серый", variable=color_var, value="Gray")
        gray.grid(row=2, column=0, sticky=W)
        green = ttk.Radiobutton(frmcolor, text="Зеленый", variable=color_var, value="Green")
        green.grid(row=3, column=0, sticky=W)
        blue = ttk.Radiobutton(frmcolor, text="Синий", variable=color_var, value="Blue")
        blue.grid(row=4, column=0, sticky=W)
        goluboy = ttk.Radiobutton(frmcolor, text="Голубой", variable=color_var, value="Goluboy")
        goluboy.grid(row=5, column=0, sticky=W)
        violet = ttk.Radiobutton(frmcolor, text="Фиолетовый", variable=color_var, value="Violet")
        violet.grid(row=6, column=0, sticky=W)
        yellow = ttk.Radiobutton(frmcolor, text="Желтый", variable=color_var, value="Yellow")
        yellow.grid(row=7, column=0, sticky=W)
        malina = ttk.Radiobutton(frmcolor, text="Малиновый", variable=color_var, value="Malina")
        malina.grid(row=8, column=0, sticky=W)
        aliy = ttk.Radiobutton(frmcolor, text="Алый", variable=color_var, value="Alyi")
        aliy.grid(row=0, column=1, sticky=W)
        begiviy = ttk.Radiobutton(frmcolor, text="Бежевый", variable=color_var, value="Begiviy")
        begiviy.grid(row=1, column=1, sticky=W)
        salatoviy = ttk.Radiobutton(frmcolor, text="Салатовый", variable=color_var, value="Salat")
        salatoviy.grid(row=2, column=1, sticky=W)
        orange = ttk.Radiobutton(frmcolor, text="Оранжевый", variable=color_var, value="Orange")
        orange.grid(row=3, column=1, sticky=W)
        aqua = ttk.Radiobutton(frmcolor, text="Аква", variable=color_var, value="Aqua")
        aqua.grid(row=4, column=1, sticky=W)

        if color == "White":
            color_var.set("White")
        elif color == "Black":
            color_var.set("Black")
        elif color == "Gray":
            color_var.set("Gray")
        elif color == "Green":
            color_var.set("Green")
        elif color == "Blue":
            color_var.set("Blue")
        elif color == "#1E90FF":
            color_var.set("Goluboy")
        elif color == "#800080":
            color_var.set("Violet")
        elif color == "Yellow":
            color_var.set("Yellow")
        elif color == "#DC143C":
            color_var.set("Malina")
        elif color == "ff0d00":
            color_var.set("Alyi")
        elif color == "#FFE4E1":
            color_var.set("Begiviy")
        elif color == "#ADFF2F":
            color_var.set("Salat")
        elif color == "#FF8C00":
            color_var.set("Orange")
        elif color == "#00FFFF":
            color_var.set("Aqua")



        # Кнопки
        ok_button = ttk.Button(parametrs_window, text="Ок", command=lambda: ok_click(color_var,parametrs_window))
        ok_button.grid(row=4, column=1, padx=5, pady=5, sticky=E)
        otmena_button = ttk.Button(parametrs_window, text="Отмена", command=lambda: dismiss(parametrs_window))
        otmena_button.grid(row=4, column=2, padx=5, pady=5, sticky=W)
        canvas.update()
        parametrs_window.grab_set()  # Захватываем пользовательский ввод

    def choose_color(parameters_window):
        global color_dice
        parameters_window.grab_release()  # Освобождаем захват для модального окна
        color_code = colorchooser.askcolor(title="Выбор цвета")[1]
        parameters_window.grab_set()  # Захватываем пользовательский ввод снова
        if color_code:
            color_dice = color_code
        canvas.update()
        on_resize()
        parameters_window.focus_set()

    def choose_color1(parameters_window):
        global activefill_dice
        parameters_window.grab_release()  # Освобождаем захват для модального окна
        color_code = colorchooser.askcolor(title="Выбор цвета")[1]
        parameters_window.grab_set()  # Захватываем пользовательский ввод снова
        if color_code:
            activefill_dice = color_code
        on_resize()
        canvas.update()
        parameters_window.focus_set()

    def ok_click(color_var,parametrs_window):
        global color, background_color, color_dice, activefill_dice

        background_color = color_var.get()

        # Установка цвета фона
        color = background_color

        # Применяем выбранные пользователем цвета квадрата и активного квадрата
        if color_dice is None:
            color_dice = "Red"  # Если цвет квадрата не выбран, установить по умолчанию
        if activefill_dice is None:
            activefill_dice = "Yellow"  # Если цвет активного квадрата не выбран, установить по умолчанию

        if color_var.get() == "White":
            color = "White"
            background_color = "White"
        elif color_var.get() == "Black":
            color = "Black"
            background_color = "Black"
        elif color_var.get() == "Gray":
            color = "Gray"
            background_color = "Gray"
        elif color_var.get() == "Blue":
            color = "Blue"
            background_color = "Blue"
        elif color_var.get() == "Yellow":
            color = "Yellow"
            background_color = "Yellow"
        elif color_var.get() == "Yellow":
            color = "Yellow"
            background_color = "Yellow"
        elif color_var.get() == "Malina":
            color = "#DC143C"
            background_color = "#DC143C"
        elif color_var.get() == "Begiviy":
            color = "#FFE4E1"
            background_color = "#FFE4E1"
        elif color_var.get() == "Goluboy":
            color = "#1E90FF"
            background_color = "#1E90FF"
        elif color_var.get() == "Violet":
            color = "#800080"
            background_color = "#800080"
        elif color_var.get() == "Alyi":
            color = "ff0d00"
            background_color = "ff0d00"
        elif color_var.get() == "Salat":
            color = "#ADFF2F"
            background_color = "#ADFF2F"
        elif color_var.get() == "Aqua":
            color = "#00FFFF"
            background_color = "#00FFFF"
        elif color_var.get() == "Orange":
            color = "#FF8C00"
            background_color = "#FF8C00"
        else:
            color = "Green"
            background_color = "Green"


        parametrs_window.destroy()
        update_canvas_background()  # Обновление фона канвы
        on_resize()  # Перерисовка канвы с новым фоном

    def update_canvas_background():
        global background_color
        canvas.config(bg=background_color)
    def exit_cascade(event=None):

        def yes_button():
            global flag
            flag = True

            # Подключение к базе данных (создание, если не существует)
            conn = sqlite3.connect('playersinfo_poker.db')

            # Создаем курсор
            cursor = conn.cursor()

            # Создаем таблицу (если не существует)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS players (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    color_dice TEXT,
                    background_color TEXT,
                    score INTEGER,
                    time TEXT
                )
            ''')

            # Вставка данных
            for player, score in zip(players, scores):
                cursor.execute('''
                    INSERT INTO players (name, color_dice, background_color, score, time) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (player, color_dice, background_color, score, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

            # Пример выборки данных (для проверки, можно удалить позже)
            cursor.execute('''SELECT * FROM players''')
            rows = cursor.fetchall()
            for row in rows:
                print(row)  # Вывод данных в консоль, можно удалить или заменить на другой метод отображения

            # Сохраняем изменения
            conn.commit()

            # Закрываем подключение
            conn.close()
            exit_win.destroy()
            Win.destroy()

        def non_button():
            exit_win.destroy()

        exit_win = Toplevel(Win)
        exit_win.title("Выход")
        exit_win.geometry("250x120")
        exit_win.resizable(False, False)
        center_child(exit_win, Win)
        exit_win.protocol("WM_DELETE_WINDOW", lambda: dismiss(exit_win))  # Перехватываем нажатие на крестик

        label1 = Label(exit_win, text="Вы действительно хотите выйти из игры?")
        label1.pack()
        btn1 = ttk.Button(exit_win, text="Да", command=yes_button)
        btn1.pack()
        btn2 = ttk.Button(exit_win, text="Нет", command=non_button)
        btn2.pack()
        exit_win.grab_set()  # Захватываем пользовательский ввод

    def on_closing():
        global flag
        flag = True
        if flag == True:
            # 2. Создаем подключение к базе данных (если базы данных не существует, она будет создана)
            conn = sqlite3.connect('playersinfo_poker.db')
            # 3. Создаем курсор
            cursor = conn.cursor()
            # 4. Выполняем SQL-запросы
            # Пример создания таблицы
            cursor.execute('''
                                    CREATE TABLE IF NOT EXISTS players (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        color_dice INTEGER,
                        background_color INTEGER,
                        score INTEGER,
                        time TEXT
                                    )
                                ''')
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Прмер вставки данных
            for player, score in zip(players, scores):
                cursor.execute('''
                    INSERT INTO players (name, color_dice, background_color, score, time) 
                    VALUES (?, ?, ?, ?, ?)
                ''', (player, color_dice, background_color, score, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            # Пример выборки данных
            cursor.execute('''SELECT * FROM players ''')
            # Сохраняем изменения
            conn.commit()
            # 5. Закрываем подключение
            conn.close()

        Win.destroy()



    def win_booster():
        def no_activ_booster():
            booster_win.destroy()

        booster_win = Toplevel(Win)
        booster_win.title("Бустер")
        booster_win.geometry("400x150")
        booster_win.resizable(False, False)
        center_child(booster_win, Win)
        booster_win.protocol("WM_DELETE_WINDOW",
                             lambda: dismiss(booster_win))  # Перехватываем нажатие на крестик
        lbl = Label(booster_win, text="Данный бустер будет удваивать очки в течении 3-х минут.")
        lbl.pack()
        lbl1 = Label(booster_win, text="Следующий бустер можно будет активироать только через 6 часов")
        lbl1.pack()
        btn1 = ttk.Button(booster_win, text="Активировать бустер", command=booster_activate)
        btn1.pack()
        btn2 = ttk.Button(booster_win, text="Не активировать", command=no_activ_booster)
        btn2.pack()

    def data_razrab():
        n = messagebox.showinfo(title="Данные про разработчиков",
                            message="Разработчики данной игры Булыгин Святослав и Cергей Багач")
    def data_game():
        messagebox.showinfo(title="Данные про разработчиков",
                            message="Игра создана на языке программирования Python с помощью библиотеки Tkinter")

    def all_data_users():
        all_data_users_win = Toplevel(Win)
        all_data_users_win.title("Полные параметры пользоватей")
        all_data_users_win.geometry("650x350")
        all_data_users_win.resizable(False, False)
        center_child(all_data_users_win, Win)
        all_data_users_win.protocol("WM_DELETE_WINDOW",
                                    lambda: dismiss(all_data_users_win))  # Перехватываем нажатие на крестик
        n = Text(all_data_users_win)
        scrollbar = Scrollbar(all_data_users_win, command=n.yview)
        n.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        n.pack()

        conn = sqlite3.connect('playersinfo_poker.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT name,
                score,
               color_dice, 
                background_color,
               time
        FROM players
        ORDER BY name DESC;''')
        rows = cursor.fetchall()
        # Определение заголовков столбцов
        columns = ["Name", "Score", "Color_dice ", "Background_color", "Time"]

        # Форматирование данных с помощью tabulate
        results = tabulate.tabulate(rows, headers=columns, tablefmt="center")

        n.insert(1.0, str(results) + '\n')
        conn.commit()
        conn.close()
        all_data_users.grab_set()  # Захватываем пользовательский ввод

    def data_users():
        data_users_win = Toplevel(Win)
        data_users_win.title("Сокращеные данные пользоватей")
        data_users_win.geometry("450x350")
        data_users_win.resizable(False, False)
        center_child(data_users_win, Win)
        data_users_win.protocol("WM_DELETE_WINDOW",
                                lambda: dismiss(data_users_win))  # Перехватываем нажатие на крестик
        n = Text(data_users_win)
        scrollbar = Scrollbar(data_users_win, command=n.yview)
        n.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        n.pack()

        conn = sqlite3.connect('playersinfo_poker.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT name, SUM(score) AS total_score
                FROM players
                GROUP BY name
                ORDER BY total_score DESC;''')
        rows = cursor.fetchall()
        # Определение заголовков столбцов
        columns = ["Name", "Score"]

        # Форматирование данных с помощью tabulate
        results = tabulate.tabulate(rows, headers=columns, tablefmt="center")

        n.insert(1.0, str(results) + '\n')
        conn.commit()
        conn.close()
        data_users.grab_set()  # Захватываем пользовательский ввод

    def booster_activate():
        global booster_active, last_booster_activation_time

        # Проверяем время последней активации бустера
        if last_booster_activation_time is not None:
            time_passed = datetime.now() - last_booster_activation_time
            if time_passed < timedelta(hours=6):
                remaining_time = timedelta(hours=6) - time_passed
                messagebox.showinfo("Бустер недоступен",
                                    f"Вы сможете активировать бустер через {remaining_time}.")
                return

        # Активируем бустер на 3 минуты
        booster_active = True
        last_booster_activation_time = datetime.now()
        messagebox.showinfo("Бустер активирован",
                            "Ваши очки за будут удваиваться в течение 3 минут.")
        Win.after(180000, booster_deactivate)  # Деактивация бустера через 3 минуты

    def booster_deactivate():
        global booster_active
        booster_active = False
        messagebox.showinfo("Бустер деактивирован", "Действие бустера закончилось.")
    def config_win1():
        Win.update_idletasks()

        # Получаем размеры экрана
        screen_width = Win.winfo_screenwidth()
        screen_height = Win.winfo_screenheight()

        # Вычисляем координаты для центрирования окна
        x = int((screen_width / 2) - (screen_width / 2))
        y = int((screen_height / 2) - (screen_height / 2))

        # Устанавливаем размеры и позицию окна
        Win.geometry(f"{screen_width}x{screen_height}+{x}+{y}")

        # Разворачиваем окно на весь экран, сохраняя кнопки управления
        Win.state('zoomed')
    def pravila():
        pravila_win = Toplevel(Win)
        pravila_win.title("Правила игры")
        pravila_win.geometry("750x400")
        pravila_win.resizable(False, False)
        center_child(pravila_win, Win)
        pravila_win.protocol("WM_DELETE_WINDOW",
                          lambda: dismiss(pravila_win)) # Перехватываем нажатие на крестик
        font_settings = ("Arial", 15, "bold")
        lbl = Label(pravila_win,
                    text="Правила покера на костях:", font = font_settings)

        lbl.pack()
        setting = ("Arial", 9, "bold")
        lbl1 = Label(pravila_win,
                    text="Правила покера на костях \n Сначала игроки проходят этап с названием ,,обязаловка'' которая идет до тех пор пока \n каждый из игроков не выбросит все цифры. \n"
                         " В этом этапе главная цель - выбросить как можно больше костей одного номинала \n иначе начислиться штраф. Если ты выбрасываешь 3 кости одного номинала то ты получаешь 0 очков.\n"
                         "Если ты выбрасыаешь 4 двойки тогда ты получаешь +2 очка, 4 шестерки: +6 очков, 4 тройки: +3 очка и тд.\n Выбрасыаешь 5 двоек тогда ты получаешь +4 очка, 5 шестерок: +12 очков, 5 троек: +6 очка и тд\n"
                         "Такая же схема и в обратную сторону.\nЕсли ты выбрасыаешь 2 двойки тогда ты получаешь -2 очка, 2 шестерки: -6 очков, 2 тройки: -3 очка и тд.\n После конца обязаловки начинаеться основная игра цель которой выбрасывать комбинацции по типу. Пара, Каре,Покер и тд.\n Подробнее "
                         "о комбинация можете почитать в разделе ,,Обьяснение комбинаций''.\n Основная игра длиться 6 раундов для каждого игрока по окончанию которой подводяться результаты игры",
                    font=setting)

        lbl1.pack()
        btn = ttk.Button(pravila_win,text = "Перейти в раздел ,,Обьяснение комбинаций''", command = help_user)
        btn.pack()
        pravila_win.grab_set()  # Захватываем пользовательский ввод
    def help_user():
        help_win = Toplevel(Win)
        help_win.title("Обьяснение комбинаций")
        help_win.geometry("450x350")
        help_win.resizable(False, False)
        center_child(help_win, Win)
        help_win.protocol("WM_DELETE_WINDOW",
                                lambda: dismiss(help_win))  # Перехватываем нажатие на крестик
        lbl = Label(help_win,text = "Покер - 5 костей одного номинала \n Пара - две кости одинакового номинала \n Две пары - 2 пары костей одного номинала \n Тройка - 3 кости одного номинала"
                           "\n Малый стрит - кости с номиналом 1,2,3,4,5 \n Большой стрит - кости с номиналом 2,3,4,5,6 \n Чет - все кости четные \n"
                           "Нечет - все кости не четные \n Фулл-хауз - 3 кости одного номинала и еще 2 кости другого номинала \n Каре - 4 кости одного номинала"
                           "\n Шанс - любая комбинация")
        lbl.pack()
        help_win.grab_set()  # Захватываем пользовательский ввод
    def start_game():
        global call_count, turn, dice_values, roll_count, players, scores, obligatory_scores, matches_played, chosen_nominals, chosen_combinations, phase
        call_count = 0
        turn = 0
        dice_values = [random.randint(1, 6) for _ in range(5)]
        num_players = simpledialog.askinteger("Количество игроков", "Введите количество игроков (2-5):", minvalue=2,
                                              maxvalue=5, parent=Win)
        if num_players:
            players = [simpledialog.askstring("Имя игрока", f"Введите имя игрока {i + 1}:", parent=Win) for i in
                       range(num_players)]

            scores = [0 for _ in range(num_players)]
            obligatory_scores = [0 for _ in range(num_players)]
            matches_played = [0 for _ in range(num_players)]
            chosen_nominals = [[] for _ in range(num_players)]
            chosen_combinations = [[] for _ in range(num_players)]
            phase = "obligatory"
            turn = 0
            call_count = 0
            dice_values = [random.randint(1, 6) for _ in range(5)]
            status_label.config(text=f"Ход {players[turn]}")

            on_resize()  # Вызов функции для установки начального состояния
            open_roll_dialog()

    Win = Tk()
    Win.title("Игра в кости")
    Win.title("Покер на костях")
    Win.minsize(450, 250)
    Win.resizable(True, True)
    Win.option_add("*tearOff", FALSE)
    VisotaScreen = Win.winfo_screenheight()
    ChirinaScreen = Win.winfo_screenwidth()
    VisotaWin = 450
    ChirinaWin = 900
    Win.geometry(
        f"{ChirinaWin}x{VisotaWin}+{ChirinaScreen // 2 - ChirinaWin // 2}+{VisotaScreen // 2 - VisotaWin // 2}")

    main_menu = Menu()
    info_menu = Menu()
    file_menu = Menu(main_menu, tearoff=0)
    view_menu = Menu()
    help_menu = Menu()
    main_menu.add_cascade(label="Игра", underline=0, menu=file_menu)
    file_menu.add_command(label="Начать", command=start_game)
    main_menu.add_cascade(label = "Вид", menu = view_menu)
    view_menu.add_cascade(label="Параметры", command=parametr)
    view_menu.add_command(label="На полный екран", command=config_win1)
    main_menu.add_cascade(label="Инфо", menu=info_menu)
    main_menu.add_command(label='Бустеры', command=win_booster)
    main_menu.add_cascade(label = "Правила игры", menu = help_menu)
    help_menu.add_cascade(label = "Обьяснение комбинаций", command = help_user)
    help_menu.add_cascade(label = "Правила", command = pravila)
    main_menu.add_cascade(label="Выход", command=exit_cascade)
    info_menu.add_command(label="Данные про разработчиков", command=data_razrab)
    info_menu.add_command(label="Данные про игру", command=data_game)
    info_menu.add_command(label="Полные данные пользоватей", command=all_data_users)
    info_menu.add_command(label="Сокращеные данные про пользователей", command=data_users)

    canvas = Canvas(Win, bg="white")
    canvas.pack(fill=BOTH, expand=YES)
    canvas.bind("<Configure>", on_resize)
    Win.config(menu=main_menu)
    Win.bind('<Escape>', exit_cascade)
    Win.bind('<Alt-F4>', exit_cascade)
    Win.protocol("WM_DELETE_WINDOW", on_closing)
    status_label = Label(Win, text="Добро пожаловать в игру!")
    status_label.pack()

    Win.mainloop()
main_window()



