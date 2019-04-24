# Description

Downloads a CSV file and displays the average tip_amount and total line count.

The code is designed to run as fast as possible.

## How to run it

Execute the following commands:

    git clone https://github.com/vfernandezmartinez/average_calculator.git
    cd average_calculator
    time python3 calculate.py <url_of_csv>

## Implementation notes

  * Since requirements specify that only vanilla Python 3 should be used, no modules such as [pandas](https://pandas.pydata.org/) or [numpy](https://www.numpy.org/) were used.

  * Network is assumed to be fast. On a regular home Internet connection, the download speed may become the main performance limiting factor. For example, at my home it downloads at a slow 1.2MB/s thus taking around 20 minutes to download. However, if the script is run from a cloud provider, network speed will be much faster. For example, at 100MB/s, it would take around 16 seconds, which is less than it takes to process the CSV. For that reason, the main focus of the implementation is on improving the CSV processing speed.

  * The implementation does not verify the integrity of the downloaded data, since this is not a requirement. However, when downloading large files via HTTP(S), the integrity should be verified. The reason is that HTTP is not designed for transferring large files. For example, a MD5/SHA1 hash of the file could be downloaded from the remote server and compared with the hash of the downloaded file.

  * The CSV is processed while it is being downloaded. It is not temporarily stored anywhere.

  * To increase performance, the data is assumed to be in ASCII, thus allowing us to save decoding of UTF-8 data. This is the case of the provided CSV.

  * The data is read in chunks of 64 KB. readline() is not used, which increases performance in this case.

  * As a result of the above, a limitation of the implementation is that the header line cannot be longer than 64 kbytes.

  * `line.split(b',')` is included twice instead of only once because that provides a slight performance improvement of ~1%.

  * The returned line count includes the header line. Therefore, the total number of records in the CSV is the line count - 1.

## Tested approaches

The following approaches were also attempted but they turned out to be slower/worse/not possible:

  * Use a regular expression to extract the tip_amount field instead of `line.split(b',')`. This was ~20% slower than the current implementation.

  * Use csv.reader(). This was ~133% slower.

  * Download data in binary chunks but process each chunk byte by byte instead of using split(). This was ~166% slower.

  * Use ctypes to import libc.so, then use strtok(). Even though strtok() would be fast in C, this approach is very slow.

  * Enable compression. This would be beneficial for slow download speeds. However, for fast connections, the time it takes to uncompress the file might turn out to be bigger than it takes to download the whole file uncompressed. Technically, the request could contain the `Accept-Encoding: br,gzip,deflate` header. Unfortunately, S3 ignores this header. When using CloudFront, compression is supported but [only for files up to 10MB](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/ServingCompressedFiles.html#compressed-content-cloudfront). One option would be pre-compress the file with gzip and configure S3 to add the `Content-Encoding: gzip` response header. But that requires changes in your S3 bucket which are out of the scope of this script.

## Unit Tests

A simple unit test is included to ensure code correctness. To run it:

    python3 -m unittest
