import pysubs2
from subdeloc_tools.common.utils.logger_config import logger

def load_ass(file_path: str) -> pysubs2.SSAFile:
	try:
		subs = pysubs2.load(file_path)
		return subs
	except Exception as e:
		print(f"Error loading file '{file_path}': {e}")
		return None

# Shift subs by an amount of seconds
# time in seconds
# thresh in milliseconds
def shift_sub(path: str, time: int, threshold: int) -> str:
	logger.debug("Shifting {} seconds from {}".format(time, threshold))
	fname = "shifted.ass"
	subs = load_ass(path)
	for line in subs:
		if line.start > threshold:
			line.shift(s=time)
	subs.save(fname)
	return fname