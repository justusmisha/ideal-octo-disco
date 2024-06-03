from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


### FIRST MESSAGE KEYBOARD
kb_first_message = InlineKeyboardMarkup(resize_keyboard=True)
kb_first_message.add(InlineKeyboardButton("Начать", callback_data='option_srub'))


### SRUB KEYBOARD
srub_keyboard = InlineKeyboardMarkup(row_width=1)
srub_keyboard.add(InlineKeyboardButton(text="Длинна стены A", callback_data="srub_option_wall_a"),
                  InlineKeyboardButton(text="Длинна стены B", callback_data="srub_option_wall_b"),
                  InlineKeyboardButton(text="Высота сруба", callback_data="srub_option_height"),
                  InlineKeyboardButton(text="Диаметр бревен", callback_data="srub_option_diameter"),
                  InlineKeyboardButton(text="5 стена", callback_data="srub_option_extra_wall"), )

diameter_kb = InlineKeyboardMarkup(row_width=2)
diameter_kb.add(InlineKeyboardButton(text="18-22 см", callback_data="srub_option_diameter_20"),
                InlineKeyboardButton(text="20-24 см", callback_data="srub_option_diameter_22"))


### TRUE FALSE KEYBOARD
true_false_kb = InlineKeyboardMarkup(row_width=2)
true_false_kb.add(InlineKeyboardButton(text="Да", callback_data="srub_option_extra_wall_True"),
                  InlineKeyboardButton(text="Нет", callback_data="srub_option_extra_wall_False"))


### FUNDAMENT KEYBOARD
fundament_kb = InlineKeyboardMarkup(row_width=1)
fundament_kb.add(InlineKeyboardButton(text="Ленточный Фундамент", callback_data="option_fundament_lent"),
                 InlineKeyboardButton(text="Сваи Забивные", callback_data="option_fundament_zabiv"),
                 InlineKeyboardButton(text="Сваи Винтовые", callback_data="option_fundament_vint"),
                 InlineKeyboardButton(text="Назад", callback_data="option_fundament_back"))


### FINALL KEYBOARD
final_kb = InlineKeyboardMarkup(row_width=1)
final_kb.add(InlineKeyboardButton(text="Рассчитать стоимость без модификаторов", callback_data="final_price_wo_mod"),
             InlineKeyboardButton(text="Добавить стоимость крыши", callback_data='add_roof_price'),
             InlineKeyboardButton(text="Добавить стоимость фундамента", callback_data='add_fund_price'),
             InlineKeyboardButton(text="Рассчитать стоимость с модификаторами", callback_data='final_srub_price'),
             InlineKeyboardButton(text="Назад", callback_data="add_back")
             )
