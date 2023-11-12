import argparse
import requests
import gzip
import io
import os
from datetime import datetime

def download_and_uncompress(url, output_filename, output_dir):
	"""
	Download, uncompress, and save data from the given URL, and create a symlink.

	Parameters:
	url (str): URL of the file to download.
	output_filename (str): Name of the file to save the data to.
	output_dir (str): Directory to save the file.
	"""
	# Get current time and format it as -HHMM
	timestamp = datetime.now().strftime("-%H%M")

	# Determine the file extension and insert the timestamp before the extension
	file_name, file_extension = os.path.splitext(output_filename)
	output_filename_with_timestamp = f"{file_name}{timestamp}{file_extension}"
	full_path = os.path.join(output_dir, output_filename_with_timestamp)

	response = requests.get(url, stream=True)
	if response.status_code == 200:
		with gzip.open(io.BytesIO(response.content), 'rb') as file_in:
			with open(full_path, 'wb') as file_out:
				file_out.write(file_in.read())

		# Create symlink in the directory above
		symlink_name = f"{file_name}_current{file_extension}"
		symlink_path = os.path.join(os.path.dirname(output_dir), symlink_name)
		if os.path.exists(symlink_path):
			os.remove(symlink_path)
		os.symlink(full_path, symlink_path)

		print(f'Data saved to {full_path}')
		print(f'Symlink created at {symlink_path}')
	else:
		print(f'Error: Unable to download data from {url}')

def main():
	# Command line arguments
	parser = argparse.ArgumentParser(description='Download and Uncompress Aviation Weather Data')
	parser.add_argument('--metar', action='store_true', help='Download and uncompress METAR data')
	parser.add_argument('--taf', action='store_true', help='Download and uncompress TAF data')
	parser.add_argument('--airsigmet', action='store_true', help='Download and uncompress AirSIGMET data')
	parser.add_argument('--stations', action='store_true', help='Download and uncompress Station data')
	parser.add_argument('--output_dir', type=str, default='.', help='Directory to save the files (default: current directory)')
	args = parser.parse_args()

	# Ensure output directory exists
	if not os.path.exists(args.output_dir):
		os.makedirs(args.output_dir)

	# URLs for data
	urls = {
		'metar': 'https://aviationweather.gov/data/cache/metars.cache.csv.gz',
		'taf': 'https://aviationweather.gov/data/cache/tafs.cache.csv.gz',
		'airsigmet': 'https://aviationweather.gov/data/cache/airsigmets.cache.csv.gz',
		'stations': 'https://aviationweather.gov/data/cache/stations.cache.json.gz'
	}

	# Download and uncompress requested data
	if args.metar:
		download_and_uncompress(urls['metar'], 'metars.csv', args.output_dir)
	if args.taf:
		download_and_uncompress(urls['taf'], 'tafs.csv', args.output_dir)
	if args.airsigmet:
		download_and_uncompress(urls['airsigmet'], 'airsigmets.csv', args.output_dir)
	if args.stations:
		download_and_uncompress(urls['stations'], 'stations.json', args.output_dir)

if __name__ == "__main__":
	main()

