import os
import pandas as pd
import matplotlib.pyplot as plt


file = "5B.txt"
columns = ["Temps (s)", "Depl (mm)", "Force (kN)", "Jauge 0", "Jauge 1", "Jauge 2", "Jauge 3"]
step = 1


root = os.path.join(os.path.dirname(__file__), file)


valid_lines = []

with open(root, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        parts = line.split("\t")

        try:
            time = float(parts[2].replace(",", "."))
            depl = float(parts[3].replace(",", "."))
            force = float(parts[4].replace(",", "."))
            jauge0 = float(parts[5].replace(",", "."))
            jauge1 = float(parts[6].replace(",", "."))
            jauge2 = float(parts[7].replace(",", "."))
            jauge3 = float(parts[8].replace(",", "."))
        except:
            continue

        if depl == 0.0:
            continue

        valid_lines.append(parts)


columns_ = ["Date", "Heure", "Temps (s)", "Depl (mm)",
            "Force (kN)", "Jauge 0", "Jauge 1", "Jauge 2", "Jauge 3"]

df = pd.DataFrame(valid_lines, columns=columns_)

for col in columns_[2:]:
    df[col] = df[col].str.replace(",", ".", regex=False).astype(float)


df = df[columns]
df = df.iloc[::step].reset_index(drop=True)
df = df.sort_index().reset_index(drop=True)

continous_time = []
offset = 0.0

for i in range(len(df)):
    t = df.loc[i, "Temps (s)"]

    if i > 0:
        t_prev = df.loc[i - 1, "Temps (s)"]

        if t < t_prev:
            offset += t_prev

    continous_time.append(t + offset)

df["Temps (s)"] = continous_time


print(df.head())
print(f"\nFilas finales: {len(df)}")

# Guardar el resultado en la misma carpeta del script
output = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "Clean_data_5_B.csv"
)

df.to_csv(output, index=False)

print(f"Archivo guardado en: {output}")