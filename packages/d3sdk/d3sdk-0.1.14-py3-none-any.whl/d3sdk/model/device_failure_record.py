from typing import List

class Fm:
    def __init__(self, fm_code, fm_name, fmt_code, fmt_name, fmt_type):
        self.fm_code = fm_code
        self.fm_name = fm_name
        self.fmt_code = fmt_code
        self.fmt_name = fmt_name
        self.fmt_type = fmt_type

    def __repr__(self):
        return f"Fm(fm_code={self.fm_code}, fm_name={self.fm_name}, fmt_code={self.fmt_code}, fmt_name={self.fmt_name}, fmt_type={self.fmt_type})"

class DeviceFailureRecord:
    def __init__(self, alarmGroupCode, alarmGroupName, alarmType, alarmCode, description, alarmNumber, level, status, keywords, earliestAlarmTime, latestAlarmTime, deviceCode, fms:List[Fm]):
        self.alarmGroupCode = alarmGroupCode
        self.alarmGroupName = alarmGroupName
        self.alarmType = alarmType
        self.alarmCode = alarmCode
        self.description = description
        self.alarmNumber = alarmNumber
        self.level = level
        self.status = status
        self.keywords = keywords
        self.earliestAlarmTime = earliestAlarmTime
        self.latestAlarmTime = latestAlarmTime
        self.deviceCode = deviceCode
        self.fms = fms

    def __repr__(self):
        return (f"DeviceFailureRecord(dfem_code={self.dfem_code}, "
                f"display_name={self.display_name}, "
                f"dfem_bjlx={self.dfem_bjlx}, "
                f"dfem_sxmsbh={self.dfem_sxmsbh}, "
                f"description={self.description}, "
                f"dfem_bjs={self.dfem_bjs}, "
                f"dfem_bjdj={self.dfem_bjdj}, "
                f"dfem_zt={self.dfem_zt}, "
                f"dfem_gjz={self.dfem_gjz}, "
                f"dfem_zzbjsj={self.dfem_zzbjsj}, "
                f"dfem_zxbjsj={self.dfem_zxbjsj}, "
                f"device_code={self.device_code}, "
                f"fms={self.fms!r})")


    # @staticmethod
    # def from_row(row):
    #     return DeviceFailureRecord(
    #         dfem_code=row['dfem_code'],
    #         display_name=row['display_name'],
    #         dfem_bjlx=row['dfem_bjlx'],
    #         dfem_sxmsbh=row['dfem_sxmsbh'],
    #         description=row['description'],
    #         dfem_bjs=row['dfem_bjs'],
    #         dfem_bjdj=row['dfem_bjdj'],
    #         dfem_zt=row['dfem_zt'],
    #         dfem_gjz=row['dfem_gjz'],
    #         dfem_zzbjsj=row['dfem_zzbjsj'],
    #         dfem_zxbjsj=row['dfem_zxbjsj'],
    #         device_code=row['device_code'],
    #         fm_code=row['fm_code'],
    #         fm_name=row['fm_name']
    #     )


# # 创建示例对象
# record1 = DeviceFailureRecord(
#     "AG0000121409",
#     "12号定子线棒层间温度运行值持续动态超限",
#     "failure",
#     "FM800412",
#     "12号定子线棒层间温度运行值持续动态超限",
#     4,
#     "注意",
#     "已查看",
#     "定子绕组温度，动态预警",
#     "2024-06-30 12:56:48",
#     "2024-06-30 13:59:48",
#     "T0000000002",
#     "QLJ00001",
#     "定子"
# )
#
# # 打印对象
# print(record1)