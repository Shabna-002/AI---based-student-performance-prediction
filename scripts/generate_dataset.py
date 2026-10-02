import os
import random
import numpy as np
import pandas as pd

np.random.seed(42)
random.seed(42)

def generate_student_dataset(n_samples=1200):
    records = []
    
    for _ in range(n_samples):
        # Latent academic capability (latent factor between 25 and 98)
        # Mixture of normal distributions: high performers, average performers, struggling performers
        cluster = np.random.choice(["struggling", "average", "high"], p=[0.25, 0.45, 0.30])
        
        if cluster == "high":
            cap = np.random.normal(loc=84, scale=6)
            failures = 0 if np.random.rand() > 0.03 else 1
        elif cluster == "average":
            cap = np.random.normal(loc=65, scale=7)
            failures = np.random.choice([0, 1, 2], p=[0.70, 0.22, 0.08])
        else: # struggling
            cap = np.random.normal(loc=44, scale=8)
            failures = np.random.choice([1, 2, 3, 4, 5], p=[0.30, 0.30, 0.20, 0.12, 0.08])
            
        cap = float(np.clip(cap, 20.0, 99.0))
        
        # Correlated metrics with realistic noise
        attendance = float(np.clip(np.random.normal(loc=cap * 0.75 + 22, scale=6.5), 35.0, 100.0))
        internal = float(np.clip(np.random.normal(loc=cap * 0.88 + 8, scale=5.5), 20.0, 100.0))
        assignment = float(np.clip(np.random.normal(loc=cap * 0.80 + 16, scale=7.0), 30.0, 100.0))
        
        # GPA calculation based on academic performance and backlogs
        base_gpa = (
            (internal * 0.40) +
            (assignment * 0.25) +
            (attendance * 0.15) +
            (cap * 0.20)
        ) / 10.0 - (failures * 0.45) + np.random.normal(0, 0.2)
        
        gpa = float(np.clip(round(base_gpa, 2), 2.50, 9.95))
        
        # Composite score to determine ground truth class
        score = (
            (internal * 0.35) +
            (assignment * 0.25) +
            (attendance * 0.15) +
            (gpa * 10.0 * 0.25) -
            (failures * 5.0)
        )
        
        # Add slight boundary noise (3%) for real-world stochasticity
        noise = np.random.normal(0, 2.0)
        eff_score = score + noise
        
        if eff_score >= 74.0 and failures == 0 and gpa >= 7.2:
            performance = "High"
        elif eff_score >= 54.0 and failures <= 1 and gpa >= 5.3:
            performance = "Average"
        else:
            performance = "Low"
            
        records.append({
            "attendance": round(attendance, 1),
            "internal": round(internal, 1),
            "assignment": round(assignment, 1),
            "gpa": gpa,
            "failures": int(failures),
            "performance": performance
        })
        
    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    df = generate_student_dataset(1200)
    print("Dataset distribution:")
    print(df["performance"].value_counts())
    print("\nSummary statistics:")
    print(df.describe().round(2))
    
    out_path = "ml/student_performance.csv"
    df.to_csv(out_path, index=False)
    print(f"\nSuccessfully generated and saved {len(df)} records to {out_path}")
