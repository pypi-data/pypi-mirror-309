# fdcodepy

## Introduction

- FD_codepy is an open-source python package that can be used to extract time series in an interpretable manner, and use it for compression.
- The key idea is proposed specifically for metered data in energy sector, but can also be used with smart sensors and edge computing.
- Inspired by Codebook method, it breaks down the time series data into its constituent parts, i.e., the unique sub-patterns called Codewords, and the index of the Codewords, i.e., representations, allowing for efficient compression and analysis.
- Compared to resampling data into lower resolution, this lossy compression method takes similar data storage and transmission bandwidth, while preserving high frequency information and accumulative/average metered values.

- The FD_codepy source code is on GitHub: https://github.com/abc123yuanrui/FD_codepy/

  - An example is provided in example/test.ipynb

## Key method for time series compression

- `Codebook`: key class for reconstructing long energy time series into unique partitions (codewords) and representations. Check examples for details.
  - It takes time series, window size, and distance metric types as inputs.
  - Four ensambled distance methods are:
    - Euclidean Distance (default or `'euclidean'`)
    - Dynamic Time Warping (`'DTW'`)
    - Wasserstein Distance (`'Wasserstein'`)
    - Flexibility Distance (`'flexibilityD'`)
  - `preprocessing` method will normalise the data into normalised series as attribute `normalized_arr`, with the scaler attribute `scaler_average`
  - `get_distance_matrix` method is a statistical analysis that computes the distance matrix for long time series (assuming we know historical data). It returns the matrix and quantile result for setting a similarity threshold (otherwise, the threshold can be set by an empirical value).
  - `desolve_time_series_thre` process the time seires into `codewords` and `representations`, return them.
  - `post_processing` reconstructe time series based on codewords and representations, the result stores as attribute `recovered_series`
- Flexbility distance: a novel distance metric that measures the similarity between time series data while taking into account both temporal and amplitude distance, and the rebound effect of the data.

## Installation

- Install using pip: `pip install fdcodepy`

## Usage

- Import the package: `import fdcodepy`
- Step by step example: Codebook processing for a given hourly time series and window size of 24, which decides the compression ratio (same with resmpling data from hourly into daily)
  - `from fdcodepy import methods`
  - `sample_series = np.random.uniform(0, 30, 365*24)`
  - `series_codebook = methods.Code_book(time_series, 24, 'flexibilityD')`
  - `series_codebook.pre_processing()`
  - `distance_matrix, quantiles = series_codebook.get_distance_matrix()`
  - `codewords, representations = series_codebook.desolve_time_series_thre(quantiles[0])`
  - `series_codebook.post_processing()`
  - `series_codebook.recovered_series` is the reconstruted data, computed from the representations with only lenght of `len(representations)`, compared to original series with length `len(sample_series)`
- The representations are the length of data needs to be communicated to data center, which is equal to the size of downsampled data, in this case, 365
- Use the Codebook processing result to generate a report
  - `from fdcodepy.utils.helpers import code_book_processing_analysis`
  - `code_book_processing_analysis(series_codebook, time_index, report = True, export_dir = '.')`
- Use the `FlexibilityDistance` to compute the flexibility distance between two time series datasets (with default settings).
  - `from fdcodepy import methods`
  - `Code_book.flex_distance(time_series_1, time_series_2)`
