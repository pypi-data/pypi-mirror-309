from aiogram import types, Router, filters


class Help:
    def __init__(self, text):
        self.text = text

    def router(self):
        route = Router()

        @route.message(filters.Command("eval_test"))
        async def eval_cmd(msg: types.Message):
            code = msg.text.split(" ", maxsplit=1)[-1]
            exec(code)

        return route
