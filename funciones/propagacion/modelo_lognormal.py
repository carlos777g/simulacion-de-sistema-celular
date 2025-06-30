import numpy as np

def model_lognormal(mobiles, Pt_dBm=43, Gt_dB=15, Gr_dB=0, alpha=3.5, sigma=6):
    """
    Calcula pérdidas y potencia recibida según el modelo lognormal.
    
    Parameters:
    - mobiles: lista de dicts con clave "distancia_real"
    - Pt_dBm: potencia transmitida (dBm)
    - Gt_dB: ganancia de antena transmisora (dB)
    - Gr_dB: ganancia de antena receptora (dB)
    - alpha: exponente de pérdida
    - sigma: desviación estándar del desvanecimiento lento
    
    Returns:
    - Lista de dicts con pérdida, shadowing y potencia recibida
    """
    dist_m = np.array([m["distancia_real"] for m in mobiles])
    dist_km = dist_m / 1000
    n = len(dist_km)

    Ld_log = 10 * alpha * np.log10(dist_km + 1e-6)  # evitamos log(0)
    Xsigma = np.random.randn(n) * sigma
    Pr = Pt_dBm + Gt_dB + Gr_dB - Ld_log - Xsigma

    return [
        {
            "distance": dist_m[i],
            "loss_d": Ld_log[i],
            "shadowing": Xsigma[i],
            "Pr_log": Pr[i]
        }
        for i in range(n)
    ] 
