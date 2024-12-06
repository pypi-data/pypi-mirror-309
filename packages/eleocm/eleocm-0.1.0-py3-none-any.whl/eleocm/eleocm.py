
import numpy as np
from scipy.interpolate import UnivariateSpline

def eleocm(speed ,wind_speed ,swh):
    """读取数据"""
    v = speed
    v_a = wind_speed
    h_a = swh
    U = v * 1.852 / 3.6  # m/s
    Cb = 0.5691  # 方形系数
    Cw = 0.8455  # 水线面系数
    Cp = 0.6180  # 菱形系数
    v_v = 1.18831 * 1e-6  # 海水运动粘度系数 (m²/s)
    L_oa = 69.83  # 船长 (m)
    L_w = 69.60  # 水线长 (m)
    L_b = 66.42  # 船舶垂线间长 (m)
    Lcb = 0.03 * L_oa * (Cp + 0.675) ** (1 / 3)
    B = 10.90  # 船宽 (m)
    d = 3.5  # 吃水 (m)
    g = 9.8  # 重力加速度 (m/s²)
    Vpai = 1457.6  # 排水体积 (m³)
    p = 1025.91  # 海水密度 (kg/m³)
    P_1 = 1.226  # 空气密度 (kg/m³)
    Re = (v * 1.852 / 3.6) * L_w / v_v  # 雷诺数
    Cm = 0.9209  # 中横剖面系数
    Vxingpai = 1442.3
    Fn = U / np.sqrt(9.8 * L_w)  # 傅汝德数
    ks = 1.3e-4  # 粗糙度表现高度

    """摩擦阻力"""
    Cf = 0.075 / ((np.log10(Re) - 2) ** 2)  # 摩擦阻力系数
    Ce = (105 * (ks / L_b) ** (1 / 3) - 0.64) * 1e-3  # 粗糙度补贴系数
    s = 966.7  # 湿面积 (满载)
    k = 1  # 1+k
    L_R = L_w * (1 - Cp + (0.06 * Cp * Lcb) / (4 * Cp - 1))  # 船舶去流段长度
    Rf = 0.5 * Cf * p * U ** 2 * s  # 摩擦阻力

    """兴波阻力"""
    A_BT = 8.6569  # 球鼻艏横剖面面积
    H_b = 1.5  # 球鼻艏高度
    T_f = 3.5  # 艏吃水
    C3 = 0.56 * A_BT ** 1.5 / (B * d * (0.31 * np.sqrt(A_BT) + T_f - H_b))
    C2 = np.exp(-1.89 * np.sqrt(C3))
    C7 = B / L_w
    At = 1.65
    C5 = 1 - 0.8 * At / (B * d * Cm)
    C16 = 8.08 * Cp - 13.867 * Cp ** 2 + 6.984 * Cp ** 3
    C15 = -1.69385
    m1 = 0.014 * L_w / d - 1.75 * Vxingpai ** (1 / 3) / L_w - 4.79 * B / L_w - C16
    m2 = C15 * Cp ** 2 * np.exp(-0.1 * Fn ** (1.4))
    Lan = 1.446 * Cp - 0.03 * L_w / B
    iE = 1 + 89 * np.exp(
        -(L_w / B) ** 0.80856 * (1 - Cw) ** 0.30484 * (1 - Cp - 0.0225 * Lcb) ** 0.6367 * (L_R / B) ** 0.34574 * (
                100 * Vxingpai / L_w ** 3) ** 0.16302)
    C1 = 2223105 * C7 ** 3.78613 * (d / B) ** 1.07961 * (90 - iE) ** (-1.37565)
    Rw = C1 * C2 * C5 * Vxingpai * p * g * np.exp(m1 * Fn ** (-0.86) + m2 * np.cos(Lan * Fn ** (-1.9)))

    """附体阻力"""
    Sapp = 32  # 船舶附体的湿面积
    k1 = 1.4
    Rapp = 0.5 * p * Sapp * U ** 2 * k1 * Cf  # 附体阻力

    """球鼻艏附加阻力"""
    Fri = U / np.sqrt(0.15 * U ** 2 + g * (T_f - 0.25 * np.sqrt(A_BT) - H_b))
    P_b = 0.56 * np.sqrt(A_BT) * (T_f - 1.5 * H_b)
    Rb = 0.11 * p * g * Fri ** 3 * A_BT ** 1.5 * np.exp(-3 * P_b ** (-2)) / (1 + Fri ** 2)

    # 艉浸没附加阻力
    # Frd = U / np.sqrt(2 * g * At / (B + B * Cw))
    # C6 = 0.2 * (1 - 0.2 * Frd)
    # if Frd < 5 else 0

    """模型实船换算相关阻力"""
    Tf = 3.5  # 船艏吃水
    C4 = 0.04
    Ca = 0.006 * (L_w + 100) ** (-0.16) - 0.00205 + 0.003 * np.sqrt(L_w / 7.5) * Cb ** 4 * C2 * (0.04 - C4)
    Ra = 0.5 * p * U ** 2 * s * Ca

    """静水阻力"""
    Rt = Rf * k + Rw + Rapp + Ra + Rb  # 静水阻力
    Rt1 = Rt / 1000  # kN

    """空气阻力"""
    A_t = 126  # 船体水线以上部分在横剖面方向的投影面积
    Caa = 0.13 * 1e-3  # 空气阻力系数
    v_a1 = U + v_a  # 空气对船的相对速度
    Raa = 0.5 * Caa * P_1 * A_t * (v_a1 ** 2)  # 空气阻力
    Raa1 = Raa / 1000
    """波浪增阻"""
    Raw = (0.64 * (h_a ** 2) * (B ** 2) * Cb * p * g) / L_oa  # 波浪增阻
    Raw1 = Raw / 1000

    """总阻力"""
    R = Rt + Raa + Raw  # 总阻力
    R1 = R / 1000  # kN

    """推力减额与伴流分数"""
    w = (0.06684 - 0.02079 * np.cos(1.018 * U) +
         0.03277 * np.sin(1.018 * U) +
         0.01869 * np.cos(2 * 1.018 * U) +
         0.0253 * np.sin(2 * 1.018 * U) +
         0.007116 * np.cos(3 * 1.018 * U) +
         0.001222 * np.sin(3 * 1.018 * U))
    t = (0.1178 + 0.01474 * np.cos(1.527 * U) +
         0.004315 * np.sin(1.527 * U) -
         0.004767 * np.cos(2 * 1.527 * U) +
         0.001869 * np.sin(2 * 1.527 * U) -
         0.002107 * np.cos(3 * 1.527 * U) +
         0.001718 * np.sin(3 * 1.527 * U))

    """效率"""
    j = np.array([0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8])  # 船模试验螺旋桨进速系数 j
    fzqx = np.array \
        ([4.315605008, 3.451665502, 2.820872806, 2.316132906, 1.889249091, 1.514005725 ,1.174121659, 0.858364965,
                     0.558128969, 0.266049772, -0.025112701, -0.323516525, -0.639796005, -0.990206415, -1.404458332]) # 船模试验 ln(kt/j^2)
    sorted_indices = np.argsort(fzqx)
    fzqx_sorted = fzqx[sorted_indices]
    j_sorted = j[sorted_indices]

    """使用平滑样条拟合，平滑参数设为 0.9946572453860684"""
    smoothing_param1 = 0.9946572453860684  # 你之前定义的平滑参数
    cstx1 = UnivariateSpline(fzqx_sorted, j_sorted, s=smoothing_param1, ext=3)  # ext=3 允许外推
    D = 1.8  # 螺旋桨直径
    xxx = Rt / (p * ((1 - w) ** 2) * (1 - t) * U ** 2 * D ** 2)  # kT/j^2
    T_j = np.log(xxx)  # ln(kt/j^2)
    J = cstx1(T_j)  # 进速系数 J
    n = np.array([6.1010, 6.2820, 6.4650, 6.6620, 6.8830, 7.1390, 7.4400, 7.7990, 8.2290]  )# 船模试验螺旋桨转速
    nr =np.array([1.0049, 1.0052, 1.0078, 1.0109, 1.0132, 1.0138, 1.0123, 1.0087, 1.0038]  )# 船模试验螺旋桨相对旋转效率
    smoothing_param2 = 0.9999211451548893
    cstx2 = UnivariateSpline(n, nr, s=smoothing_param2, ext=3)  # ext=3 允许外推
    n1 = (1 - w) * U / (J * D)  # 螺旋桨转速 (r/s)
    n1_1 = n1 * 60  # rpm
    n_R = cstx2(n1)  # 相对旋转效率
    K_T = -0.203212669683257 * J ** 2 - 0.650037168713641 * J + 0.811410549450550
    K_Q = -0.038623141564318 * J ** 2 - 0.044613458306399 * J + 0.097828989010989
    n_o = K_T * J / (K_Q * 2 * np.pi)  # 敞水效率
    n_H = (1 - t) / (1 - w)  # 船身效率
    n_1 = 0.97  # 整流器效率
    n_2 = 0.97  # 逆变器效率
    n_3 = 0.94  # 推进电机效率

    """用于推进电功率"""
    Pe = R1 * U
    Pd = Pe / (n_H * n_o * n_R)  # 螺旋桨收到功率
    Pd2 = Pd / 0.94  # 推进电机功率
    Pp = Pe / (n_H * n_o * n_1 * n_2 * n_3 * n_R)  # 用于推进电功率

    """非推进用电功率"""
    Pcmax = 604.5  # 船舶辅助机械用电的最大功率
    fai2 = 0.8  # 船舶机械同时使用系数
    Pc = Pcmax * fai2  # 辅助机械用电功率
    Psmax = 197.2  # 船舶生活用电最大值
    fai1 = 0.4  # 船舶生活用电同时使用系数
    Ps = Psmax * fai1  # 日常生活用电功率
    n_4 = 0.98  # 690/400V变压器效率
    n_5 = 0.98  # 400V交流电网效率
    n_6 = 0.98  # 400/230V变压器效率
    Pn = Ps / (n_4 * n_5 * n_6) + Pc / (n_4 * n_5)  # 非推进用电功率

    """发电机组功率"""
    n_G = 0.9635  # 发电机组效率
    n_AC = 0.98  # 690V交流电网效率
    Pf = (Pp + Pn) / (n_G * n_AC)  # 发电机组输出功率
    Pfdan = Pf / 3  # 单台发电机功率
    """发电机油耗率"""
    taijia_P = np.array([799, 1198, 1361, 1599])
    taijia_g = np.array([196.8, 192.3, 187, 190])
    Oil_consum_rate = UnivariateSpline(taijia_P, taijia_g, s=0.00012977691803328083)  # 油耗率辅助曲线
    ge = Oil_consum_rate(Pfdan)  # 油耗率g/(kw h)
    # total_fuel_consumption_per_hour = Pf * ge / 1e3 # 单位时间油耗 (kg/h)
    Fuel_consum_ten_minutes = (Pf * ge / (6 * 1e6))  # 发电机组10分钟油耗量，单位：t
    # Fuel_consum_per_mile = (Pf * ge / (U * 3600 * 5.4 * 1e2))  # 发电机组单位距离油耗量 (t/mile)
    return Fuel_consum_ten_minutes