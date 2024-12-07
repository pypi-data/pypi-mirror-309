import numpy as np


def surftensW(temp):
    # surftensW=surftensW(temp)
    #
    # temp           Temperatur               in K
    # surftensW      Oberflächenspannung      in N/m
    #
    # Diese Funktion berechnet die thermische Leitfähigkeit einer H2O-LiBr-Lösung
    # der Temperatur temp und der Salzkonzentration konz
    #
    # Die Berechnung erfolgt nach
    # Daten des VDI-WA8 Abschnitt DB Tabelle 6. Stoffwerte von Wasser im Sättigungszustand vom Tripel- bis zum kritischen Punkt.
    #
    # Erstellt
    # 15.12.2003 JA

    # Zahlenwerte aus VDI in °C und 10**-3 N/m

    t_W = [0.01, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220,
           230, 240, 250, 260, 270, 280, 290, 300, 310, 320, 330, 340, 350, 360, 370]
    sig_W = np.asarray(
        [75.65, 74.22, 72.74, 71.2, 69.6, 67.95, 66.24, 64.49, 62.68, 60.82, 58.92, 56.97, 54.97, 52.94, 50.86, 48.75,
         46.6, 44.41, 42.2, 39.95, 37.68, 35.39, 33.08, 30.75, 28.4, 26.05, 23.7, 21.35, 19, 16.68, 14.37, 12.1, 9.875,
         7.713, 5.636, 3.675, 1.886, 0.3948]) * 0.001
    p, S, mu = np.polyfit(t_W, sig_W, 4)

    temp_dach = ((temp - 273.15 - mu[0]) / mu[
        1])  # Umrechung zur Berücksichtigung von centering and scaling, da polyfit mit mu aufgerufen

    return np.polyval(p, temp_dach)  # sigma in N/m
