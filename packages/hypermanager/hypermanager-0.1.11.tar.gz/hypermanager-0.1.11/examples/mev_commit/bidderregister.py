import asyncio
import polars as pl
from hypermanager.events import EventConfig
from hypermanager.manager import HyperManager
from hypermanager.protocols.mev_commit import mev_commit_config


async def get_events():
    """
    Fetch event logs for the UnopenedCommitmentStored event from the MEV-Commit system.
    Demonstrates three different queries:
    1. All historical events.
    2. Events from a specific block onward.
    3. Events within the most recent block range.

    The results are returned as Polars DataFrames and their shapes are printed.
    """
    manager = HyperManager(url="https://mev-commit.hypersync.xyz")

    bidder_register_config = mev_commit_config['BidderRegistered']
    # bidder_register_config = mev_commit_config['OpenedCommitmentStored']

    # Query events using the event configuration and return the result as a Polars DataFrame
    df: pl.DataFrame = await manager.execute_event_query(
        bidder_register_config,
        tx_data=True,
        # block_range=10_000
    )

    print(df)
    df.write_csv("opened_commitment_stored.csv")

# Entry point: Run the async function to execute the event queries
if __name__ == "__main__":
    # Use asyncio to run the asynchronous function in an event loop
    asyncio.run(get_events())
