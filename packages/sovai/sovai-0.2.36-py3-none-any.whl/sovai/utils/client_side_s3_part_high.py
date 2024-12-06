import pyarrow.dataset as ds
from pyarrow.fs import S3FileSystem
import pyarrow as pa
import pandas as pd
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from sovai.tools.authentication import authentication
import os
import pandas as pd
import pyarrow as pa
import pyarrow.dataset as ds
import s3fs
import logging
import datetime
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from pyarrow.fs import S3FileSystem


# Try to import CustomDataFrame, use regular DataFrame if not available
try:
    from sovai.extensions.pandas_extensions import CustomDataFrame
    HAS_CUSTOM_DATAFRAME = True
except ImportError:
    HAS_CUSTOM_DATAFRAME = False
    CustomDataFrame = pd.DataFrame  # Fallback to regular DataFrame


@lru_cache(maxsize=2)
def get_cached_s3_filesystem(storage_provider):
    return authentication.get_s3_filesystem_pickle(storage_provider, verbose=True)

@lru_cache(maxsize=2)
def get_cached_s3fs_filesystem(storage_provider):
    return authentication.get_s3fs_filesystem_json(storage_provider, verbose=True)


# Configure logging to output to both console and a log file
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("data_operations.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# -------------------------------
# Helper Functions
# -------------------------------

def construct_s3_path(type_name, provider, partition_type, ticker=None, publish_date=None, year=None, all_dates_after=False):
    """
    Construct the S3 path based on the partitioning scheme.

    Parameters:
    - type_name (str): Type of data (e.g., 'applications')
    - provider (str): 'wasabi' or 'digitalocean'
    - partition_type (str): 'date' or 'ticker'
    - ticker (str, optional): Ticker symbol
    - publish_date (str, optional): Publish date in 'YYYY-MM-DD' format
    - year (int, optional): Year extracted from publish_date
    - all_dates_after (bool, optional): If True, scan all date partitions after a certain date

    Returns:
    - str: Constructed S3 path
    """
    if provider=="digitalocean":
        bucket ="sovai/sovai-patents-export"
    else:
        bucket = "sovai-patents-export"
        

    if partition_type == "date":
        if all_dates_after:
            # Return the parent directory to scan all date partitions
            path = f"{type_name}/date/"
        else:
            if not publish_date:
                raise ValueError("publish_date must be provided for date partitioning.")
            path = f"{type_name}/date/date_partitioned={publish_date}/"
    elif partition_type == "ticker":
        if not ticker or not year:
            raise ValueError("Both ticker and year must be provided for ticker partitioning.")
        path = f"{type_name}/ticker/ticker_partitioned={ticker}/year={year}/"
    else:
        raise ValueError("Invalid partition_type. Choose 'date' or 'ticker'.")

    return f"{bucket}/{path}"


def list_date_partitions(provider, type_name):
    s3_path = construct_s3_path(type_name, provider, partition_type="date", all_dates_after=True)
    fs = get_cached_s3fs_filesystem(provider)
    try:
        partitions = fs.ls(s3_path)
        dates = []
        for partition in partitions:
            basename = os.path.basename(partition.rstrip('/'))
            if basename.startswith('date_partitioned='):
                date_str = basename.split('=')[1]
                try:
                    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
                    dates.append((date_obj, partition))
                except ValueError:
                    logger.warning(f"Unable to parse date from partition {partition}")
        return dates
    except Exception as e:
        logger.error(f"Error listing date partitions in {s3_path} ({provider}): {e}")
        return []

def load_parquet_from_s3(s3_path, provider, columns=None, start_date=None):
    """
    Load a Parquet file from S3 into a pandas DataFrame with optional date filtering.

    Parameters:
    - s3_path (str): S3 path to the Parquet file or directory
    - provider (str): 'wasabi' or 'digitalocean'
    - columns (list, optional): List of columns to select
    - start_date (str, optional): Minimum date in 'YYYY-MM-DD' format to filter the data

    Returns:
    - pandas.DataFrame: Loaded DataFrame
    """
    
    fs = get_cached_s3_filesystem(provider)
    
    try:
        dataset = ds.dataset(s3_path, filesystem=fs, format='parquet')

        if start_date:
            # Convert start_date string to pyarrow date32 scalar
            min_date_pa = pa.scalar(pd.to_datetime(start_date).date(), type=pa.date32())
            # Use ds.field to construct the filter expression
            filter_expr = ds.field('date') >= min_date_pa
            dataset = dataset.filter(filter_expr)

        table = dataset.to_table(columns=columns)

        # Log the schema for debugging
        logger.info(f"Schema for {s3_path} ({provider}):")
        logger.info(table.schema)

        df = table.to_pandas()

        partition_cols = ['ticker', 'date']
        existing_cols = [col for col in partition_cols if col in df.columns]
        other_cols = [col for col in df.columns if col not in partition_cols]
        df = df[existing_cols + other_cols]

        return df
    except Exception as e:
        logger.error(f"Error loading data from {s3_path} ({provider}): {e}")
        return pd.DataFrame()

# -------------------------------
# Loading Functions
# -------------------------------

def load_data_by_ticker(
    type_name,
    providers=['wasabi', 'digitalocean'],
    tickers=None,
    start_date=None,
    columns=None,
    max_workers=4
):
    """
    Load data for specified tickers and/or dates from S3 storage providers.

    Parameters:
    - type_name (str): Type of data (e.g., 'applications', 'prediction_all', etc.)
    - providers (list, optional): List of storage providers to load from ('wasabi', 'digitalocean')
    - tickers (str or list, optional): Ticker symbol(s) to load data for
    - start_date (str, optional): Minimum publishDate to filter data by (format 'YYYY-MM-DD') (only for date partitioning)
    - columns (list, optional): List of columns to select
    - max_workers (int, optional): Number of parallel threads

    Returns:
    - pandas.DataFrame: Concatenated DataFrame containing the loaded data
    """
    date_tasks = []
    ticker_tasks = []
    results = []

    # Normalize input parameters
    if tickers and isinstance(tickers, str):
        tickers = [tickers]
    if not tickers:
        tickers = []
    
    # If both tickers and min_date are provided
    if tickers and start_date:
        try:
            min_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            min_year = min_date_obj.year
            logger.info(f"Minimum date provided: {min_date_obj} (Year: {min_year})")
        except ValueError:
            logger.error(f"Invalid min_date format: {start_date}. Expected 'YYYY-MM-DD'.")
            return pd.DataFrame()

        for provider in providers:
            for ticker in tickers:
                # Determine the range of years to load based on start_date
                # Assuming data starts from 2011
                start_year = min_year
                current_year = datetime.datetime.now().year
                for year in range(start_year, current_year + 1):
                    s3_path = construct_s3_path(
                        type_name, provider, partition_type="ticker",
                        ticker=ticker, year=year
                    )
                    ticker_tasks.append((s3_path, provider, columns, None))  # No additional filtering here

    # If only min_date is provided
    elif start_date and not tickers:
        try:
            min_date_obj = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
            logger.info(f"Minimum date provided: {min_date_obj}")
        except ValueError:
            logger.error(f"Invalid start_date format: {start_date}. Expected 'YYYY-MM-DD'.")
            return pd.DataFrame()

        for provider in providers:
            # List all date-based partitions
            date_partitions = list_date_partitions(provider, type_name)
            for date_obj, partition_path in date_partitions:
                if date_obj >= min_date_obj:
                    date_tasks.append((partition_path, provider, columns, None))

    # If only tickers are provided
    elif tickers and not start_date:
        for provider in providers:
            for ticker in tickers:
                # Assuming data starts from 2011
                start_year = 2010 ## Change this to 2008 eventually
                current_year = datetime.datetime.now().year
                for year in range(start_year, current_year + 1):
                    s3_path = construct_s3_path(
                        type_name, provider, partition_type="ticker",
                        ticker=ticker, year=year
                    )
                    ticker_tasks.append((s3_path, provider, columns, None))

    else:
        logger.warning("No tickers or start_date provided. Please provide at least one.")
        return pd.DataFrame()

    # Combine all tasks
    all_tasks = ticker_tasks + date_tasks

    if not all_tasks:
        logger.warning("No tasks to process. Exiting.")
        return pd.DataFrame()

    def load_task(task):
        s3_path, provider, columns, ticker_filter = task
        df = load_parquet_from_s3(s3_path, provider, columns, start_date=start_date if ticker_filter is None else None)
        if not df.empty and ticker_filter:
            if 'ticker' in df.columns:
                df = df[df['ticker'].isin(ticker_filter)]
            else:
                logger.warning(f"'ticker' column not found in data from {s3_path} ({provider}). Skipping ticker filter.")
        return df

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_task = {executor.submit(load_task, task): task for task in all_tasks}
        for future in tqdm(as_completed(future_to_task), total=len(all_tasks), desc="Loading data"):
            df = future.result()
            if not df.empty:
                results.append(df)

    if results:
        final_df = pd.concat(results, ignore_index=True)
        logger.info(f"Successfully loaded data with {len(final_df)} records.")
    else:
        final_df = pd.DataFrame()
        logger.warning("No data found.")

    return final_df

# -------------------------------
# Example Usage
# -------------------------------


def load_frame_s3_paritioned_high(endpoint, tickers=None, columns=None, start_date=None, end_date=None):

    endpoint_config = {
        "patents/applications": {
            "bucket": {
                "digitalocean": "sovai/sovai-patents-export",
                "wasabi": "sovai-patents-export"
            },
            "type": "applications"
        },
    }
    
    if endpoint not in endpoint_config:
        raise ValueError(f"Invalid endpoint: {endpoint}")
    
    config = endpoint_config[endpoint]


    loaded_df_both = load_data_by_ticker(
        type_name=config["type"],
        providers=['digitalocean'],
        tickers=tickers,
        start_date=start_date,
        columns=columns,
        max_workers=8  # Adjust based on your system's capabilities
    )

    
    if HAS_CUSTOM_DATAFRAME:
        return CustomDataFrame(loaded_df_both)
    else:
        return loaded_df_both  # Returns a regular pandas DataFrame if CustomDataFrame is not available

