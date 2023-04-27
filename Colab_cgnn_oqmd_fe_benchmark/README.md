# Training a CGNN model on Colab

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Tony-Y/oqmd-v1.2-dataset-for-cgnn/blob/main/CGNN_oqmd_fe_benchmark.ipynb)

## Output Files

* log.txt
* history.csv
* test_predictions.csv
* model.pth

| Model      | RMSE (meV) | MAE (meV)  | Time   |
|------------|-----------:|-----------:|-------:|
| Benchmark  |       86.1 |       42.7 | 1h 19m |
| Database   |      124.2 |       84.8 |     NA |

<p>
  <img src="images/training_history.png" width=30%>
  <img src="images/test_prediction.png" width=30%>
</p>

## Computational Environment 

* Nvidia T4
* PyTorch 2.0.0
* CUDA 11.8

(April 27, 2023)