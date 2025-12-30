import time
import numpy as np
import matplotlib.pyplot as plt

def evaluate_system_performance(y_true, y_pred, processing_times):
    """
    Evaluates the system using standard classification metrics.
    """
    # Calculate metrics
    tp = np.sum((y_true == 1) & (y_pred == 1))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))

    accuracy = (tp + tn) / len(y_true)
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    avg_response_time = np.mean(processing_times)

    print("--- DAY 7: SYSTEM EVALUATION REPORT ---")
    print(f"Accuracy:      {accuracy:.2%}")
    print(f"Precision:     {precision:.2%}")
    print(f"Recall:        {recall:.2%}")
    print(f"Avg Response:  {avg_response_time:.4f} seconds per frame")
    
    return {"Accuracy": accuracy, "Precision": precision, "Recall": recall}

# Simulated Data: 1 = Detection (e.g., weapon), 0 = No Detection
true_labels = np.array([1, 0, 1, 1, 0, 0, 1, 0, 1, 0])
pred_labels = np.array([1, 0, 1, 0, 0, 0, 1, 0, 1, 1]) # One False Negative, One False Positive
response_times = [0.045, 0.042, 0.050, 0.048, 0.041, 0.043, 0.047, 0.046, 0.049, 0.044]

metrics = evaluate_system_performance(true_labels, pred_labels, response_times)