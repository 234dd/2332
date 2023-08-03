import json
import random
import requests
import vk_api
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from config import Config
from api import Api
from users import Users
from rcon import Rcon


def getSettings():
    config_settings = Config(file="settings.json", mode="json")
    return config_settings


def auth():
    try:
        vk = vk_api.VkApi(token=getSettings().get('token'))
        group_id = getSettings().get('group_id')
        long_poll = VkBotLongPoll(vk=vk, group_id=group_id)
        print('[!] Авторизация прошла успешно!')
        return long_poll
    except Exception as error:
        print(f'[!] Авторизация не прошла!\n[!] Текст ошибки -> {error}')


def menu():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button(label='Мой профиль', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button(label='Топ отчетов', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button(label='Топ варнов', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button(label='Топ медалей', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button(label='Топ балансов', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button(label='Дневная норма', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(label='Магазин', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(label='Онлайн', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(label='Admin panel', color=VkKeyboardColor.NEGATIVE)
    return keyboard


def admin_menu():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button(label='Профили пользователей', color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(label='Айдишники пользователей', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button(label='Сброс дневного топа', color=VkKeyboardColor.SECONDARY)
    keyboard.add_button(label='Сброс недельного топа', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button(label='В меню', color=VkKeyboardColor.POSITIVE)
    return keyboard


def shop_menu():
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button(label='Отпуск на 3 дня', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(label='100 айронов', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(label='Отпуск на 5 дней', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(label='200 айронов', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(label='Отпуск на 7 дней', color=VkKeyboardColor.POSITIVE)
    keyboard.add_button(label='500 айронов', color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(label='Дроп-кейс', color=VkKeyboardColor.SECONDARY)
    keyboard.add_line()
    keyboard.add_button(label='Обмен валютами', color=VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button(label='В меню', color=VkKeyboardColor.SECONDARY)
    return keyboard


def bot():
    try:
        global command
        long_poll = auth()
        users = Users()
        rcon = Rcon()
        print('[!] Бот запущен!')
        api = Api(token=getSettings().get('token'), user_token=getSettings().get('user_token'))
        print('[!] Апи подключено!')
        for event in long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                user_id = event.object['message']['from_id']
                peer_id = event.object['message']['peer_id']
                message_id = event.object['message']['id']

                text = event.object['message']['text']
                args = text.split()
                try:
                    command = args[0]
                    del args[0]
                except:
                    pass

                if text == 'Обмен валютами':
                    text = '[ℹ️] Информация о товаре:\n' \
                           '├ Название: Обмен валютами\n' \
                           '├ Описание: Текущий курс - 10💸=200.000$, 1.000.000$=10💸\n' \
                           '├ Для обмена необходимо написать @work_logs или @krushbtw.'
                    api.send(peer_id=peer_id, text=text)

                if text == 'Отпуск на 7 дней':
                    text = '[ℹ️] Информация о товаре:\n' \
                           '├ Название: Отпуск на 7 дней\n' \
                           f'├ Описание: После покупки Вы будете освобождены от своих обязанностей на 7 дней\n' \
                           f'├ Цена: {getSettings().get("shop")["otpusk_7_days"]["price"]}💸'
                    keyboard = VkKeyboard(one_time=False, inline=True)
                    keyboard.add_callback_button(label='Купить', color=VkKeyboardColor.POSITIVE,
                                                 payload={"text": "OK.", 'hash': f'{peer_id}_buy_otpusk7',
                                                          "type": "show_snackbar"}
                                                 )
                    api.send_keyboard(message=text, peer_id=peer_id, keyboard=keyboard.get_keyboard())

                if text == 'Отпуск на 5 дней':
                    text = '[ℹ️] Информация о товаре:\n' \
                           '├ Название: Отпуск на 5 дней\n' \
                           f'├ Описание: После покупки Вы будете освобождены от своих обязанностей на 5 дней\n' \
                           f'├ Цена: {getSettings().get("shop")["otpusk_5_days"]["price"]}💸'
                    keyboard = VkKeyboard(one_time=False, inline=True)
                    keyboard.add_callback_button(label='Купить', color=VkKeyboardColor.POSITIVE,
                                                 payload={"text": "OK.", 'hash': f'{peer_id}_buy_otpusk5',
                                                          "type": "show_snackbar"}
                                                 )
                    api.send_keyboard(message=text, peer_id=peer_id, keyboard=keyboard.get_keyboard())

                if text == 'Отпуск на 3 дня':
                    text = '[ℹ️] Информация о товаре:\n' \
                           '├ Название: Отпуск на 3 дня\n' \
                           f'├ Описание: После покупки Вы будете освобождены от своих обязанностей на 3 дня\n' \
                           f'├ Цена: {getSettings().get("shop")["otpusk_3_days"]["price"]}💸'
                    keyboard = VkKeyboard(one_time=False, inline=True)
                    keyboard.add_callback_button(label='Купить', color=VkKeyboardColor.POSITIVE,
                                                 payload={"text": "OK.", 'hash': f'{peer_id}_buy_otpusk3',
                                                          "type": "show_snackbar"}
                                                 )
                    api.send_keyboard(message=text, peer_id=peer_id, keyboard=keyboard.get_keyboard())

                if text == '500 айронов':
                    text = '[ℹ️] Информация о товаре:\n' \
                           '├ Название: 500 айронов\n' \
                           f'├ Описание: После покупки Вам автоматически выдастся 500 айронов на указанный Вами режим\n' \
                           f'├ Цена: {getSettings().get("shop")["donate_money_500"]["price"]}💸'
                    keyboard = VkKeyboard(one_time=False, inline=True)
                    keyboard.add_callback_button(label='Купить', color=VkKeyboardColor.POSITIVE,
                                                 payload={"text": "OK.", 'hash': f'{peer_id}_buy_500donmoney',
                                                          "type": "show_snackbar"}
                                                 )
                    api.send_keyboard(message=text, peer_id=peer_id, keyboard=keyboard.get_keyboard())

                if text == '200 айронов':
                    text = '[ℹ️] Информация о товаре:\n' \
                           '├ Название: 200 айронов\n' \
                           f'├ Описание: После покупки Вам автоматически выдастся 200 айронов на указанный Вами режим\n' \
                           f'├ Цена: {getSettings().get("shop")["donate_money_200"]["price"]}💸'
                    keyboard = VkKeyboard(one_time=False, inline=True)
                    keyboard.add_callback_button(label='Купить', color=VkKeyboardColor.POSITIVE,
                                                 payload={"text": "OK.", 'hash': f'{peer_id}_buy_200donmoney',
                                                          "type": "show_snackbar"}
                                                 )
                    api.send_keyboard(message=text, peer_id=peer_id, keyboard=keyboard.get_keyboard())

                if text == '100 айронов':
                    text = '[ℹ️] Информация о товаре:\n' \
                           '├ Название: 100 айронов\n' \
                           f'├ Описание: После покупки Вам автоматически выдастся 100 айронов на указанный Вами режим\n' \
                           f'├ Цена: {getSettings().get("shop")["donate_money_100"]["price"]}💸'
                    keyboard = VkKeyboard(one_time=False, inline=True)
                    keyboard.add_callback_button(label='Купить', color=VkKeyboardColor.POSITIVE,
                                                 payload={"text": "OK.", 'hash': f'{peer_id}_buy_100donmoney',
                                                          "type": "show_snackbar"}
                                                 )
                    api.send_keyboard(message=text, peer_id=peer_id, keyboard=keyboard.get_keyboard())

                if text == 'Дроп-кейс':
                    text = '[ℹ️] Информация о товаре:\n' \
                           '├ Название: Дроп-кейс\n' \
                           f'├ Описание: После покупки Вам автоматически выдастся дроп-кейс на указанный Вами режим\n' \
                           f'├ Цена: {getSettings().get("shop")["case"]["price"]}💸'
                    keyboard = VkKeyboard(one_time=False, inline=True)
                    keyboard.add_callback_button(label='Купить', color=VkKeyboardColor.POSITIVE,
                                                 payload={"text": "OK.", 'hash': f'{peer_id}_buy_case',
                                                          "type": "show_snackbar"}
                                                 )
                    api.send_keyboard(message=text, peer_id=peer_id, keyboard=keyboard.get_keyboard())

                if text == 'Онлайн':
                    names = [i for i in users.getAll()]
                    names1 = []
                    admins = []
                    for i in names:
                        names1.append(users.getName(str(i)))
                    a = requests.get(url='http://ironmine.fun/api/rcon/index.php?mode=grief&command=list').text
                    all_grief = a.split()[1]
                    a = a.split(':')
                    del a[0]
                    b = requests.get(url='http://ironmine.fun/api/rcon/index.php?mode=surv&command=list').text
                    all_surv = b.split(' ')[1]
                    b = b.split(':')
                    del b[0]
                    if len(b[0]) != 0:
                        b = b[0].replace('\r\n', '')
                    else:
                        b = 'Пусто.'
                    if len(a[0]) != 0:
                        a = a[0].replace('\r\n', '')
                    else:
                        a = 'Пусто.'
                    text = f'[ℹ️] Онлайн на режиме гриферства ({all_grief}):\n├ {"".join(a)}\n\n[ℹ️] Онлайн на режиме выживания ({all_surv}):\n├ {"".join(b)}'
                    api.send(peer_id=peer_id, text=text)

                if text == 'Топ балансов':
                    text = '[🔝] Топ балансов:\n'
                    f = json.loads(open(file='users.json', mode='r').read())
                    a, a1 = [], {}
                    for i in f:
                        if users.getUser(str(i))['balance'] != 0:
                            a.append(users.getUser(str(i))['balance'])
                            a1[users.getUser(str(i))['balance']] = users.getUser(str(i))['id']
                    a.sort()
                    a.reverse()
                    for i in a:
                        text += f'├ {users.getName(a1.get(i))} | {users.getRole(a1.get(i))} - {users.getBalance(a1.get(i))}.\n'
                    api.send(peer_id=peer_id, text=text)

                if text == 'Айдишники пользователей':
                    text = '[✅] Список:\n'
                    n = 1
                    f = json.loads(open(file='users.json', mode='r').read())
                    for i in f:
                        info = users.getUser(str(i))
                        text += f"{n}. {info['name']} - {info['id']}\n"
                        n += 1
                    api.send(peer_id=peer_id, text=text)

                if text == 'В меню':
                    api.send_keyboard(peer_id=peer_id, keyboard=menu().get_keyboard(), message='[✅] Отправляю меню...')

                if text == 'Магазин':
                    api.send_keyboard(peer_id=peer_id, message='[✅] Магазин:', keyboard=shop_menu().get_keyboard())

                if text == 'Профили пользователей':
                    keyboard = VkKeyboard(inline=True, one_time=False)
                    f = json.loads(open(file='users.json', mode='r').read())
                    n = 0
                    for i in f:
                        keyboard.add_callback_button(label=str(users.getName(str(i))), color=VkKeyboardColor.PRIMARY,
                                                     payload={"text": "OK.", 'hash': f'{users.getName(str(i))}_profile',
                                                              "type": "show_snackbar"})
                        if n % 4 == 0:
                            keyboard.add_line()
                        else:
                            pass
                        n += 1
                    api.send_keyboard(peer_id=peer_id, message='[✅] Чей профиль смотрим?',
                                      keyboard=keyboard.get_keyboard())

                if text == 'Admin panel':
                    if users.getRoleById(str(user_id)) >= getSettings().get('min_role_for_admin_panel'):
                        api.send_keyboard(peer_id=peer_id, keyboard=admin_menu().get_keyboard(),
                                          message='[✅] Отправляю меню...')
                    else:
                        api.send(peer_id=peer_id, text='[❗] У вас нет прав!')

                if text == 'Топ медалей':
                    text = '[🔝] Топ медалей:\n'
                    f = json.loads(open(file='users.json', mode='r').read())
                    a, a1 = [], {}
                    for i in f:
                        if users.getUser(str(i))['medals'] != 0:
                            a.append(users.getUser(str(i))['medals'])
                            a1[users.getUser(str(i))['medals']] = users.getUser(str(i))['id']
                    a.sort()
                    a.reverse()
                    for i in a:
                        if users.getRoleById(a1.get(i)) < 4:
                            text += f'├ {users.getName(a1.get(i))} | {users.getRole(a1.get(i))} - {users.getMedals(a1.get(i))}.\n'
                    api.send(peer_id=peer_id, text=text)

                if text == 'Дневная норма':
                    f = json.loads(open(file='users.json', mode='r').read())
                    norma = "[ℹ️] Дневная норма:\n"
                    for i in f:
                        if users.getRoleById(str(i)) == 1:
                            if users.getDayReports(str(i)) >= 5:
                                norma += f"├ {users.getName(str(i))} | {users.getRole(str(i))} - ✅\n"
                            else:
                                norma += f"├ {users.getName(str(i))} | {users.getRole(str(i))} - ⛔\n"
                        elif users.getRoleById(str(i)) == 2:
                            if users.getDayReports(str(i)) >= 7:
                                norma += f"├ {users.getName(str(i))} | {users.getRole(str(i))} - ✅\n"
                            else:
                                norma += f"├ {users.getName(str(i))} | {users.getRole(str(i))} - ⛔\n"
                    api.send(peer_id=peer_id, text=norma)

                if text == 'Топ варнов':
                    text = '[🔝] Топ варнов:\n'
                    f = json.loads(open(file='users.json', mode='r').read())
                    for i in f:
                        if users.getRoleById(str(i)) < 4:
                            text += f'├ {users.getName(str(i))} | {users.getRole(str(i))} - {users.getWarns(str(i))}/3.\n'
                    api.send(peer_id=peer_id, text=text)

                if text == 'Сброс дневного топа':
                    f = json.loads(open(file='users.json', mode='r').read())
                    a, a1 = [], {}
                    for i in f:
                        if users.getUser(str(i))['days_reports'] != 0:
                            a.append(users.getUser(str(i))['days_reports'])
                            a1[users.getUser(str(i))['days_reports']] = users.getUser(str(i))['id']
                    a.sort()
                    a.reverse()
                    if len(a) != 0:
                        id = a1.get(a[0])
                        api.send_user(user_id=id,
                                      text='[❤️] Вы получили похвалу от администратора за первое место в топе по отчетам за день!')
                        for i in f:
                            users.clearDayReports(str(i))
                        api.send(peer_id=peer_id,
                                 text=f'[✅] Статистика за день сброшена! Самым активным оказался {users.getName(str(id))}')
                    else:
                        api.send(peer_id=peer_id, text='[❗] Сбрасывать нечего.')

                if text == 'Сброс недельного топа':
                    f = json.loads(open(file='users.json', mode='r').read())
                    a, a1 = [], {}
                    for i in f:
                        if users.getUser(str(i))['week_reports'] != 0:
                            a.append(users.getUser(str(i))['week_reports'])
                            a1[users.getUser(str(i))['week_reports']] = users.getUser(str(i))['id']
                    a.sort()
                    a.reverse()
                    id = a1.get(a[0])
                    users.addMedals(str(id))
                    api.send_user(user_id=id,
                                  text='[🏅] Вы получили медальку за первое место в топе по отчетам за неделю!')
                    for i in f:
                        users.clearWeekReports(str(i))
                    api.send(peer_id=peer_id,
                             text=f'[✅] Статистика за неделю сброшена! Медаль вручена {users.getName(str(id))}')

                if text == 'Мой профиль':
                    norma = ""
                    if users.getRoleById(str(user_id)) == 1:
                        if users.getDayReports(str(user_id)) >= 5:
                            norma += "Дневная норма выполнена"
                        else:
                            norma += "Дневная норма не выполнена"
                    elif users.getRoleById(str(user_id)) == 2:
                        if users.getDayReports(str(user_id)) >= 7:
                            norma += "Дневная норма выполнена"
                        else:
                            norma += "Дневная норма не выполнена"
                    else:
                        norma += 'Вам не нужна дневная норма'
                    text = f"""[👤] Ваш профиль:
├ Ваш ник: {users.getName(str(user_id))} 👀
├ Ваша должность: {users.getRole(str(user_id))} 👤
├ Привилегии на грифе / выже: {users.getGroupGrief(str(user_id))} / {users.getGroupSurv(str(user_id))} 👑
├ Медалей: {users.getMedals(str(user_id))} 🏅
├ Варнов: {users.getWarns(str(user_id))}/3 ⛔
├ Баланс: {users.getBalance(str(user_id))} 💸
├ Всего отчетов: {users.getAllReports(str(user_id))} 📦
├ Отчетов за неделю: {users.getWeekReports(str(user_id))} 📥
├ Отчетов за день: {users.getDayReports(str(user_id))} ({norma}) 📩"""
                    api.send(peer_id=peer_id, text=text)

                if text == 'Топ отчетов':
                    a, a1 = [], {}
                    b, b1 = [], {}
                    c, c1 = [], {}
                    f = json.loads(open(file='users.json', mode='r').read())
                    for i in f:
                        if users.getUser(str(i))['all_reports'] != 0:
                            a.append(users.getUser(str(i))['all_reports'])
                            a1[users.getUser(str(i))['all_reports']] = users.getUser(str(i))['name']
                    a.sort()
                    a.reverse()
                    for i in f:
                        if users.getUser(str(i))['week_reports'] != 0:
                            b.append(users.getUser(str(i))['week_reports'])
                            b1[users.getUser(str(i))['week_reports']] = users.getUser(str(i))['name']
                    b.sort()
                    b.reverse()
                    for i in f:
                        if users.getUser(str(i))['days_reports'] != 0:
                            c.append(users.getUser(str(i))['days_reports'])
                            c1[users.getUser(str(i))['days_reports']] = users.getUser(str(i))['name']
                    c.sort()
                    c.reverse()
                    text = f"[🔝] Топ отчетов за все время: (Суммарно: {str(sum(a))})\n"
                    for i in a:
                        text += f'├ {a1.get(i)} - {i}\n'
                    text += f'\n[🔝] Топ за неделю: (Суммарно: {str(sum(b))})\n'
                    for i in b:
                        text += f'├ {b1.get(i)} - {i}\n'
                    text += f'\n[🔝] Топ за день: (Суммарно: {str(sum(c))})\n'
                    for i in c:
                        text += f'├ {c1.get(i)} - {i}\n'

                    api.send(peer_id=peer_id, text=text)

                if command == '/start':
                    api.send_keyboard(peer_id=peer_id, keyboard=menu().get_keyboard(), message='[✅] Отправляю меню...')

                if command == "/test":
                    pass

                if command == "/add":
                    if len(args) >= 4:
                        users.add(str(args[0]), str(args[1]), str(args[2]), str(args[3]))
                        api.send(peer_id=peer_id, text='[✅] Пользователь добавлен!')
                    else:
                        api.send(peer_id=peer_id, text='[➖] Ошибка!\n[❓] Используйте: /add user_id nickname group_grief group_surv')

                if command == '/report':
                    if len(args) >= 2 and len(event.object['message']['attachments']) != 0:
                        rand_number = random.randint(0, 999999)
                        reason = event.object['message']['text'].replace('/report', ' ').split()
                        del reason[0]
                        reason = ' '.join(reason)
                        keyboard = VkKeyboard(inline=True, one_time=False)
                        a = api.send(peer_id=peer_id, text=f'[✅] Отчет отправлен! Его уникальный айди - {rand_number}\nОжидайте...')['response']
                        keyboard.add_callback_button(label='Одобрить', color=VkKeyboardColor.POSITIVE,
                                                     payload={'hash': f'{user_id}_{peer_id}_{a}_{rand_number}_yesreport',
                                                              "type": "show_snackbar", "text": 'OK.'})
                        keyboard.add_callback_button(label='Отказать', color=VkKeyboardColor.NEGATIVE,
                                                     payload={'hash': f'{user_id}_{peer_id}_{a}_{rand_number}_noreport',
                                                              "type": "show_snackbar", "text": 'OK.'})
                        text = f'[✅] Пришел новый отчет! Его айди - {rand_number}.\n' \
                               f'[👤] Отправил: {users.getUser(str(user_id))["name"]} (@id{user_id} | {users.getRole(str(user_id))})\n' \
                               f'[🪚] Ник нарушителя: {args[0]}\n' \
                               f'[✉️] Причина нарушения: {reason}\n' \
                               f'[📷] Доказательства:'
                        attachments = event.object['message']['attachments']
                        att = []
                        for i in attachments:
                            type = i['type']
                            attach = i[type]
                            att.append(f'{type}{attach["owner_id"]}_{attach["id"]}_{attach["access_key"]}')
                        api.send_attachment(keyboard=keyboard.get_keyboard(), peer_id=getSettings().get('chat_id'), text=text, attachments=','.join(att))
                    else:
                        api.send_user(user_id=user_id, text='[❓] Используйте:\n'
                                                            '/report\n'
                                                            'Ник нарушителя\n'
                                                            'Причина нарушения\n'
                                                            'Доказательства (фото, видео)\n\n'
                                                            'ПРИМЕР(ТОЛЬКО ТАК):\n'
                                                            'JordanBreakwood\n'
                                                            '1.1, 1.2, 1.3 и т.д\n'
                                                            '*Доказательства*')

                if command == '/rcon':
                    if len(args) >= 1:
                        modes = ['grief', 'surv']
                        a = args[0]
                        if args[0] in modes:
                            del args[0]
                            b = rcon.send(mode=a, command=' '.join(args))
                            api.send(peer_id=peer_id, text=f'[✅] Ответ от сервера:\n├ {b}')
                        else:
                            api.send(peer_id=peer_id, text='[❓] Используйте: /rcon <grief или surv> command.')
            elif event.type == VkBotEventType.MESSAGE_EVENT:

                global id1
                hash = event.object['payload']['hash']
                peer_id = event.object['peer_id']
                message_id = event.object['conversation_message_id']

                if '_grief_' in hash:
                    a = hash.split('_')
                    nick = a[0]
                    user_id = a[3]
                    b = a[2]
                    if b == 'don100':
                        rcon.send(mode='grief', command=f'givedonmoney {nick} 100')
                        users.minusBalance(str(user_id), getSettings().get('shop')['donate_money_100']['price'])
                        api.send(peer_id=peer_id, text=f'[✅] 100 айронов выдано на режиме гриферство (Ник: {nick})\nБаланс: {users.getBalance(str(user_id))}💸')
                    if b == 'don200':
                        rcon.send(mode='grief', command=f'givedonmoney {nick} 200')
                        users.minusBalance(str(user_id), getSettings().get('shop')['donate_money_200']['price'])
                        api.send(peer_id=peer_id, text=f'[✅] 200 айронов выдано на режиме гриферство (Ник: {nick})\nБаланс: {users.getBalance(str(user_id))}💸')
                    if b == 'don500':
                        rcon.send(mode='grief', command=f'givedonmoney {nick} 500')
                        users.minusBalance(str(user_id), getSettings().get('shop')['donate_money_500']['price'])
                        api.send(peer_id=peer_id, text=f'[✅] 500 айронов выдано на режиме гриферство (Ник: {nick})\nБаланс: {users.getBalance(str(user_id))}💸')
                    if b == 'case':
                        rcon.send(mode='grief', command=f'drc add {nick} 1')
                        users.minusBalance(str(user_id), getSettings().get('shop')['case']['price'])
                        api.send(peer_id=peer_id, text=f'[✅] Дроп-кейс выдан на режим гриферство (Ник: {nick})\nБаланс: {users.getBalance(str(user_id))}💸')

                if '_surv_' in hash:
                    a = hash.split('_')
                    nick = a[0]
                    user_id = a[3]
                    b = a[2]
                    if b == 'don100':
                        rcon.send(mode='surv', command=f'givedonmoney {nick} 100')
                        users.minusBalance(str(user_id), getSettings().get('shop')['donate_money_100']['price'])
                        api.send(peer_id=peer_id, text=f'[✅] 100 айронов выдано на режиме выживание (Ник: {nick})\nБаланс: {users.getBalance(str(user_id))}💸')
                    if b == 'don200':
                        rcon.send(mode='surv', command=f'givedonmoney {nick} 200')
                        users.minusBalance(str(user_id), getSettings().get('shop')['donate_money_200']['price'])
                        api.send(peer_id=peer_id, text=f'[✅] 200 айронов выдано на режиме выживание (Ник: {nick})\nБаланс: {users.getBalance(str(user_id))}💸')
                    if b == 'don500':
                        rcon.send(mode='surv', command=f'givedonmoney {nick} 500')
                        users.minusBalance(str(user_id), getSettings().get('shop')['donate_money_500']['price'])
                        api.send(peer_id=peer_id, text=f'[✅] 500 айронов выдано на режиме выживание (Ник: {nick})\nБаланс: {users.getBalance(str(user_id))}💸')
                    if b == 'case':
                        rcon.send(mode='surv', command=f'drc add {nick} 1')
                        users.minusBalance(str(user_id), getSettings().get('shop')['case']['price'])
                        api.send(peer_id=peer_id, text=f'[✅] Дроп-кейс выдан на режим выживание (Ник: {nick})\nБаланс: {users.getBalance(str(user_id))}💸')

                if 'case' in hash:
                    a = hash.split('_')
                    user_id = a[0]
                    if users.getBalance(str(user_id)) >= getSettings().get('shop')['case']['price']:
                        keyboard = VkKeyboard(inline=True, one_time=False)
                        keyboard.add_callback_button(label='Гриферство', color=VkKeyboardColor.NEGATIVE, payload={
                            'hash': f'{users.getName(str(user_id))}_grief_case_{user_id}', "type": "show_snackbar",
                            "text": 'OK.'})
                        keyboard.add_callback_button(label='Выживание', color=VkKeyboardColor.POSITIVE, payload={
                            'hash': f'{users.getName(str(user_id))}_surv_case_{user_id}', "type": "show_snackbar",
                            "text": 'OK.'})
                        api.send_keyboard(peer_id=peer_id, message='[✅] Выберите режим:',
                                          keyboard=keyboard.get_keyboard())
                    else:
                        api.send(peer_id=peer_id, text='[➖] У вас не хватает денег!')

                if 'otpusk3' in hash:
                    a = hash.split('_')
                    user_id = a[0]
                    if users.getBalance(str(user_id)) >= getSettings().get('shop')['otpusk_3_days']['price']:
                        users.minusBalance(str(user_id), getSettings().get('shop')['otpusk_3_days']['price'])
                        api.send(peer_id=peer_id, text=f'[✅] Вы купили отпуск на 3 дня\nБаланс: {users.getBalance(str(user_id))}💸')
                        for i in getSettings().get('admins'):
                            api.send(peer_id=i, text=f'[ℹ️] {users.getName(str(user_id))} купил отпуск на 3 дня.')
                    else:
                        api.send(peer_id=peer_id, text='[➖] У вас не хватает денег!')

                if 'otpusk5' in hash:
                    a = hash.split('_')
                    user_id = a[0]
                    if users.getBalance(str(user_id)) >= getSettings().get('shop')['otpusk_5_days']['price']:
                        users.minusBalance(str(user_id), getSettings().get('shop')['otpusk_5_days']['price'])
                        api.send(peer_id=peer_id, text=f'[✅] Вы купили отпуск на 5 дней\nБаланс: {users.getBalance(str(user_id))}💸')
                        for i in getSettings().get('admins'):
                            api.send(peer_id=i, text=f'[ℹ️] {users.getName(str(user_id))} купил отпуск на 5 дней.')
                    else:
                        api.send(peer_id=peer_id, text='[➖] У вас не хватает денег!')

                if 'otpusk7' in hash:
                    a = hash.split('_')
                    user_id = a[0]
                    if users.getBalance(str(user_id)) >= getSettings().get('shop')['otpusk_7_days']['price']:
                        users.minusBalance(str(user_id), getSettings().get('shop')['otpusk_7_days']['price'])
                        api.send(peer_id=peer_id, text=f'[✅] Вы купили отпуск на 7 дней\nБаланс: {users.getBalance(str(user_id))}💸')
                        for i in getSettings().get('admins'):
                            api.send(peer_id=i, text=f'[ℹ️] {users.getName(str(user_id))} купил отпуск на 7 дней.')
                    else:
                        api.send(peer_id=peer_id, text='[➖] У вас не хватает денег!')

                if '_100donmoney' in hash:
                    a = hash.split('_')
                    user_id = a[0]
                    if users.getBalance(str(user_id)) >= getSettings().get('shop')['donate_money_100']['price']:
                        keyboard = VkKeyboard(inline=True, one_time=False)
                        keyboard.add_callback_button(label='Гриферство', color=VkKeyboardColor.NEGATIVE, payload={'hash': f'{users.getName(str(user_id))}_grief_don100_{user_id}', "type": "show_snackbar", "text": 'OK.'})
                        keyboard.add_callback_button(label='Выживание', color=VkKeyboardColor.POSITIVE, payload={'hash': f'{users.getName(str(user_id))}_surv_don100_{user_id}', "type": "show_snackbar", "text": 'OK.'})
                        api.send_keyboard(peer_id=peer_id, message='[✅] Выберите режим:', keyboard=keyboard.get_keyboard())
                    else:
                        api.send(peer_id=peer_id, text='[➖] У вас не хватает денег!')

                if '_200donmoney' in hash:
                    a = hash.split('_')
                    user_id = a[0]
                    if users.getBalance(str(user_id)) >= getSettings().get('shop')['donate_money_200']['price']:
                        keyboard = VkKeyboard(inline=True, one_time=False)
                        keyboard.add_callback_button(label='Гриферство', color=VkKeyboardColor.NEGATIVE, payload={'hash': f'{users.getName(str(user_id))}_grief_don200_{user_id}', "type": "show_snackbar", "text": 'OK.'})
                        keyboard.add_callback_button(label='Выживание', color=VkKeyboardColor.POSITIVE, payload={'hash': f'{users.getName(str(user_id))}_surv_don200_{user_id}', "type": "show_snackbar", "text": 'OK.'})
                        api.send_keyboard(peer_id=peer_id, message='[✅] Выберите режим:', keyboard=keyboard.get_keyboard())
                    else:
                        api.send(peer_id=peer_id, text='[➖] У вас не хватает денег!')

                if '_500donmoney' in hash:
                    a = hash.split('_')
                    user_id = a[0]
                    if users.getBalance(str(user_id)) >= getSettings().get('shop')['donate_money_500']['price']:
                        keyboard = VkKeyboard(inline=True, one_time=False)
                        keyboard.add_callback_button(label='Гриферство', color=VkKeyboardColor.NEGATIVE, payload={'hash': f'{users.getName(str(user_id))}_grief_don500_{user_id}', "type": "show_snackbar", "text": 'OK.'})
                        keyboard.add_callback_button(label='Выживание', color=VkKeyboardColor.POSITIVE, payload={'hash': f'{users.getName(str(user_id))}_surv_don500_{user_id}', "type": "show_snackbar", "text": 'OK.'})
                        api.send_keyboard(peer_id=peer_id, message='[✅] Выберите режим:', keyboard=keyboard.get_keyboard())
                    else:
                        api.send(peer_id=peer_id, text='[➖] У вас не хватает денег!')

                if "_yesreport" in hash:
                    a = hash.split('_')
                    user_id = a[0]
                    peer_id = a[1]
                    message_id = a[2]
                    api.reply_to(peer_id=peer_id, message_id=message_id, photos=getSettings().get('photos')['report_yes'])
                    users.addReport(user_id=str(user_id))

                if "_noreport" in hash:
                    a = hash.split('_')
                    peer_id = a[1]
                    message_id = a[2]
                    api.reply_to(peer_id=peer_id, message_id=message_id, photos=getSettings().get('photos')['report_no'])

                if "_balanceminus" in hash:
                    id2 = str(hash.split('_')[0])
                    users.setBalance(id2)
                    api.send(peer_id=peer_id, text='[✅] Баланс пользователя обнулён!')
                    api.send(peer_id=id2, text=f'[✅] Админстратор обнулил ваш баланс!')

                if '_give_' in hash:
                    id2 = str(hash.split('_')[0])
                    count = int(hash.split('_')[2])
                    users.addBalance(id2, count)
                    api.send(peer_id=peer_id, text=f'[✅] Баланс выдан пользователю! Теперь его баланс {users.getBalance(id2)}💸')
                    api.send(peer_id=id2, text=f'[✅] Администратор выдал вам {count}💸')

                if '_minus_' in hash:
                    id2 = str(hash.split('_')[0])
                    count = int(hash.split('_')[2])
                    if users.getBalance(id2) >= count:
                        users.minusBalance(id2, count)
                        api.send(peer_id=peer_id, text=f'[✅] Баланс снят пользователю! Теперь его баланс {users.getBalance(id2)}💸')
                        api.send(peer_id=id2, text=f'[✅] Администратор снял у вас {count}💸')
                    else:
                        api.send(peer_id=peer_id, text=f'[✅] Снимать нечего!')

                if "_balancevichet" in hash:
                    keyboard = VkKeyboard(inline=True, one_time=False)
                    keyboard.add_callback_button(label='10', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_minus_10', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_callback_button(label='20', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_minus_20', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_callback_button(label='30', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_minus_30', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_callback_button(label='40', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_minus_40', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_callback_button(label='50', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_minus_50', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_line()
                    keyboard.add_callback_button(label='60', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_minus_60', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_callback_button(label='70', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_minus_70', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_callback_button(label='80', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_minus_80', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_callback_button(label='90', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_minus_90', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_callback_button(label='100', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_minus_100', "type": "show_snackbar", "text": 'OK.'})
                    api.send_keyboard(peer_id=peer_id, keyboard=keyboard.get_keyboard(), message='[✅] Сколько?')

                if "_givebalance" in hash:
                    keyboard = VkKeyboard(inline=True, one_time=False)
                    keyboard.add_callback_button(label='10', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_give_10', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_callback_button(label='20', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_give_20', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_callback_button(label='30', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_give_30', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_callback_button(label='40', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_give_40', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_callback_button(label='50', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_give_50', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_line()
                    keyboard.add_callback_button(label='60', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_give_60', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_callback_button(label='70', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_give_70', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_callback_button(label='80', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_give_80', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_callback_button(label='90', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_give_90', "type": "show_snackbar", "text": 'OK.'})
                    keyboard.add_callback_button(label='100', color=VkKeyboardColor.PRIMARY, payload={'hash': f'{str(id1)}_give_100', "type": "show_snackbar", "text": 'OK.'})
                    api.send_keyboard(peer_id=peer_id, keyboard=keyboard.get_keyboard(), message='[✅] Сколько?')

                if '_kick' in hash:
                    id2 = str(hash.split('_')[0])
                    rcon.send(mode='grief', command=f'takeoff {users.getName(id2)}')
                    rcon.send(mode='grief', command=f'setgroup {users.getName(id2)} {users.getGroupGrief(id2)}')
                    rcon.send(mode='surv', command=f'takeoff {users.getName(id2)}')
                    rcon.send(mode='surv', command=f'setgroup {users.getName(id2)} {users.getGroupSurv(id2)}')
                    users.kick(id2)
                    api.send(peer_id=peer_id, text='[✅] Пользователь уволен!')
                    api.block_user(user_id=id2, group_id=getSettings().get('group_id'))

                if '_role2' in hash:
                    id2 = str(hash.split('_')[0])
                    if users.getRoleById(id2) > 1:
                        users.setRole(id2, users.getRoleById(id2)-1)
                        api.send(peer_id=peer_id,
                                 text='[✅] Должность понижена!\n'
                                      f'[ℹ️] Теперь у {users.getName(id2)} должность {users.getRole(id2)}.')
                        api.send_user(user_id=id2,
                                      text=f'[ℹ️] Вы понижены! Теперь ваша должность {users.getRole(id2)}')
                    else:
                        api.send(peer_id=peer_id,
                                 text='[❗] У пользователя минимальная должность!')

                if '_role1' in hash:
                    id2 = str(hash.split('_')[0])
                    if users.getRoleById(id2) < 5:
                        users.setRole(id2, users.getRoleById(id2)+1)

                        api.send(peer_id=peer_id,
                                 text='[✅] Должность повышена!\n'
                                      f'[ℹ️] Теперь у {users.getName(id2)} должность {users.getRole(id2)}.')
                        api.send_user(user_id=id2,
                                      text=f'[ℹ️] Вы повышены! Теперь ваша должность {users.getRole(id2)}')
                    else:
                        api.send(peer_id=peer_id,
                                 text='[❗] У пользователя максимальная должность!')

                if '_unwarn' in hash:
                    id2 = str(hash.split("_")[0])
                    if users.getWarns(id2) > 0:
                        users.unwarn(id2)
                        api.send(peer_id=peer_id, text='[✅] С пользователя снят варн!')
                        api.send_user(user_id=id2,
                                      text=f'[✅] С вас снят варн!\n[❓] Количество ваших варнов: {users.getWarns(id2)}/3.')
                    else:
                        api.send(peer_id=peer_id, text='[✅] У пользователя нет варнов!')

                if '_addwarn' in hash:
                    id2 = str(hash.split("_")[0])
                    if users.getWarns(id2) == 2:
                        users.kick(id2)
                        api.send(peer_id=peer_id, text='[✅] У пользователя 3/3 варнов, увольняю...')
                        api.send_user(user_id=id2, text='[✅] Вам выдан варн!\n[❓] Количество ваших варнов: '
                                                        '3/3.\n[❗] Вы уволены!')
                        api.block_user(user_id=id2, group_id=getSettings().get('group_id'))
                    else:
                        users.warn(id2)
                        api.send(peer_id=peer_id, text='[✅] Пользователю выдан варн!')
                        api.send_user(user_id=id2,
                                      text=f'[✅] Вам выдан варн!\n[❓] Количество ваших варнов: {users.getWarns(id2)}/3.')

                if '_profile' in hash:
                    nick = hash.split('_')[0]
                    f = json.loads(open(file='users.json', mode='r').read())
                    id1 = None
                    for i in f:
                        if users.getName(str(i)) == nick:
                            id1 = i
                    norma = ""
                    if users.getRoleById(str(id1)) == 1:
                        if users.getDayReports(str(id1)) >= 5:
                            norma += "Дневная норма выполнена"
                        else:
                            norma += "Дневная норма не выполнена"
                    elif users.getRoleById(str(id1)) == 2:
                        if users.getDayReports(str(id1)) >= 7:
                            norma += "Дневная норма выполнена"
                        else:
                            norma += "Дневная норма не выполнена"
                    else:
                        norma += 'Не нужна дневная норма'
                    text = f"""[👤] Профиль:
├ Ник: {users.getName(str(id1))} 👀
├ Должность: {users.getRole(str(id1))} 👤
├ Привилегии на грифе / выже: {users.getGroupGrief(str(id1))} / {users.getGroupSurv(str(id1))} 👑
├ Медалей: {users.getMedals(str(id1))} 🏅
├ Варнов: {users.getWarns(str(id1))}/3 ⛔
├ Баланс: {users.getBalance(str(id1))} 💸
├ Всего отчетов: {users.getAllReports(str(id1))} 📦
├ Отчетов за неделю: {users.getWeekReports(str(id1))} 📥
├ Отчетов за день: {users.getDayReports(str(id1))} ({norma}) 📩"""
                    keyboard = VkKeyboard(inline=True, one_time=False)
                    keyboard.add_callback_button(label='Дать варн', color=VkKeyboardColor.NEGATIVE,
                                                 payload={'hash': f'{str(id1)}_addwarn', "type": "show_snackbar",
                                                          "text": 'OK.'})
                    keyboard.add_callback_button(label='Снять варн', color=VkKeyboardColor.POSITIVE,
                                                 payload={'hash': f'{str(id1)}_unwarn', "type": "show_snackbar",
                                                          "text": 'OK.'})
                    keyboard.add_line()
                    keyboard.add_callback_button(label='Повысить', color=VkKeyboardColor.POSITIVE,
                                                 payload={'hash': f'{str(id1)}_role1', "type": "show_snackbar",
                                                          "text": 'OK.'})
                    keyboard.add_callback_button(label='Понизить', color=VkKeyboardColor.NEGATIVE,
                                                 payload={'hash': f'{str(id1)}_role2', "type": "show_snackbar",
                                                          "text": 'OK.'})
                    keyboard.add_line()
                    keyboard.add_callback_button(label='Уволить', color=VkKeyboardColor.NEGATIVE,
                                                 payload={'hash': f'{str(id1)}_kick', "type": "show_snackbar",
                                                          "text": 'OK.'})
                    keyboard.add_line()
                    keyboard.add_callback_button(label='Выдать баланс', color=VkKeyboardColor.POSITIVE,
                                                 payload={'hash': f'{str(id1)}_givebalance', "type": "show_snackbar",
                                                          "text": 'OK.'})
                    keyboard.add_callback_button(label='Обнулить баланс', color=VkKeyboardColor.SECONDARY,
                                                 payload={'hash': f'{str(id1)}_balanceminus', "type": "show_snackbar",
                                                          "text": 'OK.'})
                    keyboard.add_callback_button(label='Снять баланс', color=VkKeyboardColor.NEGATIVE,
                                                 payload={'hash': f'{str(id1)}_balancevichet', "type": "show_snackbar",
                                                          "text": 'OK.'})
                    api.send_keyboard(peer_id=peer_id, message=text, keyboard=keyboard.get_keyboard())

    except Exception as e:
        bot()


if __name__ == "__main__":
    bot()
