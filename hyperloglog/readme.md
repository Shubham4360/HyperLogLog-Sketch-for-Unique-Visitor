# 🚀 HyperLogLog Sketch for Unique Visitor Counting in Massive Real-Time GitHub Data Streams


## 📌 Project Overview

This project implements a real-time big data streaming system that estimates the number of unique GitHub users using the HyperLogLog probabilistic data structure.

The system consumes real-time GitHub events, processes massive data streams using Apache Kafka and Apache Spark Structured Streaming, and compares:

- Exact unique user counting
- HyperLogLog approximate counting


The goal is to demonstrate how HyperLogLog reduces memory consumption while maintaining high accuracy for large-scale streaming analytics.


---

# 🏗️ System Architecture

            GitHub Events API

                   |

                   |

             Python Producer

                   |

                   |

                Kafka

                   |

                   |

      Spark Structured Streaming

                   |

      ----------------------------

      |                          |

 Exact Counter             HyperLogLog

      |                          |

      ----------------------------

                   |

                   |

             PostgreSQL

                   |

                   |

          Streamlit Dashboard




---

# ✨ Features


## Real-Time Data Streaming

- Fetches live GitHub public events
- Streams events continuously
- Sends data through Apache Kafka


## HyperLogLog Analytics

- Approximate unique visitor counting
- Fixed memory usage
- Configurable precision
- Error measurement


## Big Data Technologies

- Apache Kafka
- Apache Spark Structured Streaming
- PostgreSQL
- Docker
- Streamlit


## Monitoring Dashboard

Displays:

- Total events processed
- Exact unique users
- HyperLogLog estimate
- Accuracy percentage
- Memory usage
- Real-time charts


---

# 🛠️ Technology Stack


| Technology | Purpose |
|------------|---------|
| Python | Application development |
| Kafka | Event streaming |
| Spark | Stream processing |
| HyperLogLog | Approximate counting |
| PostgreSQL | Data storage |
| Streamlit | Visualization |
| Docker | Deployment |


---

# 📂 Project Structure

final_project/
│

├── producer/

│ ├── github_api.py

│ ├── kafka_producer.py

│ └── github_producer.py

│

├── consumer/

│ ├── spark_consumer.py

│ ├── hll_counter.py

│ └── exact_counter.py

│

├── database/

│ ├── postgres.py

│ └── schema.sql

│

├── dashboard/

│ ├── app.py

│ └── charts.py

│

├── config/

│ ├── settings.py

│ └── logging_config.py

│

├── tests/

│

├── docker-compose.yml

├── requirements.txt

└── README.md



