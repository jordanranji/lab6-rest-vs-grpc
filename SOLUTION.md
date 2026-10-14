| Method | Local | Same-Zone | Different Region |
| REST add | 2.34 | 2.19 | 2.14 |
| gRPC add | 0.72 | 0.74 | 0.700 |
| REST rawimg | 4.19 | 4.31 | 4.25 |
| gRPC rawimg | 11.18 | 8.56 | 8.27 |
| REST dotproduct | 2.86 | 2.74 | 2.63 |
| gRPC dotproduct | 0.769 | 0.81 | 0.78 |
| REST jsonimg | 26.5 | 26.37 | 26.33 |
| gRPC jsonimg | 24.3 | 24.42 | 24.40 |
| PING | 0.044 | 0.044 | 0.088 |


gRPC was much lower in add and dot product. In raw it was much longer, and in JSON Image it was very similar. Across local, same-zone, and different region they were almost all the same/similar.\
The biggest difference was in ping, which doubled in different region vs. local or same. 
