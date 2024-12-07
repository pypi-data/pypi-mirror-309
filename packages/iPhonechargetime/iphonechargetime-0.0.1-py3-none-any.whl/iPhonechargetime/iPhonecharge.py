# iPhonebattery.py
import json

# iPhone 15～16シリーズのバッテリー情報
battery_data = {
    "iPhone15": {
        "battery_capacity": 3349,  # mAh
        "default_voltage": 9  # V
    },
    "iPhone15Plus": {
        "battery_capacity": 4383,
        "default_voltage": 9
    },
    "iPhone15Pro": {
        "battery_capacity": 3274,
        "default_voltage": 9
    },
        "iPhone15ProMax": {
        "battery_capacity": 4422,
        "default_voltage": 9
    },
        "iPhone16ProMax": {
        "battery_capacity": 4685,
        "default_voltage": 9
    },
    "iPhone16": {
        "battery_capacity": 3561,  # mAh
        "default_voltage": 9  # V
    },
    "iPhone16Plus": {
        "battery_capacity": 4383,  # mAh
        "default_voltage": 9  # V
    },
    "iPhone16Pro": {
        "battery_capacity": 4200,  # mAh
        "default_voltage": 9  # V
    }
}

# iPhoneの充電速度計算
def iPhonebattery(model, charge_percentage, W=20, V=None):
    if model not in battery_data:
        raise ValueError("Unknown model: {}".format(model))

    # モデルのバッテリー容量（mAh）を取得
    battery_capacity = battery_data[model]["battery_capacity"]

    # 充電電圧（V）を指定されていない場合、デフォルトを使用
    voltage = V if V is not None else battery_data[model]["default_voltage"]

    # 充電電流の計算（A）
    current = W / voltage  # I = P / V
    current_mAh = current * 1000  # mAに変換

    # 1秒あたりの充電量
    charge_rate_per_second = current_mAh / battery_capacity * 100  # %

    # 充電の開始と終了のパーセンテージ
    start_percentage = charge_percentage
    end_percentage = 100

    # 充電にかかる秒数の計算
    time_to_charge = (end_percentage - start_percentage) / charge_rate_per_second  # 秒

    # 結果を返す
    return time_to_charge
