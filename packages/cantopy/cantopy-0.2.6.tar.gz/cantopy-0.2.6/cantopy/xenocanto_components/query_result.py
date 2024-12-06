from cantopy.xenocanto_components.result_page import ResultPage
from cantopy.xenocanto_components.recording import Recording
import pandas as pd


class QueryResult:
    """Wrapper container for storing all the ResultPages returned by the XenoCanto API in response to a given Query in one place.

    Attributes
    ----------
    available_num_recordings : int
        The total available number of recordings found for this query,
        independent of the amount of recordings in this QueryResult.
    available_num_species : int
        The total available number of species found for this query,
        independent of the amount of recordings in this QueryResult.
    available_num_pages : int
        The total number of pages available for this query.
    result_pages: list[ResultPage]
        List of all the returned pages for the query

    """

    def __init__(self, query_metadata: dict[str, int], result_pages: list[ResultPage]):
        """Create a QueryResult container.

        Parameters
        ----------
        query_metadata
            Dictionary containing metadata information about the query results,
            the dict keys are: "available_num_recordings", "available_num_species", "available_num_pages".
        result_pages
            List of all the returned pages for the query.

        """

        # Set the query metadata attributes
        self.available_num_recordings = int(query_metadata["available_num_recordings"])
        self.available_num_species = int(query_metadata["available_num_species"])
        self.available_num_pages = query_metadata["available_num_pages"]

        # Set the result pages
        self.result_pages = result_pages

    def get_all_recordings(self) -> list[Recording]:
        """Return all the recordings contained in this QueryResult, across all ResultPages.

        Returns
        -------
        List[Recording]
            List of all the recordings contained in this QueryResult.

        """

        # Initialize the list of recordings
        all_recordings: list[Recording] = []

        # Loop over all the result pages
        for result_page in self.result_pages:
            # Add all the recordings to the list
            all_recordings.extend(result_page.recordings)

        # Return the list of recordings
        return all_recordings
    
    def get_all_recordings_metadata(self) -> pd.DataFrame:
        """Return all the recordings metadata contained in this QueryResult, across all 
        ResultPages.

        Returns
        -------
        pd.DataFrame
            DataFrame containing all the recordings metadata contained in this 
            QueryResult.

        """

        all_recordings = self.get_all_recordings()

        all_recordings_metadata = pd.concat(
            [recording.to_dataframe_row() for recording in all_recordings],
            ignore_index=True
        )

        return pd.DataFrame(all_recordings_metadata)
