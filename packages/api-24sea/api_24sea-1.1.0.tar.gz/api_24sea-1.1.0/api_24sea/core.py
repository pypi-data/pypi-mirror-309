# -*- coding: utf-8 -*-
"""The core module for the datasignals package
"""

import datetime
import logging
import os
from typing import Any, Dict, List, Optional, Union
from warnings import simplefilter

import pandas as pd
import requests as req
from pydantic import validate_call

# Local imports
from . import exceptions as E
from . import utils as U
from .datasignals import schemas as S

try:
    # delete the accessor to avoid warning
    del pd.DataFrame.datasignals
except AttributeError:
    pass

# This filter is used to ignore the PerformanceWarning that is raised when
# the DataFrame is modified in place. This is the case when we add columns
# to the DataFrame in the get_data method.
# This is the only way to update the DataFrame in place when using accessors
# and performance is not an issue in this case.
# See https://stackoverflow.com/a/76306267/7169710 for reference.
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

logging.basicConfig(format="%(message)s", level=logging.INFO)


class API:
    """Accessor for working with data signals coming from the 24SEA API."""

    def __init__(
        self, username: Optional[str] = None, password: Optional[str] = None
    ):
        self.base_url: str = f"{U.BASE_URL}datasignals/"
        self.username: Optional[str] = username
        self.password: Optional[str] = password
        self.auth: Optional[req.auth.HTTPBasicAuth] = None
        self.authenticated: bool = False
        self.metrics_overview: Optional[pd.DataFrame] = None

        if self.username and self.password:
            self.authenticate(self.username, self.password)
        else:
            self._auto_authenticate

    @property
    def _auto_authenticate(self):
        """Automatically authenticate using environment variables if available."""
        username = os.getenv("24SEA_API_USERNAME")
        password = os.getenv("24SEA_API_PASSWORD")
        if username and password:
            self.authenticate(username, password)

    @validate_call
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate the user with the 24SEA API. Additionally, define
        the ``metrics_overview`` dataframe.

        Parameters
        ----------
        username : str
            The username to authenticate.
        password : str
            The password to authenticate.

        Returns
        -------
        bool
            True if the authentication was successful, otherwise False.
        """
        # -- Step 1: Authenticate and check the credentials
        self.username = username
        self.password = password
        self.auth = req.auth.HTTPBasicAuth(self.username, self.password)
        # fmt: off
        try:
            r_profile = U.handle_request(
                f"{self.base_url}profile",
                {"username": self.username},
                self.auth,
                {"accept": "application/json"},
            )
            if r_profile.ok:
                self.authenticated = True
            logging.info("\033[32;1mThis dataframe has now access to https://api.24sea.eu/.\033[0m")  # noqa: E501  # pylint: disable=C0301
        except req.exceptions.HTTPError:
            raise E.AuthenticationError("\033[31;1mThe username and/or password are incorrect.\033[0m")  # noqa: E501  # pylint: disable=C0301
        # fmt: on
        # -- Step 2: Define the metrics_overview dataframe
        if self.metrics_overview is not None:
            return self.authenticated
        logging.info("Now getting your metrics_overview table...")
        r_metrics = U.handle_request(
            f"{self.base_url}metrics",
            {"project": None, "locations": None, "metrics": None},
            self.auth,
            {"accept": "application/json"},
        )
        # fmt: off
        if not isinstance(r_metrics, type(None)):
            try:
                m_ = pd.DataFrame(r_metrics.json())
            except Exception:
                raise E.ProfileError(f"\033[31;1mThe metrics overview is empty. This is your profile information:"  # noqa: E501  # pylint: disable=C0301
                                     f"\n {r_profile.json()}")
        if m_.empty:
            raise E.ProfileError(f"\033[31;1mThe metrics overview is empty. This is your profile information:"  # noqa: E501  # pylint: disable=C0301
                                 f"\n {r_profile.json()}")
        try:
            s_ = m_.apply(lambda x: x["metric"]
                          .replace(x["statistic"], "")
                         .replace(x["short_hand"], "")
                         .strip(), axis=1).str.strip("_").str.split("_", expand=True)  # noqa: E501  # pylint: disable=C0301
            # Just take the first two columns to avoid duplicates
            s_ = s_.iloc[:, :2]
            s_.columns = ["site_id", "location_id"]
        # fmt: on
        except Exception:
            self.metrics_overview = m_
        self.metrics_overview = pd.concat([m_, s_], axis=1)
        return self.authenticated

    @U.check_authentication
    @validate_call
    def get_metrics(
        self,
        site: Optional[str] = None,
        locations: Optional[Union[str, List[str]]] = None,
        metrics: Optional[Union[str, List[str]]] = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> Optional[List[Dict[str, Optional[str]]]]:
        """
        Get the metrics names for a site, provided the following parameters.

        Parameters
        ----------
        site : Optional[str]
            The site name. If None, the queryable metrics for all sites
            will be returned, and the locations and metrics parameters will be
            ignored.
        locations : Optional[Union[str, List[str]]]
            The locations for which to get the metrics. If None, all locations
            will be considered.
        metrics : Optional[Union[str, List[str]]]
            The metrics to get. They can be specified as regular expressions.
            If None, all metrics will be considered.

            For example:

            * | ``metrics=["^ACC", "^DEM"]`` will return all the metrics that
              | start with ACC or DEM,
            * Similarly, ``metrics=["windspeed$", "winddirection$"]`` will
              | return all the metrics that end with windspeed and
              | winddirection,
            * and ``metrics=[".*WF_A01.*",".*WF_A02.*"]`` will return all
              | metrics that contain WF_A01 or WF_A02.

        Returns
        -------
        Optional[List[Dict[str, Optional[str]]]]
            The metrics names for the given site, locations and metrics.

        .. note::
            This class method is legacy because it does not add functionality to
            the DataSignals pandas accessor.

        """
        url = f"{self.base_url}metrics"
        # fmt: on
        if headers is None:
            headers = {"accept": "application/json"}
        if site is None:
            params = {}
        if isinstance(locations, List):
            locations = ",".join(locations)
        if isinstance(metrics, List):
            metrics = ",".join(metrics)
        params = {
            "project": site,
            "locations": locations,
            "metrics": metrics,
        }

        r_ = U.handle_request(url, params, self.auth, headers)

        # Set the return type of the get_metrics method to the Metrics schema
        return r_.json()  # type: ignore

    @U.check_authentication
    def selected_metrics(self, data: pd.DataFrame) -> pd.DataFrame:
        """Return the selected metrics for the query."""
        if self.metrics_overview is None:
            raise E.ProfileError(
                "\033[31mThe metrics overview is empty. Please authenticate "
                "first with the \033[1mauthenticate\033[22m method."
            )
        if data.empty:
            raise E.DataSignalsError(
                "\033[31mThe \033[1mselected_metrics\033[22m method can only "
                "be called if the DataFrame is not empty, or after the "
                "\033[1mget_data\033[22m method has been called."
            )
        # Get the selected metrics as the Data columns that are available
        # in the metrics_overview DataFrame
        return self.metrics_overview[
            self.metrics_overview["metric"].isin(data.columns)
        ].set_index("metric")

    @U.check_authentication
    @validate_call(config=dict(arbitrary_types_allowed=True))
    def get_data(
        self,
        sites: Optional[Union[List, str]],
        locations: Optional[Union[List, str]],
        metrics: Union[List, str],
        start_timestamp: Union[str, datetime.datetime],
        end_timestamp: Union[str, datetime.datetime],
        outer_join_on_timestamp: bool = False,
        headers: Optional[Union[Dict[str, str]]] = None,
        data: Optional[pd.DataFrame] = None,
        as_dict: bool = False,
        as_star_schema: bool = False,
    ) -> Union[pd.DataFrame, Dict[str, Dict[str, pd.DataFrame]]]:
        """Get the data signals from the 24SEA API.

        Parameters
        ----------
        sites : Optional[Union[List, str]]
            The site name or List of site names. If None, the site will be
            inferred from the metrics.
        locations : Optional[Union[List, str]]
            The location name or List of location names. If None, the location
            will be inferred from the metrics.
        metrics : Union[List, str]
            The metric name or List of metric names. It must be provided.
            They do not have to be the entire metric name, but can be a part
            of it. For example, if the metric name is
            ``"mean_WF_A01_windspeed"``, the user can equivalently provide
            ``sites="wf"``, ``locations="a01"``, ``metric="mean windspeed"``.
        start_timestamp : Union[str, datetime.datetime]
            The start timestamp for the query. It must be in ISO 8601 format,
            e.g., ``"2021-01-01T00:00:00Z"`` or a datetime object.
        end_timestamp : Union[str, datetime.datetime]
            The end timestamp for the query. It must be in ISO 8601 format,
            e.g., ``"2021-01-01T00:00:00Z"`` or a datetime object.
        outer_join_on_timestamp : bool, optional
            If True, the data will be joined on the timestamp which will be the
            index of the DataFrame. If False, the data will be concatenated
            without any join. Default is False.
        headers : Optional[Union[Dict[str, str]]], optional
            The headers to pass to the request. If None, the default headers
            will be used as ``{"accept": "application/json"}``. Default is None.
        data : pd.DataFrame
            The DataFrame to update with the data signals. If None, a new
            DataFrame will be created. Default is None.
        as_dict : bool, optional
            If True, the data will be returned as a list of dictionaries.
            Default is False.
        as_star_schema : bool, optional
            If True, the data will be returned in a star schema format.
            Default is False.

        Returns
        -------
        Union[pd.DataFrame, Dict[str, Dict[str, pd.DataFrame]]]
            - The DataFrame containing the data signals, or
            - A dictionary containing the data signals divided by location, or
            - A dictionary containing the data signals in star schema format.
        """
        if as_star_schema:
            as_dict = True
        if data is None:
            data = pd.DataFrame()
        # Clean the DataFrame
        data_ = pd.DataFrame()
        # -- Step 1: Build the query object from GetData
        query = S.GetData(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
            sites=sites,
            locations=locations,
            metrics=metrics,
            headers=headers,
            outer_join_on_timestamp=outer_join_on_timestamp,
            as_dict=as_dict,
            as_star_schema=as_star_schema,
        )

        if query.sites is None and query.locations is None:
            query_str = (
                "metric.str.contains(@query.metrics, case=False, regex=True)"
            )
        elif query.sites is None and query.locations is not None:
            query_str = (
                "(location.str.lower() == @query.locations or location_id.str.lower() == @query.locations) "
                "and metric.str.contains(@query.metrics, case=False, regex=True)"
            )
        elif query.locations is None and query.sites is not None:
            query_str = (
                "(site.str.lower() == @query.sites or site_id.str.lower() == @query.sites) "
                "and metric.str.contains(@query.metrics, case=False, regex=True)"
            )
        else:
            query_str = (
                "(site_id.str.lower() == @query.sites or site.str.lower() == @query.sites) "
                "and (location.str.lower() == @query.locations or location_id.str.lower() == @query.locations) "
                "and metric.str.contains(@query.metrics, case=False, regex=True)"
            )

        nl = "\n"
        l_ = f"\033[30;1mQuery:\033[0;34m {query_str.replace(' and ', f'{nl}       and ')}\n"
        logging.info(l_)

        self._selected_metrics = self.metrics_overview.query(query_str).pipe(  # type: ignore  # noqa: E501  # pylint: disable=E501
            lambda df: df.sort_values(
                ["site", "location", "data_group", "short_hand", "statistic"],
                ascending=[True, True, False, True, True],
            )
        )
        logging.info("\033[32;1mMetrics selected for the query:\033[0m\n")
        # fmt: off
        logging.info(self._selected_metrics[["metric", "unit_str", "site",
                                             "location"]])
        # fmt: on
        data_frames = []
        grouped_metrics = self._selected_metrics.groupby(["site", "location"])

        # return grouped_metrics
        logging.info(
            f"\n\033[32;1mRequested time range:\033[0;34m "
            f"From {str(query.start_timestamp)[:-4].replace('T', ' ')} UTC "
            f"To {str(query.end_timestamp)[:-4].replace('T', ' ')} UTC\n\033[0m"
        )
        import concurrent.futures

        def fetch_data(site, location, group):
            # fmt: off
            s_ = "• " + ",".join(group["metric"].tolist()).replace(",", "\n           • ")  # noqa: E501  # pylint: disable=C0301
            logging.info(f"\033[32;1m\033[32;1m⏳ Getting data for {site} - "
                         f"{location}...\n  Metrics: \033[0;34m{s_}\n\033[0m")
            # fmt: on
            r_ = U.handle_request(
                f"{self.base_url}data",
                {
                    "start_timestamp": query.start_timestamp,
                    "end_timestamp": query.end_timestamp,
                    "project": [site],
                    "location": [location],
                    "metrics": ",".join(group["metric"].tolist()),
                },
                self.auth,
                query.headers,
            )
            # Warn if empty
            if r_.json() == []:
                logging.warning(
                    f"\033[33;1mNo data found for {site} - {location}.\033[0m"
                )
            return pd.DataFrame(r_.json())

        with concurrent.futures.ThreadPoolExecutor(4) as executor:
            # fmt: off
            future_to_data = {
                executor.submit(fetch_data,
                                site,
                                location,
                                group): (site, location)
                for (site, location), group in grouped_metrics
            }
            # fmt: on
            for future in concurrent.futures.as_completed(future_to_data):
                data_frames.append(future.result())
            # data_frames.append(pd.DataFrame(r_.json()))

        # if left_join_on_timestamp is True, lose the location and site columns
        # and join on timestamp
        if outer_join_on_timestamp:
            for i, df in enumerate(data_frames):
                if df.empty:
                    continue
                data_frames[i] = df.set_index("timestamp")
                data_frames[i].index = pd.to_datetime(data_frames[i].index)
                # drop site and location
                if "site" in data_frames[i].columns:
                    data_frames[i].drop(["site"], axis=1, inplace=True)
                if "location" in data_frames[i].columns:
                    data_frames[i].drop(["location"], axis=1, inplace=True)
            data_ = pd.concat([data_] + data_frames, axis=1, join="outer")
        else:
            data_ = pd.concat([data_] + data_frames, ignore_index=True)

        logging.info("\033[32;1m✔️ Data successfully retrieved.\033[0m")
        logging.info(
            "Your \033[30;1mpandas DataFrame\033[0m has been updated with the "
            "queried data."
        )
        data.drop(data.index, inplace=True)
        for col in data_.columns:
            if col in data.columns:
                del data[col]
            data[col] = data_[col]
            del data_[col]
        if as_dict:
            if as_star_schema:
                return to_star_schema(data, self.metrics_overview)
            return data.reset_index().to_dict("records")
        return data


def to_category_value(
    data: Union[pd.DataFrame, Dict[str, Dict[str, pd.DataFrame]]],
    metrics_overview: pd.DataFrame,
    keep_stat_in_metric_name: bool = False,
) -> pd.DataFrame:
    """
    Categorize the data based on the metrics overview.

    Parameters
    ----------
    data : Union[pd.DataFrame, Dict[str, Dict[str, pd.DataFrame]]]
        The data to be categorized. It can be either a DataFrame or a dictionary
        of DataFrames.
    metrics_overview : pd.DataFrame
        A DataFrame containing the information about the metrics.
    keep_stat_in_metric_name : bool, optional
        Whether to keep the statistic in the metric name, by default True.

    Returns
    -------
    Union[pd.DataFrame, Dict[str, Dict[str, pd.DataFrame]]]
        The data in category-value format, based on the metrics overview.

    Notes
    -----
    The function performs the following steps:
    1. Transforms the data dictionary into a DataFrame if necessary.
    2. Resets the index and converts the timestamp column to datetime.
    3. Melts the data to long format.
    4. Merges the melted data with the metrics overview DataFrame.
    5. Renames columns for consistency.
    6. Extracts latitude and heading information from the metric names.
    7. Extracts sub-assembly information from the metric names.
    8. Reorders the columns.
    9. Optionally appends the statistic to the metric name.
    10. Drops the rows where the metric name is "index", "site" or "location".

    Example
    -------
    >>> import pandas as pd
    >>> from typing import Union, Dict
    >>> data = {
    ...     'timestamp': ['2021-01-01', '2021-01-02'],
    ...     'mean_WF_A01_TP_SG_LAT005_DEG000': [1.0, 1.1],
    ...     'mean_WF_A02_TP_SG_LAT005_DEG000': [2.0, 2.1]
    ... }
    >>> metrics_overview = pd.DataFrame({
    ...     'metric': ['mean_WF_A01_TP_SG_LAT005_DEG000',
    ...                'mean_WF_A02_TP_SG_LAT005_DEG000'],
    ...     'short_hand': ['TP_SG_LAT005_DEG000', 'TP_SG_LAT005_DEG000'],
    ...     'statistic': ['mean', 'mean'],
    ...     'unit': ['unit', 'unit'],
    ...     'site': ['WindFarm', 'WindFarm'],
    ...     'location': ['WFA01', 'WFA02'],
    ...     'data_group': ['SG', 'SG'],
    ...     'site_id': ['WF', 'WF'],
    ...     'location_id': ['A01', 'A02']
    ... })
    >>> categorized = to_category_value(data, metrics_overview)
    >>> categorized
    +------------+--------------------------------+-------+------+-----------+---------------------+---------+-------------+-----+---------+-----------+----------+--------------+
    | timestamp  | full_metric_name               | value | unit | statistic | short_hand          | site_id | location_id | lat | heading | site      | location | metric_group |
    +============+================================+=======+======+===========+=====================+=========+=============+=====+=========+===========+==========+==============+
    | 2021-01-01 | mean_WF_A01_TP_SG_LAT005_DEG000| 1.0   | unit | mean      | TP_SG_LAT005_DEG000 | WF      | A01         | 5.0 | 0.0     | WindFarm  | WFA01    | SG           |
    +------------+--------------------------------+-------+------+-----------+---------------------+---------+-------------+-----+---------+-----------+----------+--------------+
    | 2021-01-02 | mean_WF_A01_TP_SG_LAT005_DEG000| 1.1   | unit | mean      | TP_SG_LAT005_DEG000 | WF      | A01         | 5.0 | 0.0     | WindFarm  | WFA01    | SG           |
    +------------+--------------------------------+-------+------+-----------+---------------------+---------+-------------+-----+---------+-----------+----------+--------------+
    | 2021-01-01 | mean_WF_A02_TP_SG_LAT005_DEG000| 2.0   | unit | mean      | TP_SG_LAT005_DEG000 | WF      | A02         | 5.0 | 0.0     | WindFarm  | WFA02    | SG           |
    +------------+--------------------------------+-------+------+-----------+---------------------+---------+-------------+-----+---------+-----------+----------+--------------+
    | 2021-01-02 | mean_WF_A02_TP_SG_LAT005_DEG000| 2.1   | unit | mean      | TP_SG_LAT005_DEG000 | WF      | A02         | 5.0 | 0.0     | WindFarm  | WFA02    | SG           |
    +------------+--------------------------------+-------+------+-----------+---------------------+---------+-------------+-----+---------+-----------+----------+--------------+
    """
    if isinstance(data, dict):
        data = pd.DataFrame(data)
    # Categorize the data
    # fmt: off
    data["timestamp"] = pd.to_datetime(data["timestamp"] \
                        if "timestamp" in data.columns else data.index)
    data = data.reset_index(drop=True)
    # Melt the data
    categorized = data.melt(id_vars=["timestamp"],
                            var_name="metric",
                            value_name="value")
    # Merge the melted data with the metrics overview DataFrame
    categorized = categorized.merge(metrics_overview, how="left",
                                    left_on="metric", right_on="metric")
    # Rename the columns
    categorized.rename(columns={"unit_str": "unit",
                                "data_group": "metric_group"},
                       inplace=True)
    # Get the lat, and heading from the metric name
    categorized["lat"] = categorized["metric"] \
                         .str.extract(r"(_LAT)(\w{3})")[1].astype(float)
    categorized["heading"] = categorized["metric"] \
                             .str.extract(r"(_DEG)(\w{3})")[1].astype(float)
    # Now get the subassembly from the metric name.
    categorized["sub_assembly"] = categorized["metric"] \
                                  .str.extract(r"(_TP_)|(_TW_)|(_MP_)") \
                                  .bfill(axis=1) \
                                  .infer_objects(copy=False)[0] \
                                  .str.replace("_", "")
    # Reorder the columns
    columns = ["timestamp", "metric", "value", "unit", "statistic",
               "short_hand", "site_id", "location_id", "sub_assembly", "lat",
               "heading", "site", "location", "metric_group"]
    categorized = categorized[columns]
    if keep_stat_in_metric_name:
        categorized["stat_short_hand"] = categorized["statistic"] \
                                         + "_" \
                                         + categorized["short_hand"]
    # Drop the rows where the value of column metric is "index", "site" or
    # "location"
    # fmt: on
    categorized = categorized[
        ~categorized["metric"].isin(["index", "site", "location"])
    ]
    return categorized.reset_index(drop=True)


def to_star_schema(
    data: Union[pd.DataFrame, Dict[str, List[Dict[str, Any]]]],
    metrics_overview: pd.DataFrame,
) -> Dict[str, pd.DataFrame]:
    """
    Transforms the data and metrics_overview into a star schema format for
    analytical purposes.

    Parameters
    ----------
    data : Union[pd.DataFrame, Dict[str, list[dict[str, Any]]]]
        A DataFrame or dictionary representing the raw data. The keys are column
        column names, and the values are lists of data.
        Must include a "timestamp" column or have indices that can be converted
        to timestamps.
    metrics_overview : pd.DataFrame
        A DataFrame containing metadata for metrics, including the following
        required columns:
        - | 'metric': The metric names (must match column names in `data`).
        - | 'short_hand': Short descriptive names for the metrics.
        - | 'description': Detailed descriptions of the metrics.
        - | 'statistic': Aggregation or statistical operation (e.g., mean,
        | std).
        - | 'unit_str': The units for the metrics.
        - | 'location': Location identifiers.
        - | 'site': Windfarm identifiers.
        - | 'data_group': Grouping of data (e.g., "scada").

    Returns
    -------
    dict[str, pd.DataFrame]
        A dictionary containing the following tables:

        - | 'FactData': The fact table linking metrics to timestamps,
          | locations, and metric IDs.
        - | 'DimMetric': Dimension table for metrics, including metric ID,
          | short name, description, statistic, and unit.
        - | 'DimWindFarm': Dimension table for wind farms, including
          | locations and sites.
        - | 'DimCalendar': Dimension table for time, including date parts
          | (year, month, day, hour, minute).
        - | 'DimDataGroup': Dimension table for data groups.

    Raises
    ------
    ValueError
        If required columns are missing in `data` or `metrics_overview`.
    KeyError
        If the `metric` column in `metrics_overview` contains values not present
        in `data`.

    Example
    -------
    >>> import pandas as pd
    >>> data = {
    ...     'timestamp': ['2020-01-01T00:00:00Z', '2020-01-01T00:10:00Z'],
    ...     'mean_WF_A01_winddirection': [257.445, 262.03],
    ...     'std_WF_A01_windspeed': [1.5165, 1.7966]
    ... }
    >>> metrics_overview = pd.DataFrame({
    ...     'metric': ['mean_WF_A01_winddirection', 'std_WF_A01_windspeed'],
    ...     'short_hand': ['winddirection', 'windspeed'],
    ...     'description': ['Wind direction', 'Wind speed'],
    ...     'statistic': ['mean', 'std'],
    ...     'unit_str': ['°', 'm/s'],
    ...     'location': ['WFA01', 'WFMA4'],
    ...     'site': ['windfarm', 'windfarm'],
    ...     'data_group': ['scada', 'scada']
    ... })
    >>> result = to_star_schema(data, metrics_overview)
    >>> for key, df in result.items():
    ...     print(f"{key}: {df.to_markdown()}")
    """
    # fmt: off
    # Input validation
    req_metrics_cols = {"metric", "short_hand", "description", "statistic",
                        "unit_str","location", "site", "data_group"}
    if not req_metrics_cols.issubset(metrics_overview.columns):
        raise ValueError("metrics_overview must contain the following columns: "
                         f"{req_metrics_cols}")

    if isinstance(data, dict):
        data = pd.DataFrame(data)

    # If site and location are not present in the data, drop them
    data.drop(columns=['site', 'location'], errors='ignore', inplace=True)

    # Ensure timestamps are datetime
    if not data.empty:
        if isinstance(data.index, pd.DatetimeIndex):
            data["timestamp"] = data.index
        if "timestamp" not in data.columns:
            raise ValueError("`data` must include a 'timestamp' column or "
                             "indices convertible to timestamps.")

    if "timestamp" not in data.columns:
        raise ValueError("`data` must include a 'timestamp' column or indices "
                         "convertible to timestamps.")

    missing_metrics = set(data.columns) \
                      - {"timestamp", "index", "site", "location"} \
                      - set(metrics_overview["metric"])
    if missing_metrics:
        raise KeyError("The following metrics in `data` are "
                      f"missing from `metrics_overview`: {missing_metrics}")
    # fmt: on
    # Ensure timestamps are datetime
    data["timestamp"] = pd.to_datetime(data["timestamp"])
    data = data.reset_index(drop=True)

    # Reshape the data to long format
    fact_metrics = data.melt(
        id_vars=["timestamp"], var_name="metric", value_name="value"
    )

    # Create DimMetric with metric_id
    dim_metric = metrics_overview[
        ["metric", "short_hand", "description", "statistic", "unit_str"]
    ].drop_duplicates()
    dim_metric.rename(columns={"short_hand": "short_str"}, inplace=True)

    # Generate unique metric_id as a composite key
    dim_metric["metric_id"] = (
        dim_metric["statistic"] + "_" + dim_metric["short_str"]
    )

    # Map metric_id to the fact table
    metric_to_id = dim_metric.set_index("metric")["metric_id"]
    fact_metrics["metric_id"] = fact_metrics["metric"].map(metric_to_id)

    # Dimension table for WindFarm
    dim_windfarm = (
        metrics_overview[["location", "site"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    # Map site and location to fact table
    metric_to_site_location = metrics_overview[
        ["metric", "site", "location"]
    ].set_index("metric")
    fact_metrics["location"] = fact_metrics["metric"].map(
        metric_to_site_location["location"]
    )
    fact_metrics["site"] = fact_metrics["metric"].map(
        metric_to_site_location["site"]
    )

    # Dimension table for Calendar
    dim_calendar = (
        fact_metrics[["timestamp"]].drop_duplicates().reset_index(drop=True)
    )
    dim_calendar["year"] = dim_calendar["timestamp"].dt.year
    dim_calendar["month"] = dim_calendar["timestamp"].dt.month
    dim_calendar["day"] = dim_calendar["timestamp"].dt.day
    dim_calendar["hour"] = dim_calendar["timestamp"].dt.hour
    dim_calendar["minute"] = dim_calendar["timestamp"].dt.minute

    # Dimension table for DataGroup
    dim_data_group = (
        metrics_overview[["data_group"]]
        .drop_duplicates()
        .reset_index(drop=True)
    )

    # Add data_group_id to fact_metrics
    data_group_map = (
        metrics_overview[["metric", "data_group"]]
        .drop_duplicates()
        .set_index("metric")["data_group"]
    )
    fact_metrics["data_group"] = fact_metrics["metric"].map(data_group_map)

    # Select and reorder columns for the fact table
    fact_metrics = fact_metrics[
        ["timestamp", "location", "data_group", "metric_id", "value"]
    ]

    return {
        "FactData": fact_metrics,
        "DimMetric": dim_metric[
            ["metric_id", "short_str", "description", "statistic", "unit_str"]
        ],
        "DimWindFarm": dim_windfarm,
        "DimCalendar": dim_calendar,
        "DimDataGroup": dim_data_group,
    }
