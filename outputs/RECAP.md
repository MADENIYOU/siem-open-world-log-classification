# RECAP — Open-World Hierarchical Classification (SIEVE)

Généré le 2026-11-10 09:24 | QUICK=False | backbone=distilbert-base-uncased | rotations=5 (inconnues par rotation=6)

## Configuration
```json
{
 "seed": 42,
 "backbone": "distilbert-base-uncased",
 "max_len": 96,
 "batch_size": 64,
 "epochs": 3,
 "lr": 5e-05,
 "weight_decay": 0.01,
 "warmup_ratio": 0.06,
 "lambda_cons": 0.5,
 "n_rotations": 5,
 "n_unknown": 6,
 "train_cap": 1500,
 "eval_cap": 300,
 "proto_cap": 300,
 "split_frac": [
  0.6,
  0.2,
  0.2
 ],
 "strict_min_groups": 5,
 "tpr_target": 0.95,
 "mc_passes": 5,
 "noise_levels": [
  0.1,
  0.2,
  0.3,
  0.4,
  0.5
 ],
 "fp16": true,
 "resume": true
}
```

## Données
```
                           format  rows_raw  bad_label  exact_dups_removed  conflict_rows_removed  rows_kept  n_classes  min_per_class  max_per_class  label_runs  mean_chars
p                                                                                                                                                                            
0.0  lines(delim=',',label=first)     35001          1                   4                      0      34996         30           1163           1167          30       150.9
0.1  lines(delim=',',label=first)     35001          1                   0                      0      35000         30           1166           1167          30       155.0
0.2  lines(delim=',',label=first)     35001          1                   0                      0      35000         30           1166           1167          30       159.6
0.3  lines(delim=',',label=first)     35001          1                   0                      0      35000         30           1166           1167          30       164.1
0.4  lines(delim=',',label=first)     35001          1                   0                      0      35000         30           1166           1167          30       167.6
0.5  lines(delim=',',label=first)     35001          1                   0                      0      35000         30           1166           1167          30       172.8
```

Classes strictes (split par template, sans fuite) : 19/30. Non strictes (fuite résiduelle, split aléatoire) : ['directory-changed', 'directory-created', 'directory-deleted', 'file-action-failure', 'file-deleted', 'file-modification', 'file-read', 'file-write', 'http-request-failure', 'http-request-success', 'user-session-open']

## Rotations des classes cachées
```
                                                                                                                       unknown                                          unknown_families  n_unknown_strict
rotation                                                                                                                                                                                                  
0                   [directory-deleted, file-action-failure, http-request-failure, ids-alert, process-shutdown, user-deletion]  [directory, file, http, network_security, process, user]                 3
1                    [authentication-failed, connection-opened, file-read, http-request-success, process-started, user-logout]   [authentication, connection, file, http, process, user]                 4
2                 [authentication-success, connection-closed, database-operation, file-modification, file-write, process-info]       [authentication, connection, file, process, system]                 4
3         [connection-failed, network-filtered, process-error, system-configuration-changed, user-creation, user-session-open]     [connection, network_security, process, system, user]                 5
4                    [directory-changed, directory-created, file-deleted, hardware-monitoring, network-traffic, process-ended]      [directory, file, network_security, process, system]                 3
```

## E1 — Closed-set (30 classes)
```
             rot test_set      f1  acc_fine  fam_acc  tax_dist     ece  cons_raw     n
model view                                                                            
hier  all     E1    clean  0.6813    0.7203   0.8155    0.4643  0.2134    0.9779  6882
      strict  E1    clean  0.5291    0.5809   0.7326    0.6865  0.3397    0.9779  4319
flat  all     E1    clean  0.6644    0.7058   0.7958    0.4984  0.2248       NaN  6882
      strict  E1    clean  0.5062    0.5578   0.7013    0.7409  0.3625       NaN  4319
```

## E2 — Détection d'inconnus (moyenne ± std sur rotations) — vue STRICT (sans fuite de template)
```
              n_rot          auroc        aupr_in       aupr_out          fpr95           oscr         osr_f1   known_reject     unk_accept    unk_fam_acc
model method                                                                                                                                              
flat  energy      5  0.722 ± 0.098  0.864 ± 0.049  0.506 ± 0.162  0.793 ± 0.191  0.533 ± 0.064  0.336 ± 0.033  0.064 ± 0.061  0.823 ± 0.221  0.361 ± 0.132
      mcd         5  0.716 ± 0.101  0.859 ± 0.056  0.492 ± 0.151  0.816 ± 0.177  0.524 ± 0.071  0.336 ± 0.033  0.061 ± 0.055  0.815 ± 0.193  0.361 ± 0.132
      msp         5  0.711 ± 0.104  0.858 ± 0.052  0.475 ± 0.178  0.830 ± 0.211  0.521 ± 0.074  0.335 ± 0.034  0.057 ± 0.037  0.824 ± 0.170  0.361 ± 0.132
      proto       5  0.727 ± 0.096  0.873 ± 0.045  0.509 ± 0.158  0.785 ± 0.184  0.537 ± 0.065  0.339 ± 0.033  0.064 ± 0.053  0.803 ± 0.228  0.361 ± 0.132
hier  energy      5  0.693 ± 0.090  0.849 ± 0.062  0.462 ± 0.086  0.890 ± 0.050  0.519 ± 0.069  0.332 ± 0.037  0.081 ± 0.048  0.789 ± 0.141  0.367 ± 0.180
      hier        5  0.692 ± 0.076  0.854 ± 0.052  0.442 ± 0.080  0.895 ± 0.051  0.517 ± 0.062  0.328 ± 0.039  0.078 ± 0.027  0.845 ± 0.046  0.367 ± 0.180
      mcd         5  0.679 ± 0.090  0.835 ± 0.064  0.437 ± 0.069  0.903 ± 0.025  0.506 ± 0.069  0.331 ± 0.038  0.091 ± 0.042  0.793 ± 0.108  0.367 ± 0.180
      msp         5  0.677 ± 0.089  0.837 ± 0.067  0.417 ± 0.077  0.930 ± 0.030  0.508 ± 0.069  0.331 ± 0.036  0.090 ± 0.018  0.826 ± 0.112  0.367 ± 0.180
      proto       5  0.702 ± 0.076  0.856 ± 0.052  0.464 ± 0.079  0.888 ± 0.060  0.522 ± 0.066  0.335 ± 0.036  0.091 ± 0.038  0.778 ± 0.083  0.367 ± 0.180
```

## E2 — idem vue ALL
```
              n_rot          auroc        aupr_in       aupr_out          fpr95           oscr         osr_f1   known_reject     unk_accept    unk_fam_acc
model method                                                                                                                                              
flat  energy      5  0.795 ± 0.078  0.939 ± 0.025  0.491 ± 0.165  0.746 ± 0.188  0.669 ± 0.053  0.656 ± 0.045  0.039 ± 0.037  0.823 ± 0.221  0.361 ± 0.132
      mcd         5  0.790 ± 0.078  0.937 ± 0.027  0.474 ± 0.152  0.773 ± 0.189  0.664 ± 0.059  0.657 ± 0.043  0.037 ± 0.033  0.815 ± 0.193  0.361 ± 0.132
      msp         5  0.777 ± 0.079  0.935 ± 0.026  0.438 ± 0.166  0.805 ± 0.178  0.654 ± 0.061  0.655 ± 0.040  0.041 ± 0.021  0.824 ± 0.170  0.361 ± 0.132
      proto       5  0.810 ± 0.072  0.946 ± 0.022  0.501 ± 0.162  0.743 ± 0.188  0.681 ± 0.051  0.659 ± 0.046  0.039 ± 0.031  0.803 ± 0.228  0.361 ± 0.132
hier  energy      5  0.758 ± 0.087  0.923 ± 0.037  0.438 ± 0.090  0.793 ± 0.149  0.643 ± 0.074  0.652 ± 0.054  0.050 ± 0.029  0.789 ± 0.141  0.367 ± 0.180
      hier        5  0.755 ± 0.062  0.926 ± 0.027  0.395 ± 0.050  0.859 ± 0.043  0.643 ± 0.055  0.643 ± 0.043  0.057 ± 0.026  0.845 ± 0.046  0.367 ± 0.180
      mcd         5  0.750 ± 0.083  0.916 ± 0.038  0.413 ± 0.070  0.814 ± 0.100  0.636 ± 0.068  0.651 ± 0.052  0.057 ± 0.025  0.793 ± 0.108  0.367 ± 0.180
      msp         5  0.743 ± 0.081  0.916 ± 0.039  0.377 ± 0.062  0.850 ± 0.097  0.634 ± 0.069  0.646 ± 0.048  0.063 ± 0.021  0.826 ± 0.112  0.367 ± 0.180
      proto       5  0.784 ± 0.065  0.937 ± 0.023  0.450 ± 0.081  0.803 ± 0.099  0.663 ± 0.057  0.652 ± 0.047  0.057 ± 0.023  0.778 ± 0.083  0.367 ± 0.180
```

## E3 — Closed-set sur connus & qualité hiérarchique
```
              n_rot             f1       acc_fine        fam_acc       tax_dist            ece       cons_raw
model view                                                                                                   
flat  all         5  0.725 ± 0.041  0.765 ± 0.042  0.837 ± 0.031  0.398 ± 0.068  0.168 ± 0.039      nan ± nan
      strict      5  0.589 ± 0.056  0.646 ± 0.060  0.760 ± 0.045  0.593 ± 0.096  0.268 ± 0.059      nan ± nan
hier  all         5  0.719 ± 0.055  0.762 ± 0.051  0.839 ± 0.038  0.399 ± 0.082  0.177 ± 0.036  0.982 ± 0.012
      strict      5  0.583 ± 0.075  0.642 ± 0.072  0.764 ± 0.054  0.594 ± 0.117  0.280 ± 0.049  0.982 ± 0.012
```

## Stabilité selon les classes cachées (AUROC strict)
```
              auroc_mean    ci95     min     max      cv
model method                                            
flat  energy      0.7222  0.1220  0.6173  0.8800  0.1360
      mcd         0.7156  0.1250  0.6147  0.8787  0.1407
      msp         0.7111  0.1287  0.6268  0.8844  0.1458
      proto       0.7268  0.1187  0.6367  0.8855  0.1315
hier  energy      0.6933  0.1115  0.6274  0.8367  0.1295
      hier        0.6921  0.0938  0.6113  0.8093  0.1092
      mcd         0.6789  0.1113  0.5908  0.8231  0.1320
      msp         0.6769  0.1101  0.6002  0.8192  0.1310
      proto       0.7024  0.0948  0.6247  0.8189  0.1087
```

## Hiérarchique − Flat (apparié)
```
               diff_mean  diff_ci95 wins  p_ttest  p_wilcoxon
method metric                                                
energy auroc     -0.0289     0.0516  1/5   0.1948      0.1875
       oscr      -0.0144     0.0144  0/5   0.0494      0.0625
       osr_f1    -0.0032     0.0178  2/5   0.6428      0.6250
mcd    auroc     -0.0367     0.0614  1/5   0.1726      0.1875
       oscr      -0.0181     0.0231  0/5   0.0943      0.0625
       osr_f1    -0.0046     0.0179  2/5   0.5154      0.6250
msp    auroc     -0.0342     0.0590  1/5   0.1829      0.1875
       oscr      -0.0128     0.0249  2/5   0.2253      0.3125
       osr_f1    -0.0047     0.0162  2/5   0.4670      0.6250
proto  auroc     -0.0244     0.0603  2/5   0.3238      0.6250
       oscr      -0.0145     0.0227  1/5   0.1504      0.1250
       osr_f1    -0.0041     0.0142  2/5   0.4691      0.4375
```

## E4 — Robustesse au bruit
```
                   auroc    oscr  osr_f1  known_reject  unk_accept
model method p                                                    
flat  energy 0.0  0.7222  0.5334  0.3356        0.0637      0.8229
             0.1  0.7175  0.5250  0.3332        0.0609      0.8229
             0.2  0.7111  0.5159  0.3305        0.0661      0.8165
             0.3  0.7002  0.5020  0.3253        0.0686      0.8184
             0.4  0.6944  0.4926  0.3227        0.0707      0.8125
             0.5  0.6853  0.4759  0.3154        0.0804      0.8057
      mcd    0.0  0.7156  0.5244  0.3360        0.0611      0.8145
      msp    0.0  0.7111  0.5206  0.3352        0.0570      0.8235
             0.1  0.7078  0.5152  0.3346        0.0608      0.8170
             0.2  0.7010  0.5084  0.3327        0.0680      0.8119
             0.3  0.6914  0.4954  0.3265        0.0704      0.8197
             0.4  0.6852  0.4860  0.3245        0.0756      0.8168
             0.5  0.6764  0.4699  0.3174        0.0851      0.8088
      proto  0.0  0.7268  0.5370  0.3394        0.0640      0.8025
             0.1  0.7218  0.5290  0.3375        0.0653      0.7971
             0.2  0.7156  0.5213  0.3358        0.0701      0.7894
             0.3  0.7037  0.5063  0.3298        0.0745      0.7900
             0.4  0.6975  0.4964  0.3266        0.0785      0.7861
             0.5  0.6882  0.4794  0.3186        0.0909      0.7747
hier  energy 0.0  0.6933  0.5189  0.3324        0.0809      0.7890
             0.1  0.6885  0.5074  0.3294        0.0844      0.7796
             0.2  0.6800  0.4960  0.3258        0.0950      0.7614
             0.3  0.6707  0.4809  0.3181        0.1043      0.7601
             0.4  0.6671  0.4723  0.3147        0.1118      0.7442
             0.5  0.6580  0.4538  0.3078        0.1185      0.7451
      hier   0.0  0.6921  0.5170  0.3281        0.0776      0.8453
             0.1  0.6869  0.5066  0.3270        0.0794      0.8268
             0.2  0.6788  0.4970  0.3251        0.0893      0.8074
             0.3  0.6699  0.4818  0.3183        0.0950      0.8036
             0.4  0.6642  0.4722  0.3143        0.1046      0.7944
             0.5  0.6563  0.4547  0.3074        0.1118      0.7856
      mcd    0.0  0.6789  0.5063  0.3314        0.0913      0.7928
      msp    0.0  0.6769  0.5078  0.3306        0.0896      0.8264
             0.1  0.6701  0.4954  0.3281        0.0893      0.8132
             0.2  0.6623  0.4852  0.3245        0.0966      0.7908
             0.3  0.6535  0.4700  0.3172        0.1026      0.7924
             0.4  0.6496  0.4618  0.3139        0.1104      0.7818
             0.5  0.6403  0.4433  0.3062        0.1155      0.7793
      proto  0.0  0.7024  0.5224  0.3353        0.0912      0.7783
             0.1  0.6977  0.5125  0.3330        0.0956      0.7645
             0.2  0.6917  0.5042  0.3306        0.1104      0.7408
             0.3  0.6824  0.4886  0.3216        0.1238      0.7388
             0.4  0.6774  0.4785  0.3188        0.1311      0.7249
             0.5  0.6703  0.4615  0.3105        0.1388      0.7175

               f1  acc_fine  fam_acc  tax_dist     ece
model p                                               
flat  0.0  0.5894    0.6463   0.7605    0.5932  0.2684
      0.1  0.5884    0.6403   0.7603    0.5994  0.2692
      0.2  0.5828    0.6312   0.7479    0.6209  0.2690
      0.3  0.5736    0.6189   0.7426    0.6385  0.2754
      0.4  0.5683    0.6114   0.7420    0.6466  0.2783
      0.5  0.5552    0.5948   0.7238    0.6814  0.2841
hier  0.0  0.5827    0.6420   0.7638    0.5942  0.2797
      0.1  0.5749    0.6304   0.7541    0.6155  0.2783
      0.2  0.5689    0.6226   0.7456    0.6318  0.2782
      0.3  0.5569    0.6051   0.7340    0.6609  0.2882
      0.4  0.5491    0.5967   0.7302    0.6731  0.2879
      0.5  0.5344    0.5774   0.7136    0.7090  0.2999
```

## Rejet par classe inconnue
```
model                          flat                        hier                                       famille stricte
method                       energy    mcd    msp  proto energy   hier    mcd    msp  proto                          
cls                                                                                                                  
authentication-failed         0.105  0.045  0.116  0.116  0.064  0.060  0.056  0.094  0.064    authentication    True
authentication-success        0.000  0.000  0.000  0.000  0.078  0.209  0.033  0.160  0.193    authentication    True
connection-closed             0.000  0.000  0.009  0.000  0.031  0.075  0.035  0.022  0.199        connection    True
connection-failed             0.019  0.007  0.022  0.059  0.290  0.227  0.164  0.193  0.331        connection    True
connection-opened             0.055  0.174  0.242  0.160  0.082  0.059  0.123  0.078  0.064        connection    True
database-operation            0.533  0.583  0.432  0.541  0.992  0.718  0.992  0.923  0.965            system    True
directory-changed             0.009  0.017  0.004  0.004  0.206  0.176  0.249  0.167  0.245         directory   False
directory-created             0.000  0.000  0.052  0.039  0.043  0.159  0.142  0.009  0.223         directory   False
directory-deleted             0.000  0.069  0.000  0.000  0.176  0.245  0.202  0.090  0.249         directory   False
file-action-failure           0.000  0.000  0.000  0.000  0.120  0.266  0.129  0.112  0.343              file   False
file-deleted                  0.215  0.215  0.133  0.193  0.116  0.030  0.215  0.026  0.137              file   False
file-modification             0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000              file   False
file-read                     0.120  0.296  0.339  0.026  0.361  0.335  0.369  0.369  0.309              file   False
file-write                    0.223  0.176  0.172  0.232  0.133  0.000  0.026  0.000  0.150              file   False
hardware-monitoring           0.090  0.137  0.113  0.142  0.000  0.057  0.028  0.165  0.000            system    True
http-request-failure          0.000  0.004  0.000  0.000  0.000  0.000  0.000  0.000  0.000              http   False
http-request-success          0.215  0.193  0.103  0.193  0.309  0.219  0.236  0.180  0.215              http   False
ids-alert                     0.015  0.122  0.198  0.103  0.359  0.328  0.382  0.263  0.473  network_security    True
network-filtered              1.000  1.000  0.970  1.000  0.970  0.018  0.705  0.289  0.120  network_security    True
network-traffic               0.000  0.031  0.000  0.000  0.000  0.000  0.000  0.000  0.000  network_security    True
process-ended                 0.005  0.005  0.021  0.010  0.000  0.005  0.000  0.005  0.005           process    True
process-error                 0.995  0.804  0.742  0.995  0.979  0.361  0.866  0.856  0.964           process    True
process-info                  0.319  0.422  0.470  0.699  0.000  0.000  0.000  0.000  0.000           process    True
process-shutdown              0.000  0.000  0.000  0.000  0.000  0.072  0.000  0.000  0.113           process    True
process-started               0.068  0.023  0.098  0.064  0.428  0.424  0.432  0.295  0.485           process    True
system-configuration-changed  0.226  0.236  0.038  0.184  0.264  0.274  0.368  0.354  0.340            system    True
user-creation                 0.420  0.337  0.443  0.513  0.363  0.130  0.340  0.430  0.247              user    True
user-deletion                 0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000  0.000              user    True
user-logout                   0.000  0.000  0.070  0.000  0.000  0.000  0.012  0.000  0.004              user    True
user-session-open             0.966  0.991  0.781  0.991  0.004  0.004  0.086  0.004  0.017              user   False
```

## Limites à discuter dans le papier
- Données **synthétiques** (440 templates × Faker) : une fuite de template résiduelle existe pour les classes non strictes → privilégier la vue `strict`.
- Les groupes sont **reconstruits** par clustering (k connu) : approximation des templates réels.
- La **taxonomie est une construction** à valider par un expert SIEM.
- Masquer des classes **simule** l'open-set ; ne prouve pas la détection de toute nouveauté réelle.
- Pas de test CDS réel (440 logs non fournis) : les versions bruitées mesurent la robustesse lexicale, pas le transfert réel.
- Non couverts : OpenMax, ensembles profonds (seul MC-Dropout est testé).
- 5 rotations : IC95 larges, Wilcoxon p_min = 2/2^5.
