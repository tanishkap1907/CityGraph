import pyarrow.parquet as pq
import pandas as pd
from neo4j import GraphDatabase
import time


class DataLoader:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self.driver.verify_connectivity()

    def close(self):
        self.driver.close()

    def load_transform_file(self, file_path):
        # Read parquet
        trips = pq.read_table(file_path).to_pandas()

        # Filter required columns
        trips = trips[['tpep_pickup_datetime', 'tpep_dropoff_datetime', 
                       'PULocationID', 'DOLocationID', 'trip_distance', 'fare_amount']]

        # Filter Bronx locations
        bronx = [3, 18, 20, 31, 32, 46, 47, 51, 58, 59, 60, 69, 78, 81, 94, 
                 119, 126, 136, 147, 159, 167, 168, 169, 174, 182, 183, 184, 
                 185, 199, 200, 208, 212, 213, 220, 235, 240, 241, 242, 247, 
                 248, 250, 254, 259]
        trips = trips[trips['PULocationID'].isin(bronx) & trips['DOLocationID'].isin(bronx)]
        trips = trips[trips['trip_distance'] > 0.1]
        trips = trips[trips['fare_amount'] > 2.5]

        # Convert datetime columns
        trips['tpep_pickup_datetime'] = pd.to_datetime(trips['tpep_pickup_datetime'])
        trips['tpep_dropoff_datetime'] = pd.to_datetime(trips['tpep_dropoff_datetime'])

        # Create Location nodes
        location_ids = pd.unique(trips[['PULocationID', 'DOLocationID']].values.ravel())
        with self.driver.session() as session:
            session.run(
                """
                UNWIND $locs AS id
                MERGE (:Location {name: id})
                """,
                locs=[int(x) for x in location_ids]
            )

            # Create TRIP relationships in batches
            trips_list = trips.to_dict('records')
            batch_size = 500
            for i in range(0, len(trips_list), batch_size):
                batch = trips_list[i:i+batch_size]
                session.run(
                    """
                    UNWIND $batch AS t
                    MATCH (pu:Location {name: t.PULocationID})
                    MATCH (do:Location {name: t.DOLocationID})
                    CREATE (pu)-[:TRIP {
                        distance: t.trip_distance,
                        fare: t.fare_amount,
                        pickup_dt: datetime(t.tpep_pickup_datetime),
                        dropoff_dt: datetime(t.tpep_dropoff_datetime)
                    }]->(do)
                    """,
                    batch=batch
                )


def main():
    total_attempts = 10
    attempt = 0
    while attempt < total_attempts:
        try:
            data_loader = DataLoader("neo4j://localhost:7687", "neo4j", "graphprocessing")
            data_loader.load_transform_file("/var/lib/neo4j/import/yellow_tripdata_2022-03.parquet")
            data_loader.close()
            print("Data loaded successfully!")
            attempt = total_attempts
        except Exception as e:
            print(f"(Attempt {attempt+1}/{total_attempts}) Error: {e}")
            attempt += 1
            time.sleep(10)


if __name__ == "__main__":
    main()