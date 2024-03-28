from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_keyboard(
        buttons: list[str],
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int] = (2,)):
    """
    Parameters request_contact and request_location must be as indexes of btns args for buttons you need.
    Example:
    get_keyboard(
        buttons=["Меню", "О магазине", "Варианты оплаты", "Варианты доставки", "Отправить номер телефона"],
        placeholder="Что вас интересует?",
        request_contact=4,
        sizes=(2, 2, 1)
        )
    """
    def validate_args():
        logs = []
        if sum(sizes) != len(buttons):
            logs.append('| sizes - Компоновка кнопок не соотвествует их количеству')
        if request_contact >= len(buttons):
           logs.append('| request_contact - Индекс Контактной Кнопки за границей списка Кнопок.')
        if request_location >= len(buttons):
            logs.append('| request_location - Индекс Локационной Кнопки за границей списка Кнопок.')
        if request_contact == request_location:
            logs.append('| request_contact == request_location - На одну кнопку нельзя одновременно задать запрос на Локацию и Контакт.')
        if logs:
            raise(' | '.join(logs))

    validate_args()
    keyboard = ReplyKeyboardBuilder()
    for button in buttons:
        need_contact, need_location = False, False
        if request_contact and request_contact == buttons.index(button):
            need_contact = True
        if request_location and request_location == buttons.index(button):
            need_location = True
        keyboard.add(KeyboardButton(text=button,
                                    request_contact=need_contact,
                                    request_location=need_location))
        return keyboard.adjust(*sizes).as_markup(resize_keyboard=True, input_field_placeholder=placeholder)


if __name__ == '__main__':
    buttons = ["Меню", "О магазине", "Варианты оплаты", "Варианты доставки", "Отправить номер телефона"]
    print(buttons.index("О магазине"))
