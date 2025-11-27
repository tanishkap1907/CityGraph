# CityGraph – NYC Taxi Graph Analytics & Streaming Pipeline  
**Technologies:** Neo4j, Docker, Kubernetes (Minikube), Kafka, ZooKeeper, Python, Cypher, Neo4j GDS Library

CityGraph is a complete graph-based data engineering system constructed through two interconnected projects.  
It demonstrates large-scale data ingestion, graph modeling, distributed streaming, and real-time graph analytics using modern data infrastructure.

---

## 🚦 Project Overview

### 📌 **Project 1 — Dockerized Neo4j Graph Processing**
A complete graph construction and analytics workflow that:
- Processes **2.9M+ NYC taxi trip records**
- Loads structured graph data into **Neo4j**
- Implements **PageRank** and **BFS** using the **Neo4j GDS Library**
- Fully automated using a custom **Dockerfile**  
- Achieved **100/100** accuracy in all grading tests (data loading + PageRank + BFS)

📁 **Folder:** `cse511-project1/`

---

### 📌 **Project 2 — Real-Time Kafka → Neo4j Streaming Pipeline (Kubernetes)**
A distributed data streaming system that:
- Ingests and streams data using **Kafka**
- Uses **Kubernetes (Minikube)** for scalable orchestration
- Deploys Neo4j via **Helm**
- Transfers streaming messages → Kafka → Neo4j through **Kafka Connect**
- Ensures high-availability ingestion with automated connector configuration  
- Achieved **100/100** end-to-end pipeline validation

📁 **Folder:** `Project-2/`

---

## 🧠 Key Features
- 🚀 Fully Dockerized, reproducible Neo4j environment  
- 🔁 Real-time streaming from Kafka into Neo4j  
- 🧮 Graph algorithms implemented: PageRank & BFS  
- ⚙️ Kubernetes orchestrated microservices  
- 📡 Kafka Connect automated graph ingestion  
- 📦 Structured ETL using Cypher + Python  
- 🔍 High-availability pipeline with proven reproducibility  

---

## 📂 Repository Structure

