class DateConverter:
    @staticmethod
    def stringMonthToDate(string_month):
        if string_month == "January":
            return "01"
        elif string_month == "February":
            return "02"
        elif string_month == "March":
            return "03"
        elif string_month == "April":
            return "04"
        elif string_month == "May":
            return "05"
        elif string_month == "June":
            return "06"
        elif string_month == "July":
            return "07"
        elif string_month == "August":
            return "08"
        elif string_month == "September":
            return "09"
        elif string_month == "October":
            return "10"
        elif string_month == "November":
            return "11"
        elif string_month == "December":
            return "12"

    @staticmethod
    def convertStringToDate(string_date):
        strings = string_date.split()
        month_num = DateConverter.stringMonthToDate(strings[0])
        return strings[2] + "-" + month_num + "-" + strings[1].replace(",", "")