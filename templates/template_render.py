from string import Template


class EmailTemplates():

    @staticmethod
    def send_reminder_overdue():
        mssg = Template('$name, You have borrowed $title and return date passed $return_at\n Please return it imidietly\nBest Regards\nPawel')
        return mssg

    @staticmethod
    def send_reminder_nearby():
        mssg = Template('$name, You have borrowed $title and the return day is $return_at. Its about @result days from today.Please try not to overdue this dateBest Regards'
                        'Pawel')
        return mssg