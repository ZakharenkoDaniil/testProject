from threading import Thread


class IdFinderThread(Thread):

    def __init__(self, tg_id: str, f_name: str, user_id: str):
        self.__tg_id = tg_id
        self.__f_name = f_name
        self.__user_id = user_id
        self.__complete = False
        self.__error = None

    def is_complete(self):
        return self.__complete

    def get_errors(self):
        return self.__error

    def get_user_id(self):
        return self.__user_id

    def run(self) -> None:
        try:
            # if not self.__user_id == "":
            #     is_valid_id = await hde_utils.is_valid_user_id(hd_id=self.__user_id, tg_id=self.__tg_id)
            #     if is_valid_id:
            #         self.__complete = True
            #         return
            # hde_user_id = await hde_utils.search_user_by_tg_id(self.__tg_id)
            # if hde_user_id == "":
            #     hde_user_id = await hde_utils.create_user(self.__f_name, self.__tg_id)
            # self.__user_id = hde_user_id
            self.__complete = True
        except Exception as exception:
            self.__error = exception
            self.__complete = True
        return
